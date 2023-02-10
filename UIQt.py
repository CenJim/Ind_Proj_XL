import os
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QApplication, QGridLayout, QLabel, QWidget, QFileDialog
from PyQt6.QtGui import QIcon, QAction
from qt_material import apply_stylesheet

from layout.Widget_bottom_left import Widget_bottom_left
from layout.Widget_bottom_right import Widget_bottom_right
from layout.Widget_top_left import Widget_top_left
from layout.Widget_top_right import Widget_top_right

import numpy as np


class MainWindow(QMainWindow):

    def __init__(self, handler):
        super().__init__()

        self.test = 0
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

        # create a set waveform action
        setAct = QAction(QIcon('icon/sinusoid.svg'), 'Set', self)
        setAct.setShortcut('Ctrl+W')
        setAct.setStatusTip('Set the waveform generator')
        setAct.triggered.connect(self.setWaveShape)

        # create a run action
        runAct = QAction(QIcon('icon/run.svg'), 'Run', self)
        runAct.setShortcut('Ctrl+R')
        runAct.setStatusTip('Run application')
        runAct.triggered.connect(self.run)

        # create a data download action
        downloadAct = QAction(QIcon('icon/database-download.svg'), 'Download', self)
        downloadAct.setShortcut('Ctrl+S')
        downloadAct.setStatusTip('Download the csv data')
        downloadAct.triggered.connect(lambda: self.download_data())

        # Add measurement data action
        addAct = QAction(QIcon('icon/add.svg'), 'Add Data', self)
        addAct.setShortcut('+')
        addAct.setStatusTip('Add a measurement data')
        addAct.triggered.connect(lambda: self.add_data())

        # Add reset data action
        resetAct = QAction(QIcon('icon/refresh.svg'), 'Reset Data', self)
        resetAct.setStatusTip('Reset the stored data')
        resetAct.triggered.connect(lambda: self.reset_data())

        # init a statusbar
        self.statusBar()

        # init a menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        # init a toolbar
        toolbar = self.addToolBar('Exit')
        toolbar.setIconSize(QSize(30, 30))
        toolbar.addAction(exitAct)
        toolbar.addAction(setAct)
        toolbar.addAction(addAct)
        toolbar.addAction(runAct)
        toolbar.addAction(downloadAct)
        toolbar.addAction(resetAct)

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

    def setWaveShape(self):
        self.handler.setFunGen(self.widget_top_left.waveShape, self.widget_top_left.amplitude,
                               self.widget_top_left.frequency,
                               self.widget_top_left.modulation)

    def run(self):
        if self.widget_top_left.mode == 1:
            self.run_waveform()
        elif self.widget_top_left.mode == 2:
            self.run_fgen_osc()
        elif self.widget_top_left.mode == 3:
            self.run_square()
        elif self.widget_top_left.mode == 4:
            self.run_triangle()
        elif self.widget_top_left.mode == 5:
            self.run_angle_osc()

    def download_data(self):
        file_path = QFileDialog.getOpenFileNames(self, "Download Data", os.getcwd() + "/data", "Csv files(*.csv)")

    def run_waveform(self):
        print('running waveform')
        # capture the waveform of the scope and store them into the .csv file
        self.handler.waveform(self.widget_top_left.waveShape, self.widget_top_left.amplitude,
                              self.widget_top_left.frequency,
                              self.widget_top_left.modulation)
        # plot the .csv file
        # measure the value and display
        self.widget_top_right.setDCVrms(self.handler.osc.measure_DC_Vrms())
        self.widget_top_right.setVpp(self.handler.osc.measure_Vpp())
        self.widget_top_right.setVmax(self.handler.osc.measure_Vmax())
        self.widget_top_right.setFrequency(self.handler.osc.measure_frequency())
        self.widget_top_right.setPeriod(self.handler.osc.measure_period())
        # draw the waveform
        self.widget_bottom_left.plot()

    def run_fgen_osc(self):
        print('running draw fgen_osc')
        result = self.handler.draw_Vgen_Vosc_chart(self.widget_top_left.interval, self.widget_top_left.frequency)
        # result = np.array([(0, 1, 2, 3), (0, 1, 2, 3)])
        self.widget_bottom_right.plot(result)

    def run_square(self):
        print('running square')
        self.handler.run_square(self.widget_top_left.amplitude, self.widget_top_left.frequency,
                                self.widget_top_left.modulation)
        self.handler.capture()
        # measure the value and display
        self.widget_top_right.setDCVrms(self.handler.osc.measure_DC_Vrms())
        self.widget_top_right.setVpp(self.handler.osc.measure_Vpp())
        self.widget_top_right.setVmax(self.handler.osc.measure_Vmax())
        self.widget_top_right.setFrequency(self.handler.osc.measure_frequency())
        self.widget_top_right.setPeriod(self.handler.osc.measure_period())
        # draw the waveform
        self.widget_bottom_left.plot()

    def run_triangle(self):
        print('running triangle')
        self.handler.run_triangle(self.widget_top_left.amplitude, self.widget_top_left.frequency,
                                  self.widget_top_left.modulation)
        self.handler.capture()
        # measure the value and display
        self.widget_top_right.setDCVrms(self.handler.osc.measure_DC_Vrms())
        self.widget_top_right.setVpp(self.handler.osc.measure_Vpp())
        self.widget_top_right.setVmax(self.handler.osc.measure_Vmax())
        self.widget_top_right.setFrequency(self.handler.osc.measure_frequency())
        self.widget_top_right.setPeriod(self.handler.osc.measure_period())
        # draw the waveform
        self.widget_bottom_left.plot()

    def run_angle_osc(self):
        print('running draw angle_osc')
        result = self.handler.run_angle_osc()
        self.widget_bottom_right.plot(result)

    def add_data(self):
        if self.widget_top_left.mode == 5:
            self.handler.add_data(self.widget_top_left.angle)

    def reset_data(self):
        self.handler.reset_data()

def mainWindow(handler):
    app = QApplication(sys.argv)
    mainWindow = MainWindow(handler)
    apply_stylesheet(app, theme='dark_teal.xml')
    mainWindow.show()
    sys.exit(app.exec())


def mainWindowTest():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec())
