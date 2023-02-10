from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QComboBox, QLineEdit, QHBoxLayout, QPushButton


class Widget_top_left(QWidget):

    def __init__(self):
        super().__init__()

        # title
        self.title = QLabel('Working Mode Set')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")

        self.grid = QVBoxLayout()
        self.subgridUp = QHBoxLayout()
        self.subgrid = QGridLayout()
        self.amplitude = 0.0  # default value is 0 V
        self.frequency = 1000.0  # default value is 1000 Hz
        self.interval = 1.0  # default value
        self.mode = 1  # default mode is the first mode
        self.modulation = 0  # default modulation mode is off
        self.waveShape = 0  # default waveShape is sin shape
        self.angle = 0 # default angle is 0

        self.initUI()

    def initUI(self):
        # five settings
        mode = QLabel('Mode:')
        shape = QLabel('Wave Shape:')
        amplitude = QLabel('Amplitude (Vpp):')
        frequency = QLabel('Frequency (Hz):')
        interval = QLabel('Interval (Volts):')
        modulation = QLabel('Amplitude Modulation:')
        angle = QLabel('Angle:')

        # text input for voltage setting
        qle_amplitude = QLineEdit(self)
        qle_amplitude.textChanged[str].connect(self.amplitudeChanged)
        qle_amplitude.setMaximumWidth(self.width() * 0.27)
        qle_amplitude.setMaximumHeight(self.height() * 0.05)

        # text input for frequency setting
        qle_frequency = QLineEdit("1000", self)
        qle_frequency.textChanged[str].connect(self.frequencyChanged)
        qle_frequency.setMaximumWidth(self.width() * 0.27)
        qle_frequency.setMaximumHeight(self.height() * 0.05)

        # Drop down menu for mode setting
        combo_mode = QComboBox(self)
        combo_mode.addItem('Waveform')
        combo_mode.addItem('Draw Fgen-Osc')
        combo_mode.addItem('Draw Angle-Osc')
        combo_mode.addItem('Square Waveform')
        combo_mode.addItem('Triangle Waveform')
        combo_mode.textActivated[str].connect(self.modeSelected)
        combo_mode.setMaximumWidth(self.width() * 0.27)
        combo_mode.setMaximumHeight(self.height() * 0.05)

        # Drop down menu for wave shape selection
        combo_shape = QComboBox(self)
        combo_shape.addItem('Sine')
        combo_shape.addItem('Square')
        combo_shape.addItem('Ramp')
        combo_shape.addItem('Pulse')
        combo_shape.textActivated[str].connect(self.shapeSelected)
        combo_shape.setMaximumWidth(self.width() * 0.27)
        combo_shape.setMaximumHeight(self.height() * 0.05)

        # Text input for interval setting
        qle_interval = QLineEdit(self)
        qle_interval.textChanged[str].connect(self.intervalChanged)
        qle_interval.setMaximumWidth(self.width() * 0.27)
        qle_interval.setMaximumHeight(self.height() * 0.05)

        # Drop down menu for modulation setting
        combo_modulation = QComboBox(self)
        combo_modulation.addItem('Off')
        combo_modulation.addItem('On')
        combo_modulation.textActivated[str].connect(self.modulationSelected)
        combo_modulation.setMaximumWidth(self.width() * 0.27)
        combo_modulation.setMaximumHeight(self.height() * 0.05)

        # Text input for angle setting
        qle_angle = QLineEdit(self)
        qle_angle.textChanged[str].connect(self.angleChanged)
        qle_angle.setMaximumWidth(self.width() * 0.27)
        qle_angle.setMaximumHeight(self.height() * 0.05)

        self.grid.setSpacing(10)
        self.grid.addLayout(self.subgridUp)
        self.subgridUp.addWidget(self.title)
        self.grid.addLayout(self.subgrid)
        self.subgrid.addWidget(mode, 0, 0)
        self.subgrid.addWidget(combo_mode, 0, 1)
        self.subgrid.addWidget(shape, 1, 0)
        self.subgrid.addWidget(combo_shape, 1, 1)
        self.subgrid.addWidget(amplitude, 2, 0)
        self.subgrid.addWidget(qle_amplitude, 2, 1)
        self.subgrid.addWidget(frequency, 3, 0)
        self.subgrid.addWidget(qle_frequency, 3, 1)
        self.subgrid.addWidget(interval, 4, 0)
        self.subgrid.addWidget(qle_interval, 4, 1)
        self.subgrid.addWidget(modulation, 5, 0)
        self.subgrid.addWidget(combo_modulation, 5, 1)
        self.subgrid.addWidget(angle, 6, 0)
        self.subgrid.addWidget(qle_angle, 6, 1)
        self.grid.addStretch(1)

        self.setLayout(self.grid)

    # Functions executed when a mode is selected
    def modeSelected(self, text):
        if text == 'Waveform':
            self.mode = 1
        elif text == 'Draw Fgen-Osc':
            self.mode = 2
        elif text == 'Square Waveform':
            self.mode = 3
        elif text == 'Triangle Waveform':
            self.mode = 4
        elif text == 'Draw Angle-Osc':
            self.mode = 5

    def intervalChanged(self, text):
        try:
            self.interval = float(text)
        except Exception as ex:
            print('interval is not a float')

    def amplitudeChanged(self, text):
        try:
            self.amplitude = float(text)
        except Exception as ex:
            print('amplitude is not a float')

    def frequencyChanged(self, text):
        try:
            self.frequency = float(text)
        except Exception as ex:
            print('frequency is not a float')

    def modulationSelected(self, text):
        if text == 'Off':
            self.modulation = 0
        elif text == 'On':
            self.modulation = 1

    def shapeSelected(self, text):
        if text == 'Sine':
            self.waveShape = 0
        elif text == 'Square':
            self.waveShape = 1
        elif text == 'Ramp':
            self.waveShape = 2
        elif text == 'Pulse':
            self.waveShape = 3

    def angleChanged(self, text):
        try:
            self.angle = float(text)
        except Exception as ex:
            print('angle is not a float')

