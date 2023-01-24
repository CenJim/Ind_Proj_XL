from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QComboBox, QLineEdit


class Widget_top_left(QWidget):

    def __init__(self):
        super().__init__()

        self.grid = QVBoxLayout()
        self.subgrid = QGridLayout()
        self.amplitude = 0.0     # default value is 0 V
        self.frequency = 1000.0  # default value is 1000 Hz
        self.interval = 1.0      # default value
        self.mode = 1            # default mode is the first mode
        self.modulation = 0      # default modulation mode is off

        self.initUI()

    def initUI(self):
        # title
        title = QLabel('Working Mode Set')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # five settings
        mode = QLabel('Mode:')
        amplitude = QLabel('Amplitude (Volts):')
        frequency = QLabel('Frequency (Hz):')
        interval = QLabel('Interval (Volts):')
        modulation = QLabel('Modulation:')

        # text input for voltage setting
        qle_amplitude = QLineEdit(self)
        qle_amplitude.textChanged[str].connect(self.amplitudeChanged)
        qle_amplitude.setMaximumWidth(self.width() * 0.2)

        # text input for frequency setting
        qle_frequency = QLineEdit(self)
        qle_frequency.textChanged[str].connect(self.frequencyChanged)
        qle_frequency.setMaximumWidth(self.width() * 0.2)

        # Drop down menu for mode setting
        combo_mode = QComboBox(self)
        combo_mode.addItem('Waveform')
        combo_mode.addItem('Draw Fgen-Osc')
        combo_mode.addItem('Square 1Hz')
        combo_mode.addItem('Triangle 1Hz')
        combo_mode.textActivated[str].connect(self.modeSelected)

        # Text input for interval setting
        qle_interval = QLineEdit(self)
        qle_interval.textChanged[str].connect(self.intervalChanged)
        qle_interval.setMaximumWidth(self.width() * 0.2)

        # Drop down menu for modulation setting
        combo_modulation = QComboBox(self)
        combo_modulation.addItem('Off')
        combo_modulation.addItem('1 kHz')
        combo_modulation.addItem('2 kHz')
        combo_modulation.addItem('3 kHz')
        combo_modulation.textActivated[str].connect(self.modulationSelected)

        self.grid.setSpacing(10)
        self.grid.addWidget(title)
        self.grid.addLayout(self.subgrid)
        self.subgrid.addWidget(mode, 0, 0)
        self.subgrid.addWidget(combo_mode, 0, 1)
        self.subgrid.addWidget(amplitude, 1, 0)
        self.subgrid.addWidget(qle_amplitude, 1, 1)
        self.subgrid.addWidget(frequency, 2, 0)
        self.subgrid.addWidget(qle_frequency, 2, 1)
        self.subgrid.addWidget(interval, 3, 0)
        self.subgrid.addWidget(qle_interval, 3, 1)
        self.subgrid.addWidget(modulation, 4, 0)
        self.subgrid.addWidget(combo_modulation, 4, 1)

        self.setLayout(self.grid)

    # Functions executed when a mode is selected
    def modeSelected(self, text):
        if text == 'Waveform':
            self.mode = 1
        elif text == 'Draw Fgen-Osc':
            self.mode = 2
        elif text == 'Square 1Hz':
            self.mode = 3
        elif text == 'Triangle 1Hz':
            self.mode = 4

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
        elif text == '1 kHz':
            self.modulation = 1
        elif text == '2 kHz':
            self.modulation = 3
        elif text == '3 kHz':
            self.modulation = 4