import sys
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QApplication, QGridLayout, QLabel, QWidget
from PyQt6.QtGui import QIcon, QAction

from layout.Widget_bottom_left import Widget_bottom_left
from layout.Widget_bottom_right import Widget_bottom_right
from layout.Widget_top_left import Widget_top_left
from layout.Widget_top_right import Widget_top_right

import numpy as np


class MainWindow(QMainWindow):

    def __init__(self, *handler):
        super().__init__()

        self.test = 1
        # init the widgets that contains the sub-layouts
        self.widget_top_left = Widget_top_left()
        self.widget_top_right = Widget_top_right()
        self.widget_bottom_left = Widget_bottom_left()
        self.widget_bottom_right = Widget_bottom_right()

        if self.test == 0:
            self.handler = handler
            self.handler.osc_connect()

        self.initUI()

    def initUI(self):
        # create an exit action
        exitAct = QAction(QIcon('icon/close.svg'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        # create a run action
        runAct = QAction(QIcon('icon/run.svg'), 'Run', self)
        runAct.setShortcut('Ctrl+R')
        runAct.setStatusTip('Run application')
        runAct.triggered.connect(self.run)

        # init a statusbar
        self.statusBar()

        # init a menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        # init a toolbar
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)
        toolbar.addAction(runAct)

        # init a central widget
        central_widget = QWidget()
        QMainWindow.setCentralWidget(self, central_widget)

        # init the main layout
        grid_main = QGridLayout()
        central_widget.setLayout(grid_main)

        # arrange the layout
        grid_main.addWidget(self.widget_top_left, 0, 0)
        grid_main.addWidget(self.widget_top_right, 0, 1)
        grid_main.addWidget(self.widget_bottom_left, 1, 0)
        grid_main.addWidget(self.widget_bottom_right, 1, 1)

        # set the main window
        self.setGeometry(300, 300, 950, 650)
        self.setWindowTitle('Main window')
        self.show()

    def run(self):
        if self.widget_top_left.mode == 1:
            self.run_waveform()
        elif self.widget_top_left.mode == 2:
            self.run_fgen_osc()
        elif self.widget_top_left.mode == 3:
            self.run_square()
        elif self.widget_top_left.mode == 4:
            self.run_triangle()

    def run_waveform(self):
        print('running waveform')
        # capture the waveform of the scope and store them into the .csv file
        # self.handler.waveform(self.widget_top_left.amplitude, self.widget_top_left.frequency)
        # plot the .csv file
        # measure the value and display
        # self.widget_top_right.setAmplitude(self.handler.osc.measure_DC_Vrms())
        self.widget_bottom_left.plot()

    def run_fgen_osc(self):
        print('running draw fgen_osc')
        # result = self.handler.draw_Vgen_Vosc_chart(self.widget_top_left.interval)
        result = np.array([(0, 1, 2, 3), (0, 1, 2, 3)])
        self.widget_bottom_right.plot(result)

    def run_square(self):
        print('running square')

    def run_triangle(self):
        print('running triangle')


def mainWindow(handler):
    app = QApplication(sys.argv)
    mainWindow = MainWindow(handler)
    sys.exit(app.exec())


def mainWindowTest():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec())
