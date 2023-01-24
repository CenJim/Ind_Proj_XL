from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout


class Widget_top_right(QWidget):

    def __init__(self):
        super().__init__()

        self.grid = QVBoxLayout()
        self.subgrid = QGridLayout()

        self.title = QLabel('Data')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.response = QLabel('Response Time:')
        self.angle = QLabel('Angle of cell:')
        self.amplitude = QLabel('Amplitude:')

        self.amplitude_value = QLabel()

        self.initUI()

    def initUI(self):
        self.grid.setSpacing(20)
        self.grid.addWidget(self.title)
        self.grid.addLayout(self.subgrid)
        self.subgrid.addWidget(self.response, 0, 0)
        self.subgrid.addWidget(self.angle, 1, 0)
        self.subgrid.addWidget(self.amplitude, 2, 0)
        self.subgrid.addWidget(self.amplitude_value, 2, 1)
        self.grid.addStretch(1)

        self.setLayout(self.grid)

    def setAmplitude(self, amplitude):
        self.amplitude_value.setNum(amplitude)

