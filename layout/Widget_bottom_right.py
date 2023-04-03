from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg

class Widget_bottom_right(QWidget):

    def __init__(self):
        super().__init__()

        self.grid = QVBoxLayout()
        self.graphWidget = pg.PlotWidget()

        self.initUI()

    def initUI(self):
        title = QLabel('Data Chart')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")

        self.grid.setSpacing(10)
        self.grid.addWidget(title)
        self.grid.addWidget(self.graphWidget)

        self.setLayout(self.grid)

    def plot(self, data):
        self.graphWidget.clear()
        self.graphWidget.plot(data[0], data[1])
