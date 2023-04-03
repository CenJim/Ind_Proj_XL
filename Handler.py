import time
from statistics import quantiles

import numpy as np
import pandas as pd
from serial import SerialException

from serial_motor import SerialSender

class Handler:
    def __init__(self, osc, fgen):
        self.osc = osc
        self.fgen = fgen
        self.angle = []
        self.angle_Vosc = [[], [], [], [], [], []]
        self.angle_flag = 0
        self.pause = 0
        self.Vgen = []
        self.Vosc = [[], [], [], [], [], []]
        self.fgen_osc_result = np.array([])
        self.angle_osc_result = np.array([])
        self.fgen_osc_done = 0
        self.angle_osc_done = 0
        # self.serial_sender = SerialSender()

    # "1" is on, others are off
    def fgen_ch1_switch(self, flag):
        if flag == 1:
            self.fgen.ch1.set_output("ON")
        else:
            self.fgen.ch1.set_output("OFF")

    # "1" is on, others are off
    def fgen_ch2_switch(self, flag):
        if flag == 1:
            self.fgen.ch2.set_output("ON")
        else:
            self.fgen.ch2.set_output("OFF")

    # connect the oscilloscope
    def osc_connect(self):
        self.osc.connect()

    def setFunGen(self, waveShape: int, amplitude, frequency, modulation: int):
        self.fgen.ch1.set_AM(modulation)
        self.fgen_ch2_switch(0)
        if waveShape == 0:
            self.fgen.ch1.set_function("SIN")
        elif waveShape == 1:
            self.fgen.ch1.set_function("SQU")
        elif waveShape == 2:
            self.fgen.ch1.set_function("RAMP")
        elif waveShape == 3:
            self.fgen.ch1.set_function("PULS")
        self.fgen.ch1.set_frequency(frequency, unit="Hz")
        self.fgen.ch1.set_offset(0)
        self.fgen.ch1.set_amplitude(amplitude)
        self.fgen_ch1_switch(1)

    # for the draw waveform experiment
    def waveform(self, waveShape: int, amplitude, frequency, modulation: int):
        self.fgen.ch1.set_AM(modulation)
        self.fgen_ch2_switch(0)
        if waveShape == 0:
            self.fgen.ch1.set_function("SIN")
        elif waveShape == 1:
            self.fgen.ch1.set_function("SQU")
        elif waveShape == 2:
            self.fgen.ch1.set_function("RAMP")
        elif waveShape == 3:
            self.fgen.ch1.set_function("PULS")
        self.fgen.ch1.set_function("SIN")
        self.fgen.ch1.set_frequency(frequency, unit="Hz")
        self.fgen.ch1.set_offset(0)
        self.fgen.ch1.set_amplitude(amplitude)
        self.fgen_ch1_switch(1)
        time.sleep(1)
        # self.osc.capture_DC()
        self.osc.analyze_waveform()

    # for the fgen_osc experiment
    def draw_Vgen_Vosc_chart(self, interval, frequency, data_volume, wait_time, lower_limit, upper_limit):
        self.fgen_osc_done = 0
        self.fgen_ch2_switch(0)
        self.fgen.ch1.set_function("SIN")
        self.fgen.ch1.set_frequency(frequency, unit="Hz")
        self.fgen.ch1.set_offset(0)
        self.fgen.ch1.set_amplitude(0.5)
        self.fgen_ch1_switch(1)
        # self.osc.capture_DC()
        i = 0
        self.Vgen = []
        self.Vosc = [[], [], [], [], [], []]
        if lower_limit < 0.002:
            lower_limit = 0.002
        if upper_limit > 20:
            upper_limit = 20
        for amplitude_vpp in np.arange(lower_limit, upper_limit, interval):
            while self.pause == 1:
                time.sleep(1)
            print('pause: ', self.pause)
            self.fgen.ch1.set_amplitude(amplitude_vpp)
            # wait for the function generator to set
            time.sleep(wait_time)
            # self.osc.capture_DC()
            cur = []
            self.Vgen.append(amplitude_vpp)
            for i in range(data_volume):
                value = self.osc.measure_DC_Vrms()
                # wait for the scope to set
                time.sleep(0.1)
                self.Vosc[i].append(value)
                cur.append(value)
            if data_volume > 1:
                result = self.IQR(cur)  # remove the outliers
            else:
                result = cur
            avg = np.mean(result)
            self.Vosc[data_volume].append(avg)
        amplitude_vpp = upper_limit
        while self.pause == 1:
            time.sleep(1)
        print('pause: ', self.pause)
        self.fgen.ch1.set_amplitude(amplitude_vpp)
        # wait for the function generator to set
        time.sleep(1)
        # self.osc.capture_DC()
        cur = []
        self.Vgen.append(amplitude_vpp)
        for i in range(data_volume):
            value = self.osc.measure_DC_Vrms()
            # wait for the scope to set
            time.sleep(0.5)
            self.Vosc[i].append(value)
            cur.append(value)
        if data_volume > 1:
            result = self.IQR(cur)  # remove the outliers
        else:
            result = cur
        avg = np.mean(result)
        self.Vosc[data_volume].append(avg)
        print(self.Vgen)
        print(self.Vosc)
        dataframe_format = {'fgen': self.Vgen}
        for num in range(data_volume):
            dataframe_format.update({f'Vosc_{num}': self.Vosc[num]})
        dataframe_format.update({'Average': self.Vosc[data_volume]})
        vgen_vosc_dataframe = pd.DataFrame(
            # {'fgen': self.Vgen, 'Vosc_0': self.Vosc[0], 'Vosc_1': self.Vosc[1], 'Vosc_2': self.Vosc[2],
            #  'Vosc_3': self.Vosc[3], 'Vosc_4': self.Vosc[4], 'Average': self.Vosc[5]}
            # {'fgen': Vgen, 'Vosc_0': Vosc[0], 'Vosc_1': Vosc[1], 'Vosc_2': Vosc[2]}
            dataframe_format
        )
        vgen_vosc_dataframe.to_csv('data/fgen_osc_data.csv', index=True, sep=',')
        # f = open("data/fgen_osc_data.csv", "w")
        # for i in range(0, len(Vgen) - 1):
        #     f.write("%f, %f\n" % (Vgen[i], Vosc[0][i]))
        # f.close()
        self.fgen_osc_result = np.array([self.Vgen, self.Vosc[data_volume]])
        self.fgen_osc_done = 1

    def auto_angle_osc(self, interval, amplitude, frequency, data_volume, wait_time, lower_limit, upper_limit):
        self.angle_osc_done = 0
        self.fgen_ch2_switch(0)
        self.fgen.ch1.set_function("SIN")
        self.fgen.ch1.set_frequency(frequency, unit="Hz")
        self.fgen.ch1.set_offset(0)
        self.fgen.ch1.set_amplitude(amplitude)
        self.fgen_ch1_switch(1)
        self.angle = []
        self.angle_Vosc = [[], [], [], [], [], []]
        angle_degree = 0
        for angle_degree in np.arange(lower_limit, upper_limit, interval):
            while self.pause == 1:
                time.sleep(1)
            print('pause: ', self.pause)
            # self.fgen.ch1.set_amplitude(amplitude_vpp)
            if int(angle_degree) == int(lower_limit):
                self.rotate(str(int(lower_limit)))
            else:
                self.rotate(str(int(interval)))
            # wait for the function generator to set
            time.sleep(wait_time)
            # self.osc.capture_DC()
            cur = []
            self.angle.append(angle_degree)
            for i in range(data_volume):
                value = self.osc.measure_DC_Vrms()
                # wait for the scope to set
                time.sleep(0.5)
                self.angle_Vosc[i].append(value)
                cur.append(value)
            if data_volume > 1:
                result = self.IQR(cur)  # remove the outliers
            else:
                result = cur
            avg = np.mean(result)
            self.angle_Vosc[data_volume].append(avg)
        while self.pause == 1:
            time.sleep(1)
        print('pause: ', self.pause)
        # self.fgen.ch1.set_amplitude(amplitude_vpp)
        self.rotate(str(int(upper_limit - angle_degree)))
        # wait for the function generator to set
        time.sleep(wait_time)
        # self.osc.capture_DC()
        cur = []
        self.angle.append(upper_limit)
        for i in range(data_volume):
            value = self.osc.measure_DC_Vrms()
            # wait for the scope to set
            time.sleep(0.5)
            self.angle_Vosc[i].append(value)
            cur.append(value)
        if data_volume > 1:
            result = self.IQR(cur)  # remove the outliers
        else:
            result = cur
        avg = np.mean(result)
        self.angle_Vosc[data_volume].append(avg)
        print(self.angle)
        print(self.angle_Vosc)
        dataframe_format = {'angle': self.angle}
        for num in range(data_volume):
            dataframe_format.update({f'Vosc_{num}': self.angle_Vosc[num]})
        dataframe_format.update({'Average': self.angle_Vosc[data_volume]})
        vgen_vosc_dataframe = pd.DataFrame(
            # {'fgen': self.Vgen, 'Vosc_0': self.Vosc[0], 'Vosc_1': self.Vosc[1], 'Vosc_2': self.Vosc[2],
            #  'Vosc_3': self.Vosc[3], 'Vosc_4': self.Vosc[4], 'Average': self.Vosc[5]}
            # {'fgen': Vgen, 'Vosc_0': Vosc[0], 'Vosc_1': Vosc[1], 'Vosc_2': Vosc[2]}
            dataframe_format
        )
        vgen_vosc_dataframe.to_csv('data/angle_osc_data.csv', index=True, sep=',')
        # f = open("data/fgen_osc_data.csv", "w")
        # for i in range(0, len(Vgen) - 1):
        #     f.write("%f, %f\n" % (Vgen[i], Vosc[0][i]))
        # f.close()
        self.angle_osc_result = np.array([self.angle, self.angle_Vosc[data_volume]])
        self.angle_osc_done = 1



    def run_square(self, amplitude, frquency, modulation: int):
        self.fgen_ch2_switch(0)
        self.fgen.ch1.set_function("SIN")
        self.fgen.ch1.set_frequency(frquency, unit="Hz")
        self.fgen.ch1.set_offset(0)
        self.fgen.ch1.set_amplitude(amplitude)
        self.fgen.ch1.set_AM(modulation)

    def run_triangle(self, amplitude, frquency, modulation: int):
        self.fgen_ch2_switch(0)
        self.fgen.ch1.set_function("RAMP")
        self.fgen.ch1.set_frequency(frquency, unit="Hz")
        self.fgen.ch1.set_offset(0)
        self.fgen.ch1.set_amplitude(amplitude)
        self.fgen.ch1.set_AM(modulation)

    def run_angle_osc(self):
        if self.angle_flag == 1:
            dataFrame = pd.DataFrame({'angle': self.angle, 'Vosc_0': self.angle_Vosc[0], 'Vosc_1': self.angle_Vosc[1],
                                      'Vosc_2': self.angle_Vosc[2], 'Vosc_3': self.angle_Vosc[3],
                                      'Vosc_4': self.angle_Vosc[4], 'Average': self.angle_Vosc[5]})
            dataFrame.to_csv('data/angle_osc_data.csv', index=True, sep=',')
            return np.array([self.angle, self.angle_Vosc[5]])

    def add_data(self, angle):
        if self.angle_flag == 0:
            self.angle = []
            self.angle_Vosc = [[], [], [], [], [], []]
            self.angle_flag = 1
            self.angle.append(angle)
            cur = []
            for i in range(5):
                value = self.osc.measure_DC_Vrms()
                # wait for the scope to set
                time.sleep(0.5)
                self.angle_Vosc[i].append(value)
                cur.append(value)
            result = self.IQR(cur)  # remove the outliers
            avg = np.mean(result)
            self.angle_Vosc[5].append(avg)
        else:
            self.angle.append(angle)
            cur = []
            for i in range(5):
                value = self.osc.measure_DC_Vrms()
                # wait for the scope to set
                time.sleep(0.5)
                self.angle_Vosc[i].append(value)
                cur.append(value)
            result = self.IQR(cur)  # remove the outliers
            avg = np.mean(result)
            self.angle_Vosc[5].append(avg)

    def reset_data(self):
        self.angle_flag = 0

    def capture(self):
        # self.osc.capture_DC()
        self.osc.analyze_waveform()

    def IQR(self, numbers):
        numbers = sorted(numbers)
        result = quantiles(numbers)
        IQR = result[2] - result[0]
        lower_bound = result[0] - 0.3 * IQR
        upper_bound = result[2] + 0.3 * IQR
        return [n for n in numbers if lower_bound <= n <= upper_bound]

    def rising_time(self):
        df = pd.read_csv('data/waveform_data.csv')

        # Pre-process the waveform data
        data = np.array(df.iloc[:, 1])
        print('mean data: ', np.mean(data))
        data = data - np.mean(data)
        data = data[:24800]
        N = 50
        # downsample the data
        data = np.mean(data.reshape(-1, N), axis=1)

        # Calculate the derivative of the waveform
        derivative = np.gradient(data)

        # Define the threshold value
        threshold = np.std(derivative)
        print('threshold: ', threshold)

        # Identify the start time of the rising edge
        start_time = None
        for i, value in enumerate(derivative):
            if value > threshold and start_time is None:
                start_time = i
                break
        print('start time: ', start_time)

        # Find the end time of the rising edge
        end_time = None
        stable_flag = 0
        for i, value in enumerate(derivative[start_time:]):
            if -threshold / 10 < value < threshold / 10:
                end_time = start_time + i
                for j, value2 in enumerate(derivative[end_time:end_time + 10]):
                    if -threshold / 10 < value2 < threshold / 10:
                        stable_flag = 1
                    else:
                        stable_flag = 0
                        break
                if stable_flag == 1:
                    break

        print('end time: ', end_time)

        # Calculate the rising time
        rising_time = (end_time - start_time) * 50 / 12500
        print('rising time: ', rising_time, 's')
        return rising_time

    def rotate(self, angle: str):
        try:
            self.serial_sender.send(angle)
            print(self.serial_sender.receive())
            # self.serial_sender.close()
        except SerialException:
            print(SerialException)
