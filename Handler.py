import time

import numpy as np


class Handler:
    def __init__(self, osc, fgen):
        self.osc = osc
        self.fgen = fgen

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

    # for the draw waveform experiment
    def waveform(self, amplitude, frquency):
        self.fgen_ch2_switch(0)
        self.fgen.ch1.set_function("SIN")
        self.fgen.ch1.set_frequency(frquency, unit="Hz")
        self.fgen.ch1.set_offset(0)
        self.fgen.ch1.set_amplitude(amplitude)
        self.fgen_ch1_switch(1)
        self.osc.analyze_waveform()

    # for the fgen_osc experiment
    def draw_Vgen_Vosc_chart(self, interval):
        self.fgen_ch2_switch(0)
        self.fgen.ch1.set_function("SIN")
        self.fgen.ch1.set_frequency(1000, unit="Hz")
        self.fgen.ch1.set_offset(0)
        self.fgen.ch1.set_amplitude(0.5)
        self.fgen_ch1_switch(1)
        self.osc.capture_DC()
        i = 0
        Vgen = []
        Vosc = []
        for amplitude_vpp in np.arange(0.5, 20, interval):
            self.fgen.ch1.set_amplitude(amplitude_vpp)
            # wait for the function generator to set
            time.sleep(2)
            Vosc.append(self.osc.measure_DC_Vrms())
            # wait for the scope to set
            time.sleep(2)
            Vgen.append(amplitude_vpp)
        print(Vgen)
        print(Vosc)
        return np.array([Vgen, Vosc])
