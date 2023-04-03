import glob
import sys

import serial
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QApplication
from pyvisa import ResourceManager
from qt_material import apply_stylesheet
import Dsox2002a as ds
import Handler as hl
import tektronix_func_gen as tfg
from UIQt import mainWindow, mainWindowTest


class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        self.osc_address = ''
        self.fgen_address = ''
        self.rasp_address = ''

        self.osc_label = QLabel('Oscilloscope:')
        self.fgen_label = QLabel('Function Generator:')
        self.rasp_label = QLabel('Raspberry Pi Pico:')
        self.osc_combo = QComboBox()
        self.fgen_combo = QComboBox()
        self.rasp_combo = QComboBox()
        self.enter_button = QPushButton('Enter')
        self.cancel_button = QPushButton('Cancel')
        self.refresh_button = QPushButton('Refresh')

        self.main_layout = QGridLayout()
        self.top_widget = QWidget()
        self.top_layout = QGridLayout()
        self.bottom_widget = QWidget()
        self.bottom_layout = QGridLayout()

        self.initUI()
        self.resize(600, 300)

    def initUI(self):
        # set the sub-layout
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.top_widget, 0, 0)
        self.main_layout.addWidget(self.bottom_widget, 1, 0)
        self.top_widget.setLayout(self.top_layout)
        self.bottom_widget.setLayout(self.bottom_layout)

        # set the refresh button
        self.refresh_button.clicked.connect(self.refresh_resource_list)

        # set the cancel button
        self.cancel_button.clicked.connect(self.close)

        # set the enter button
        self.enter_button.clicked.connect(self.launch)

        # set the osc combo box
        self.osc_combo.textActivated[str].connect(self.osc_select)
        self.osc_combo.setMinimumWidth(350)

        # set the fgen combo box
        self.fgen_combo.textActivated[str].connect(self.fgen_select)
        self.fgen_combo.setMinimumWidth(350)

        # set the raspberry pi pico combo box
        self.rasp_combo.textActivated[str].connect(self.rasp_select)
        self.rasp_combo.setMaximumWidth(350)

        # set the raspberry pi pico combo boc
        self.rasp_combo.addItem('None')

        # get all the resource
        self.refresh_resource_list()

        # set all the widgets
        self.top_layout.addWidget(self.osc_label, 0, 0)
        self.top_layout.addWidget(self.osc_combo, 0, 1)
        self.top_layout.addWidget(self.fgen_label, 1, 0)
        self.top_layout.addWidget(self.fgen_combo, 1, 1)
        self.top_layout.addWidget(self.rasp_label, 2, 0)
        self.top_layout.addWidget(self.rasp_combo, 2, 1)
        self.bottom_layout.addWidget(self.cancel_button, 0, 0)
        self.bottom_layout.addWidget(self.refresh_button, 0, 1)
        self.bottom_layout.addWidget(self.enter_button, 0, 2)

        # set the stretch
        self.top_layout.setColumnStretch(self.top_layout.columnCount(), 0)

    def getResoureList(self):
        resource = str(ResourceManager().list_resources())
        resource = resource.split("'")
        result = []
        for item in resource:
            if len(item) > 10:
                result.append(item)
        return result

    def refresh_resource_list(self):
        self.osc_combo.clear()
        self.fgen_combo.clear()
        self.rasp_combo.clear()
        self.rasp_combo.addItem('None')
        visa_resource_list = self.getResoureList()
        com_resource_list = self.serial_ports()
        for item in visa_resource_list:
            self.osc_combo.addItem(item)
            self.fgen_combo.addItem(item)
        for item in com_resource_list:
            self.rasp_combo.addItem(item)

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/cu.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def osc_select(self, text):
        self.osc_address = text

    def fgen_select(self, text):
        self.fgen_address = text

    def rasp_select(self, text):
        self.rasp_address = text

    def launch(self):
        handler = hl.Handler(ds.Dsox2002a(ResourceManager(), self.osc_address),
                             tfg.FuncGen(self.fgen_address), self.rasp_address)
        mainWindow(handler)
        self.close()


def launcher():
    app = QApplication(sys.argv)
    launcher = Launcher()
    apply_stylesheet(app, theme='dark_teal.xml')
    launcher.show()
    sys.exit(app.exec())
