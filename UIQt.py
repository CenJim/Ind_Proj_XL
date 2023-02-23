import copy
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QApplication, QGridLayout, QLabel, QWidget, QFileDialog, \
    QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QIcon, QAction
from qt_material import apply_stylesheet

from layout.Widget_bottom_left import Widget_bottom_left
from layout.Widget_bottom_right import Widget_bottom_right
from layout.Widget_top_left import Widget_top_left
from layout.Widget_top_right import Widget_top_right

import numpy as np
import threading
import pandas as pd


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

        self.fgen_osc_dataWindow = Fgen_osc_DataWindow(self.widget_top_left.data_volume)

        self.initUI()
        self.resize(1600, 900)

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

        # create a pause action
        self.pauseAct = QAction(QIcon('icon/pause.svg'), 'Pause', self)
        self.pauseAct.setShortcut('Ctrl+P')
        self.pauseAct.setStatusTip('Pause the running')
        self.pauseAct.triggered.connect(self.pause)

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
        toolbar.addAction(self.pauseAct)
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

    def pause(self):
        if self.handler.pause == 0:
            self.handler.pause = 1
            self.pauseAct.setIcon(QIcon('icon/pause_activate.svg'))
        else:
            self.handler.pause = 0
            self.pauseAct.setIcon(QIcon('icon/pause.svg'))

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
        self.fgen_osc_dataWindow.data_volume = self.widget_top_left.data_volume
        self.fgen_osc_dataWindow.show()
        t1 = threading.Thread(target=self.handler.draw_Vgen_Vosc_chart,
                              args=(self.widget_top_left.interval, self.widget_top_left.frequency,
                                    self.widget_top_left.data_volume, self.widget_top_left.wait_time,
                                    self.widget_top_left.fgen_osc_lower_limit,
                                    self.widget_top_left.fgen_osc_upper_limit))
        t2 = threading.Thread(target=self.showData)
        t3 = threading.Thread(target=self.plot_fgen_osc)
        t1.start()
        t2.start()
        t3.start()
        # t1.join()
        # result = self.handler.draw_Vgen_Vosc_chart(self.widget_top_left.interval, self.widget_top_left.frequency)
        # result = np.array([(0, 1, 2, 3), (0, 1, 2, 3)])
        # self.widget_bottom_right.plot(self.handler.fgen_osc_result)

    def showData(self):
        vgen = copy.deepcopy(self.handler.Vgen)
        vosc = copy.deepcopy(self.handler.Vosc)
        count = 0
        self.fgen_osc_dataWindow.clearContents()
        while True:
            # print('vgen: ', vgen)
            # print('self.handler.Vgen: ', self.handler.Vgen)
            if self.handler.Vgen != vgen:
                print('update!')
                count = 0
                vgen = copy.deepcopy(self.handler.Vgen)
                self.fgen_osc_dataWindow.updateVgen(vgen)
            elif self.handler.Vosc != vosc:
                count = 0
                vosc = copy.deepcopy(self.handler.Vosc)
                self.fgen_osc_dataWindow.updateVosc(vosc)
            else:
                count = count + 1
            if count > 50:
                print('show data end')
                break
            time.sleep(0.1)
            while self.handler.pause == 1:
                time.sleep(1)

    def plot_fgen_osc(self):
        while self.handler.fgen_osc_done == 0:
            continue
        print('Plot!')
        self.widget_bottom_right.plot(self.handler.fgen_osc_result)

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
        self.widget_top_right.setResponse(self.handler.rising_time() * 1000)
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


class Fgen_osc_DataWindow(QTableWidget):
    def __init__(self, data_volume):
        super().__init__()
        self.initUI()
        self.data_volume = data_volume

    def initUI(self):
        self.setWindowTitle('Data')
        self.resize(800, 500)
        self.setRowCount(1000)
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['Fgen', 'V0', 'V1', 'V2', 'V3', 'V4', 'Vavg'])

    def updateVgen(self, vgen):
        for i in range(len(vgen)):
            self.setItem(i, 0, QTableWidgetItem(str(vgen[i])))

    def updateVosc(self, vosc):
        for col in range(self.data_volume):
            for row in range(len(vosc[col])):
                self.setItem(row, col + 1, QTableWidgetItem(str(vosc[col][row])))
        for row in range(len(vosc[self.data_volume])):
            self.setItem(row, 6, QTableWidgetItem(str(vosc[self.data_volume][row])))


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
