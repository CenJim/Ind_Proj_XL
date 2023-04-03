from Launcher import launcher

"""
print(getResoureList())


# Oscilloscope

dsox = ds.Dsox2002a(pyvisa.ResourceManager(), 'USB0::0x0957::0x179B::MY55442396::INSTR')
dsox.connect()
print(dsox.queryIDN())
# msox.reset()

print(dsox.queryOPT())
# msox.autoScale()
print(dsox.queryChannelStatus())
dsox.capture_DC()
dsox.measure_DC_Vrms()
# dsox.analyze_waveform()
# dsox.disconnect()


# function generator
import tektronix_func_gen as tfg

# basic control
with tfg.FuncGen('USB0::0x0699::0x0353::1516608::INSTR') as fgen:
    fgen.ch1.set_function("SIN")
    fgen.ch1.set_frequency(25, unit="Hz")
    fgen.ch1.set_offset(0)
    fgen.ch1.set_amplitude(2)
    fgen.ch1.set_output("ON")
    fgen.ch2.set_output("OFF")
    # alternatively fgen.ch1.print_settings() to show from one channel only
    fgen.print_settings()
"""
if __name__ == '__main__':
    launcher()

# handler = hl.Handler(ds.Dsox2002a(pyvisa.ResourceManager(), 'USB0::0x0957::0x179B::MY55442396::INSTR'),
#                      tfg.FuncGen('USB0::0x0699::0x0353::1516608::INSTR'))
#
# mainWindow(handler)
# mainWindowTest()
