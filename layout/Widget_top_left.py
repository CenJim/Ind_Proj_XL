from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QComboBox, QLineEdit, QHBoxLayout, QPushButton, \
    QFrame


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
        self.angle = 0  # default angle is 0
        self.data_volume = 5
        self.wait_time = 5
        self.fgen_osc_lower_limit = 0.1
        self.fgen_osc_upper_limit = 20

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
        data_volume = QLabel('Data Volume (0~5):')
        wait_time = QLabel('Wait Time:')
        fgen_osc_range = QLabel('Range:')

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

        # Text input for data_volume setting
        qle_data_volume = QLineEdit(self)
        qle_data_volume.textChanged[str].connect(self.dataVolumeChanged)
        qle_data_volume.setMaximumWidth(self.width() * 0.27)
        qle_data_volume.setMaximumHeight(self.height() * 0.05)

        # Text input for wait_time setting
        qle_wait_time = QLineEdit(self)
        qle_wait_time.textChanged[str].connect(self.waitTimeChanged)
        qle_wait_time.setMaximumWidth(self.width() * 0.27)
        qle_wait_time.setMaximumHeight(self.height() * 0.05)

        # a fgen_osc labeled range input for range setting
        widget_fgen_osc_range = QWidget()
        range_fgen_osc_range_layout = QHBoxLayout()
        widget_fgen_osc_range.setLayout(range_fgen_osc_range_layout)
        range_fgen_osc_range_layout.setContentsMargins(1, 0, 1, 0)
        qle_fgen_osc_lower = QLineEdit()
        qle_fgen_osc_upper = QLineEdit()
        qle_fgen_osc_lower.setMinimumWidth(self.width() * 0.1)
        qle_fgen_osc_upper.setMinimumWidth(self.width() * 0.1)
        qle_fgen_osc_lower.setMaximumHeight(self.height() * 0.05)
        qle_fgen_osc_upper.setMaximumHeight(self.height() * 0.05)
        widget_fgen_osc_range.setMaximumWidth(self.width() * 0.27)
        widget_fgen_osc_range.setMaximumHeight(self.height() * 0.06)
        range_fgen_osc_range_layout.addWidget(qle_fgen_osc_lower)
        range_fgen_osc_range_layout.addStretch()
        range_fgen_osc_range_layout.addWidget(qle_fgen_osc_upper)
        qle_fgen_osc_lower.textChanged[str].connect(self.fgenOscLowerChanged)
        qle_fgen_osc_upper.textChanged[str].connect(self.fgenOscUpperChanged)

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
        self.subgrid.addWidget(data_volume, 5, 0)
        self.subgrid.addWidget(qle_data_volume, 5, 1)
        self.subgrid.addWidget(wait_time, 6, 0)
        self.subgrid.addWidget(qle_wait_time, 6, 1)
        self.subgrid.addWidget(fgen_osc_range, 7, 0)
        self.subgrid.addWidget(widget_fgen_osc_range, 7, 1)
        self.subgrid.addWidget(modulation, 8, 0)
        self.subgrid.addWidget(combo_modulation, 8, 1)
        self.subgrid.addWidget(angle, 9, 0)
        self.subgrid.addWidget(qle_angle, 9, 1)
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
            print('interval is not a float', ex)

    def waitTimeChanged(self, text):
        try:
            self.wait_time = float(text)
        except Exception as ex:
            print('wait time is not a float', ex)

    def fgenOscLowerChanged(self, text):
        try:
            if float(text) < 0.1 or float(text) >= 20:
                print('Lower limit value should between 0.1 and 20')
            else:
                self.fgen_osc_lower_limit = float(text)
        except Exception as ex:
            print(ex)

    def fgenOscUpperChanged(self, text):
        try:
            if float(text) < 0.1 or float(text) >= 20:
                print('Upper limit value should between 0.1 and 20')
            else:
                self.fgen_osc_upper_limit = float(text)
        except Exception as ex:
            print(ex)

    def dataVolumeChanged(self, text):
        try:
            if 1 <= int(text) <= 5:
                self.data_volume = int(text)
            else:
                print('data volume is not between 1 and 5')
        except Exception as ex:
            print('data volume is not a int', ex)

    def amplitudeChanged(self, text):
        try:
            self.amplitude = float(text)
        except Exception as ex:
            print('amplitude is not a float', ex)

    def frequencyChanged(self, text):
        try:
            self.frequency = float(text)
        except Exception as ex:
            print('frequency is not a float', ex)

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


QSS = """
QSlider {
    min-height: 20px;
}
QSlider::groove:horizontal {
    border: 0px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #888, stop:1 #ddd);
    height: 20px;
    border-radius: 10px;
}
QSlider::handle {
    background: qradialgradient(cx:0, cy:0, radius: 1.2, fx:0.35,
                                fy:0.3, stop:0 #eef, stop:1 #002);
    height: 20px;
    width: 20px;
    border-radius: 10px;
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #227, stop:1 #77a);
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
}
QRangeSlider {
    qproperty-barColor: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #227, stop:1 #77a);
}
"""
