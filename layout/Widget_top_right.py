from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QFrame


class Widget_top_right(QWidget):

    def __init__(self):
        super().__init__()

        self.grid = QVBoxLayout()
        self.subgrid = QGridLayout()

        self.title = QLabel('Data')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.response = QLabel('Response Time (ms):')
        self.angle = QLabel('Angle of cell (radian):')
        self.dcvrms = QLabel('DCVrms (V):')
        self.vpp = QLabel('Vpp (V):')
        self.vmax = QLabel('Vmax (V):')
        self.frequency = QLabel('Frequency (Hz):')
        self.period = QLabel('Period (ms):')

        self.response_value = QLabel()
        self.angle_value = QLabel()
        self.dcvrms_value = QLabel()
        self.vpp_value = QLabel()
        self.vmax_value = QLabel()
        self.frequency_value = QLabel()
        self.period_value = QLabel()

        self.initUI()

    def initUI(self):
        # response_value style
        self.response_value.setStyleSheet("background-color: #232629; border: 1px inset #232629; min-height: 20px;")
        self.response_value.setMaximumWidth(self.width() * 0.2)
        # angle_value style
        self.angle_value.setStyleSheet("background-color: #232629; border: 1px inset #232629; min-height: 20px;")
        self.angle_value.setMaximumWidth(self.width() * 0.2)
        # dcvrms_value style
        self.dcvrms_value.setStyleSheet("background-color: #232629; border: 1px inset #232629; min-height: 20px;")
        self.dcvrms_value.setMaximumWidth(self.width() * 0.2)
        # vpp_value style
        self.vpp_value.setStyleSheet("background-color: #232629; border: 1px inset #232629; min-height: 20px;")
        self.vpp_value.setMaximumWidth(self.width() * 0.2)
        # vmax_value style
        self.vmax_value.setStyleSheet("background-color: #232629; border: 1px inset #232629; min-height: 20px;")
        self.vmax_value.setMaximumWidth(self.width() * 0.2)
        # frequency_value style
        self.frequency_value.setStyleSheet("background-color: #232629; border: 1px inset #232629; min-height: 20px;")
        self.frequency_value.setMaximumWidth(self.width() * 0.2)
        # period_value style
        self.period_value.setStyleSheet("background-color: #232629; border: 1px inset #232629; min-height: 20px;")
        self.period_value.setMaximumWidth(self.width() * 0.2)

        self.grid.setSpacing(23)
        self.grid.addWidget(self.title)
        self.grid.addLayout(self.subgrid)
        self.subgrid.addWidget(self.response, 0, 0)
        self.subgrid.addWidget(self.angle, 1, 0)
        self.subgrid.addWidget(self.dcvrms, 2, 0)
        self.subgrid.addWidget(self.vpp, 3, 0)
        self.subgrid.addWidget(self.vmax, 4, 0)
        self.subgrid.addWidget(self.frequency, 5, 0)
        self.subgrid.addWidget(self.period, 6, 0)
        self.subgrid.addWidget(self.response_value, 0, 1)
        self.subgrid.addWidget(self.angle_value, 1, 1)
        self.subgrid.addWidget(self.dcvrms_value, 2, 1)
        self.subgrid.addWidget(self.vpp_value, 3, 1)
        self.subgrid.addWidget(self.vmax_value, 4, 1)
        self.subgrid.addWidget(self.frequency_value, 5, 1)
        self.subgrid.addWidget(self.period_value, 6, 1)
        self.grid.addStretch(1)

        self.setLayout(self.grid)

    def setResponse(self, response_time):
        self.response_value.setNum(response_time)

    def setAngle(self, angle_value):
        self.angle_value.setNum(angle_value)

    def setDCVrms(self, dcvrms_value):
        self.dcvrms_value.setNum(dcvrms_value)

    def setVpp(self, vpp_value):
        self.vpp_value.setNum(vpp_value)

    def setVmax(self, vmax_value):
        self.vmax_value.setNum(vmax_value)

    def setFrequency(self, frequency_value):
        self.frequency_value.setNum(frequency_value)

    def setPeriod(self, period_value):
        self.period_value.setNum(period_value * 1000)

