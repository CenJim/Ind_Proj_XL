import time
from statistics import quantiles

import numpy as np
import pandas as pd


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
    def draw_Vgen_Vosc_chart(self, interval, frequency):
        self.fgen_ch2_switch(0)
        self.fgen.ch1.set_function("SIN")
        self.fgen.ch1.set_frequency(frequency, unit="Hz")
        self.fgen.ch1.set_offset(0)
        self.fgen.ch1.set_amplitude(0.5)
        self.fgen_ch1_switch(1)
        # self.osc.capture_DC()
        i = 0
        Vgen = []
        Vosc = [[], [], [], [], [], []]
        for amplitude_vpp in np.arange(0.5, 20, interval):
            self.fgen.ch1.set_amplitude(amplitude_vpp)
            # wait for the function generator to set
            time.sleep(0.5)
            # self.osc.capture_DC()
            cur = []
            for i in range(5):
                value = self.osc.measure_DC_Vrms()
                # wait for the scope to set
                time.sleep(0.5)
                Vosc[i].append(value)
                cur.append(value)
            result = self.IQR(cur)  # remove the outliers
            avg = np.mean(result)
            Vosc[5].append(avg)
            Vgen.append(amplitude_vpp)
        print(Vgen)
        print(Vosc)
        dataFrame = pd.DataFrame(
            {'fgen': Vgen, 'Vosc_0': Vosc[0], 'Vosc_1': Vosc[1], 'Vosc_2': Vosc[2], 'Vosc_3': Vosc[3],
             'Vosc_4': Vosc[4], 'Average': Vosc[5]})
        dataFrame.to_csv('data/fgen_osc_data.csv', index=True, sep=',')
        # f = open("data/fgen_osc_data.csv", "w")
        # for i in range(0, len(Vgen) - 1):
        #     f.write("%f, %f\n" % (Vgen[i], Vosc[0][i]))
        # f.close()
        return np.array([Vgen, Vosc[5]])

    def run_square(self, amplitude, frquency, modulation: int):
        self.fgen_ch2_switch(0)
        self.fgen.ch1.set_function("SQU")
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

    def capture(self):
        self.osc.capture_DC()
        self.osc.analyze_waveform()

    def three_sigma(self, ser1):
        # 求平均值
        mean_value = ser1.mean()
        # 求标准差
        std_value = ser1.std()
        # 位于(μ-3σ,μ+3σ)区间的数据是正常的，不在这个区间的数据为异常的
        # ser1中的数值小于μ-3σ或大于μ+3σ均为异常值
        min = mean_value - 3 * std_value
        max = mean_value + 3 * std_value
        outrange = []
        for i in ser1:
            if (i > max) or (i < min):
                outrange.append(i)
        return outrange

    def IQR(self, numbers):
        numbers = sorted(numbers)
        result = quantiles(numbers)
        IQR = result[2] - result[0]
        lower_bound = result[0] - 0.3 * IQR
        upper_bound = result[2] + 0.3 * IQR
        return [n for n in numbers if lower_bound <= n <= upper_bound]