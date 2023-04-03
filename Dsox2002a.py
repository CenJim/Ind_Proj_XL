import struct
import sys

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import numpy as np
import pandas as pd

import os

debug = 0

class Dsox2002a():
    def __init__(self, Resource_Manager, SCOPE_VISA_ADDRESS):
        self.rm = Resource_Manager
        self.osc_handle = None
        self.connectstatus = False
        self.visa_address = SCOPE_VISA_ADDRESS
        self.NUMBER_ANALOG_CHS = 2
        self.channelstatus = None
        self.waveformstatus = None
        self.triggerstatus = None
        self.timebasestatus = None

        self.CHS_ON = None
        self.ANALOGVERTPRES = None
        self.NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE = None
        self.NUMBER_CHANNELS_ON = None
        self.TOTAL_BYTES_TO_XFER = None
        self.ACQ_TYPE = None

    def getResoureList(self):
        resource = str(self.rm.list_resources())
        resource = resource.split("'")
        result = []
        for item in resource:
            if len(item) > 10:
                result.append(item)
        return result

    def connect(self):
        if self.connectstatus == False:
            try:
                self.osc_handle = self.rm.open_resource(self.visa_address)
            except Exception:
                print("Unable to connect to oscilloscope at " + str(self.visa_address))
                sys.exit()
                return False
            print("Successfully Connected to Device")
            self.osc_handle.timeout = 10000
            self.osc_handle.clear()
            self.connectstatus = True
        else:
            print("Device already connected")
        return self.osc_handle

    def disconnect(self):
        if self.connectstatus == True:
            self.osc_handle.clear()
            self.osc_handle.close()
            self.osc_handle = None
            self.connectstatus = False
            print("Device Successfully Disconnected")
            return True
        else:
            print("Device not Connected")
            return False

    def reset(self):
        self.osc_handle.write("*RST")

    def autoScale(self):
        self.osc_handle.write(":AUToscale")

    def queryIDN(self):
        IDN = str(self.osc_handle.query("*IDN?")).rstrip()
        IDN = IDN.split(',')
        return IDN

    def queryOPT(self):
        OPT = str(self.osc_handle.query("*OPT?")).rstrip()
        OPT = OPT.split(',')
        result = []
        for items in OPT:
            if items[0] != "0":
                result.append(items)
        return result

    def queryChannelStatus(self):
        option = ["BANDwidth", "BWLimit", "COUPling", "DISPlay", "IMPedance", "INVert", "LABel",
                  "OFFSet", "PROBe", "PROTection", "RANGe", "SCALe", "UNITs", "VERNier"]
        channelstatus = {}
        for items in option:
            tail = ":" + items + "?"
            channelstatus[items] = []
            for channels in range(1, self.NUMBER_ANALOG_CHS + 1):
                channelstatus[items].append(self.osc_handle.query(":CHANnel" + str(channels) + tail).rstrip())
        self.channelstatus = channelstatus
        return channelstatus

    def configChannel(self, channelstatus):
        options = ["BANDwidth", "BWLimit", "COUPling", "DISPlay", "IMPedance", "INVert", "LABel",
                   "OFFSet", "PROBe", "RANGe", "SCALe", "UNITs", "VERNier"]
        for items in options:
            status = channelstatus[items]
            for channels in range(4):
                # print(":CHANnel" + str(channels+1)+":"+items + " " + status[channels])
                self.osc_handle.write(":CHANnel" + str(channels + 1) + ":" + items + " " + status[channels])
        return True

    # for the first experiment operation
    def capture_DC(self):
        self.do_command(":AUToscale")
        # self.do_command(":TRIGger:MODE EDGE")
        # self.do_command(":TRIGger:EDGE:SOURce CHANnel1")

    # =========================================================
    # Capture:
    # =========================================================
    def capture(self):
        # Use auto-scale to automatically set up oscilloscope.
        print("Autoscale.")
        self.do_command(":AUToscale")
        # Set trigger mode.
        self.do_command(":TRIGger:MODE EDGE")
        qresult = self.do_query_string(":TRIGger:MODE?")
        print("Trigger mode: %s" % qresult)
        # Set EDGE trigger parameters.
        self.do_command(":TRIGger:EDGE:SOURce CHANnel1")
        qresult = self.do_query_string(":TRIGger:EDGE:SOURce?")
        print("Trigger edge source: %s" % qresult)
        self.do_command(":TRIGger:EDGE:LEVel 1.5")
        qresult = self.do_query_string(":TRIGger:EDGE:LEVel?")
        print("Trigger edge level: %s" % qresult)
        self.do_command(":TRIGger:EDGE:SLOPe POSitive")
        qresult = self.do_query_string(":TRIGger:EDGE:SLOPe?")
        print("Trigger edge slope: %s" % qresult)
        # set the probe ratio
        self.do_command(":CHANnel1:PROBe 1")
        # Save oscilloscope setup.
        sSetup = self.do_query_ieee_block(":SYSTem:SETup?")
        f = open("setup.stp", "wb")
        f.write(bytes(sSetup))
        f.close()
        print("Setup bytes saved: %d" % len(bytes(sSetup)))
        # Change oscilloscope settings with individual commands:
        # Set vertical scale and offset.
        # self.do_command(":CHANnel1:SCALe 0.05")
        qresult = self.do_query_string(":CHANnel1:SCALe?")
        print("Channel 1 vertical scale: %s" % qresult)
        # self.do_command(":CHANnel1:OFFSet -1.5")
        qresult = self.do_query_string(":CHANnel1:OFFSet?")
        print("Channel 1 offset: %s" % qresult)
        # Set horizontal scale and offset.
        # self.do_command(":TIMebase:SCALe 0.0002")
        qresult = self.do_query_string(":TIMebase:SCALe?")
        print("Timebase scale: %s" % qresult)
        # self.do_command(":TIMebase:POSition 0.0")
        qresult = self.do_query_string(":TIMebase:POSition?")
        print("Timebase position: %s" % qresult)
        # Set the acquisition type.
        # self.do_command(":ACQuire:TYPE NORMal")
        qresult = self.do_query_string(":ACQuire:TYPE?")
        print("Acquire type: %s" % qresult)
        # Or, set up oscilloscope by loading a previously saved setup.
        sSetup = ""
        f = open("setup.stp", "rb")
        sSetup = f.read()
        f.close()
        # self.do_command_ieee_block(":SYSTem:SETup", sSetup) #have some problem!! invalid data
        print("Setup bytes restored: %d" % len(sSetup))
        # Capture an acquisition using :DIGitize.
        self.do_command(":DIGitize CHANnel1")

    def measure_waveform(self):
        # Make measurements.
        # --------------------------------------------------------
        self.do_command(":MEASure:SOURce CHANnel1")
        qresult = self.do_query_string(":MEASure:SOURce?")
        print("Measure source: %s" % qresult)
        self.do_command(":MEASure:FREQuency")
        qresult = self.do_query_string(":MEASure:FREQuency?")
        print("Measured frequency on channel 1: %s" % qresult)
        self.do_command(":MEASure:VAMPlitude")
        qresult = self.do_query_string(":MEASure:VAMPlitude?")
        print("Measured vertical amplitude on channel 1: %s" % qresult)
        self.do_command(":MEASure:VRMS")
        qresult = self.do_query_string(":MEASure:VRMS?")
        print("Measured DC RMS on channel 1: %s" % qresult)

    def measure_DC_Vrms(self):
        # return the Vrms value
        # self.do_command(":AUToscale")
        self.do_command(":MEASure:VRMS DISPlay,DC,CHANnel1")
        qresult = float(self.do_query_string(":MEASure:VRMS?"))
        print("Measured DC RMS on channel 1: %.3f" % qresult)
        return qresult

    def measure_Vpp(self):
        self.do_command(":MEASure:VPP CHANnel1")
        qresult = float(self.do_query_string(":MEASure:VPP?"))
        print("Measured Vpp on channel 1: %.3f" % qresult)
        return qresult

    def measure_Vmax(self):
        self.do_command(":MEASure:VMAX CHANnel1")
        qresult = float(self.do_query_string(":MEASure:VMAX?"))
        print("Measured Vmax on channel 1: %.3f" % qresult)
        return qresult

    def measure_frequency(self):
        self.do_command(":MEASure:FREQuency CHANnel1")
        qresult = float(self.do_query_string(":MEASure:FREQuency?"))
        print("Measured Frequency on channel 1: %.3f" % qresult)
        return qresult

    def measure_period(self):
        self.do_command(":MEASure:PERiod CHANnel1")
        qresult = float(self.do_query_string(":MEASure:PERiod?"))
        print("Measured Period on channel 1: %.3f" % qresult)
        return qresult

    def analyze_waveform(self, file_path):
        # Download waveform data.
        # --------------------------------------------------------
        # Set the waveform points mode.
        self.do_command(":WAVeform:POINts:MODE RAW")
        qresult = self.do_query_string(":WAVeform:POINts:MODE?")
        print("Waveform points mode: %s" % qresult)
        # Get the number of waveform points available.
        self.do_command(":WAVeform:POINts 100000")
        qresult = self.do_query_string(":WAVeform:POINts?")
        print("Waveform points available: %s" % qresult)
        # Set the waveform source.
        self.do_command(":WAVeform:SOURce CHANnel1")
        qresult = self.do_query_string(":WAVeform:SOURce?")
        print("Waveform source: %s" % qresult)
        # Choose the format of the data returned:
        self.do_command(":WAVeform:FORMat BYTE")
        print("Waveform format: %s" % self.do_query_string(":WAVeform:FORMat?"))
        # Display the waveform settings from preamble:
        wav_form_dict = {
            0: "BYTE",
            1: "WORD",
            4: "ASCii",
        }
        acq_type_dict = {
            0: "NORMal",
            1: "PEAK",
            2: "AVERage",
            3: "HRESolution",
        }
        preamble_string = self.do_query_string(":WAVeform:PREamble?")
        (
            wav_form, acq_type, wfmpts, avgcnt, x_increment, x_origin,
            x_reference, y_increment, y_origin, y_reference
        ) = preamble_string.split(",")
        print("Waveform format: %s" % wav_form_dict[int(wav_form)])
        print("Acquire type: %s" % acq_type_dict[int(acq_type)])
        print("Waveform points desired: %s" % wfmpts)
        print("Waveform average count: %s" % avgcnt)
        print("Waveform X increment: %s" % x_increment)
        print("Waveform X origin: %s" % x_origin)
        print("Waveform X reference: %s" % x_reference)
        print("Waveform Y increment: %s" % y_increment)
        print("Waveform Y origin: %s" % y_origin)
        print("Waveform Y reference: %s" % y_reference)
        # Always 0.
        # Get numeric values for later calculations.
        x_increment = self.do_query_number(":WAVeform:XINCrement?")
        x_origin = self.do_query_number(":WAVeform:XORigin?")
        y_increment = self.do_query_number(":WAVeform:YINCrement?")
        y_origin = self.do_query_number(":WAVeform:YORigin?")
        y_reference = self.do_query_number(":WAVeform:YREFerence?")
        # Get the waveform data.
        sData = self.do_query_ieee_block(":WAVeform:DATA?")
        # Unpack unsigned byte data.
        values = struct.unpack("%dB" % len(bytes(sData)), bytes(sData))
        print("Number of data values: %d" % len(values))
        # Save waveform data values to CSV file.
        directory = 'data'
        path = os.path.join(file_path, directory)
        if not os.path.exists(path):
            os.mkdir(path)
        f = open(file_path + "/data/waveform_data.csv", "w")
        for i in range(0, len(values) - 1):
            time_val = x_origin + (i * x_increment)
            voltage = ((values[i] - y_reference) * y_increment) + y_origin
            f.write("%E, %f\n" % (time_val, voltage))
        f.close()
        print("Waveform format BYTE data written to waveform_data.csv.")
        # waveform_data = pd.read_csv('data/waveform_data.csv')
        # waveform_data.plot(0,1)
        # plt.show()
        self.draw_csv(file_path + '/data/waveform_data.csv')

    # draw the csv file
    def draw_csv(self, fileName):
        csvFile = pd.read_csv(fileName)
        csvFile.plot(0, 1)
        plt.show()

    # =========================================================
    # Send a command and check for errors:
    # =========================================================
    def do_command(self, command, hide_params=False):
        if hide_params:
            (header, data) = command.split(" ", 1)
            if debug:
                print("\nCmd = '%s'" % header)
        else:
            if debug:
                print("\nCmd = '%s'" % command)
        self.osc_handle.write("%s" % command)
        # if hide_params:
        #     self.check_instrument_errors(header)
        # else:
        #     self.check_instrument_errors(command)

    # =========================================================
    # Send a command and binary values and check for errors:
    # =========================================================
    def do_command_ieee_block(self, command, values):
        if debug:
            print("Cmb = '%s'" % command)
        self.osc_handle.write_binary_values("%s " % command, values, datatype='B')
        # self.check_instrument_errors(command)

    # =========================================================
    # Send a query, check for errors, return string:
    # =========================================================
    def do_query_string(self, query):
        if debug:
            print("Qys = '%s'" % query)
        result = self.osc_handle.query("%s" % query)
        # self.check_instrument_errors(query)
        return result

    # =========================================================
    # Send a query, check for errors, return floating-point value:
    # =========================================================
    def do_query_number(self, query):
        if debug:
            print("Qyn = '%s'" % query)
        results = self.osc_handle.query("%s" % query)
        # self.check_instrument_errors(query)
        return float(results)

    # =========================================================
    # Send a query, check for errors, return binary values:
    # =========================================================
    def do_query_ieee_block(self, query):
        if debug:
            print("Qys = '%s'" % query)
        result = self.osc_handle.query_binary_values("%s" % query, datatype='s')
        # self.check_instrument_errors(query)
        return result

    # =========================================================
    # Check for instrument errors:     have some problems!! always have error
    # =========================================================
    def check_instrument_errors(self,command):
        while True:
            error_string = self.osc_handle.query(":SYSTem:ERRor?")
            if error_string:  # If there is an error string value.
                if error_string.find("+0,", 0, 3) == -1:  # Not "No error".
                    print("ERROR: %s, command: '%s'" % (error_string, command))
                    print("Exited because of error.")
                    sys.exit(1)
                else:  # "No error"
                    break
            else:  # :SYSTem:ERRor? should always return string.
                print("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" % command)
                print("Exited because of error.")
                sys.exit(1)