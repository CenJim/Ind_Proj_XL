from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg
import pandas as pd
import numpy as np


class Widget_bottom_left(QWidget):

    def __init__(self):
        super().__init__()

        self.grid = QVBoxLayout()
        self.graphWidget = pg.PlotWidget()

        self.initUI()

    def initUI(self):

        title = QLabel('The Waveform of Oscilloscope')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")

        self.grid.setSpacing(10)
        self.grid.addWidget(title)
        self.grid.addWidget(self.graphWidget)

        self.setLayout(self.grid)

    def plot(self):
        self.graphWidget.clear()
        data = pd.read_csv('data/waveform_data.csv')
        time = np.array(data.iloc[:, 0])
        amplitude = np.array(data.iloc[:, 1])
        self.graphWidget.plot(time, amplitude)
