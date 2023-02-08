import pyvisa
import Dsox2002a as ds
import Handler as hl
import tektronix_func_gen as tfg
from UIQt import mainWindow, mainWindowTest


def getResoureList():
    resource = str(pyvisa.ResourceManager().list_resources())
    resource = resource.split("'")
    result = []
    for item in resource:
        if len(item) > 10:
            result.append(item)
    return result


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

print(getResoureList())
handler = hl.Handler(ds.Dsox2002a(pyvisa.ResourceManager(), 'USB0::0x0957::0x179B::MY51250763::INSTR'),
                     tfg.FuncGen('USB0::0x0699::0x0353::1511379::INSTR'))

# handler.osc_connect()
# handler.draw_Vgen_Vosc_chart(1)

mainWindow(handler)
# mainWindowTest()
