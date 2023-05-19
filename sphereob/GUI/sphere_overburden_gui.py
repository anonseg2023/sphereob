# Python modules
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
import pandas as pd
import matplotlib.backends.backend_qt5agg as backend_qt5agg
from matplotlib.figure import Figure
import sys
import threading
from PyQt5.QtWidgets import QPushButton, QSlider
from PyQt5 import QtGui, QtWidgets
# Local application modules
from sphereob.resources import resources
from sphereob.utils.sphere_response import sphereresponse

APP_NAME = 'EM sphere-overburden response'
AUTHOR = 'Double Blind'


class OptionsMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Create the spinbox widgets used for inputting sphere-overburden parameters (thickness, conductivity)

        self.thick_ob_sb = QtWidgets.QDoubleSpinBox()
        self.sigma_sp_sb = QtWidgets.QDoubleSpinBox()
        self.sigma_ob_sb = QtWidgets.QDoubleSpinBox()
        self.strike = QtWidgets.QDoubleSpinBox()
        self.dip = QtWidgets.QDoubleSpinBox()
        self.dipole = QtWidgets.QDoubleSpinBox()
        self.pulse = QtWidgets.QDoubleSpinBox()
        self.a_sb = QtWidgets.QDoubleSpinBox()
        self.timedelta_sb = QtWidgets.QDoubleSpinBox()

        # Create text input widget for transmitter-receiver geometry
        # Set position / offset values using .setText

        self.tx = QtWidgets.QLineEdit()
        self.tx.setText('0,0,60')

        self.rx = QtWidgets.QLineEdit()
        self.tx.setText('0,0,120')

        self.txrx = QtWidgets.QLineEdit()
        self.txrx.setText('12.5,0,56')

        self.rspop = QtWidgets.QLineEdit()
        self.rspop.setText('-200')

        self.user_profile = QtWidgets.QLineEdit()
        self.user_profile.setText('1000')

        self.read_data_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/chart_line_delete.png'), 'Import Waveform Data',
        )

        self.PlotPoint = QtWidgets.QComboBox()
        PointList = ['Rx', 'Tx', 'Mid point']
        self.PlotPoint.addItems(PointList)

        self.Xconvention = QtWidgets.QComboBox()
        Sign = ["+ve", "-ve"]
        self.Xconvention.addItems(Sign)

        # Setting labels and positions of variables in widgets
        # Defining limits for integers values

        for widget in (self.thick_ob_sb, self.sigma_sp_sb, self.sigma_ob_sb, self.strike, self.dip, self.pulse,
                       self.dipole, self.a_sb, self.timedelta_sb):
            if widget == self.strike or self.dip:
                widget.setRange(0, 360)
                widget.setSingleStep(1)
                widget.setDecimals(0)
            if widget == self.pulse:
                widget.setRange(0, 100000000)
                widget.setDecimals(8)
            if widget == self.timedelta_sb:
                widget.setRange(0, 1000)
                widget.setDecimals(4)
            if widget == self.a_sb:
                widget.setRange(0, 10000)
                widget.setDecimals(0)
                widget.setSingleStep(1)
            if widget ==self.dipole:
                widget.setRange(0, 1000000000)
                widget.setDecimals(2)
            if widget == self.sigma_ob_sb:
                widget.setRange(0, 10000)
                widget.setDecimals(4)
            if widget == self.sigma_sp_sb:
                widget.setRange(0, 10000)
                widget.setDecimals(2)
                widget.setSingleStep(0.1)




        coeff_grid = QtWidgets.QGridLayout()
        coeff_grid.addWidget(QtWidgets.QLabel('Transmitter Position(m)'), 0, 0)
        coeff_grid.addWidget(self.tx, 0, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Tx-Rx Offset (m)'), 1, 0)
        coeff_grid.addWidget(self.txrx, 1, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Overburden Conductivity (S/m)'), 2, 0)
        coeff_grid.addWidget(self.sigma_ob_sb, 2, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Overburden Thickness (m)'), 3, 0)
        coeff_grid.addWidget(self.thick_ob_sb, 3, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Sphere Conductivity (S/m)'), 4, 0)
        coeff_grid.addWidget(self.sigma_sp_sb, 4, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Sphere Radius (m)'), 5, 0)
        coeff_grid.addWidget(self.a_sb, 5, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Sphere Depth (m)'), 0, 2) #a_sp
        coeff_grid.addWidget(self.rspop, 0, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Strike'), 1, 2)
        coeff_grid.addWidget(self.strike, 1, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Dip'), 2, 2)
        coeff_grid.addWidget(self.dip, 2, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Pulse Length'), 3, 2)
        coeff_grid.addWidget(self.pulse, 3, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Period'), 4, 2)
        coeff_grid.addWidget(self.timedelta_sb, 4, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Dipole Moment'), 5, 2)
        coeff_grid.addWidget(self.dipole, 5, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Profile length'), 6, 2)
        coeff_grid.addWidget(self.user_profile, 6, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Plotting point'), 6, 0)
        coeff_grid.addWidget(self.PlotPoint, 6, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('X sign convention'), 7, 0)
        coeff_grid.addWidget(self.Xconvention, 7, 1)

        coeff_grid.addWidget(self.read_data_btn, 7,2,1,2)



        # Setting labels and positions of variables in widgets
        # Defining limits for integers values


        # Create the "Graph Options" widgets
        # Create checkbox for user to choose which components of response to plot

        self.sphere_x = QtWidgets.QCheckBox('x-component')
        self.sphere_x.setChecked(False)

        self.sphere_z = QtWidgets.QCheckBox('z-component')
        self.sphere_z.setChecked(False)

        self.sphere_y = QtWidgets.QCheckBox('y-component')
        self.sphere_y.setChecked(False)

        self.alltime = QtWidgets.QCheckBox('default')
        self.alltime.setChecked(True)

        self.earlytime = QtWidgets.QCheckBox('early')
        self.earlytime.setChecked(False)

        self.midtime = QtWidgets.QCheckBox('mid')
        self.midtime.setChecked(False)

        self.latetime = QtWidgets.QCheckBox('late')
        self.latetime.setChecked(False)

        self.alltime.stateChanged.connect(self.onWindowChange)
        self.earlytime.stateChanged.connect(self.onWindowChange)
        self.midtime.stateChanged.connect(self.onWindowChange)
        self.latetime.stateChanged.connect(self.onWindowChange)



        # Self.legend_loc_lbl = QtGui.QLabel('waveform data')
        # Self.legend_loc_cb = QtGui.QPushButton('read in from csv',self)

        cb_box = QtWidgets.QHBoxLayout()

        # Create plot area

        cb_box.addWidget(self.sphere_x)
        cb_box.addWidget(self.sphere_z)
        cb_box.addWidget(self.sphere_y)

        legend_box = QtWidgets.QHBoxLayout()
        # legend_box.addWidget(self.legend_loc_cb)
        legend_box.addStretch()

        self.graph_box = QtWidgets.QVBoxLayout()
        self.graph_box.addLayout(cb_box)
        self.graph_box.addLayout(legend_box)
        self.graph_gb = QtWidgets.QGroupBox('Plot options')
        #graph_gb.setlayout

        self.scaleLinear = QtWidgets.QCheckBox('linear')
        self.scaleLinear.setChecked(True)

        self.scaleLog = QtWidgets.QCheckBox('log')
        self.scaleLog.setChecked(False)

        self.scaleLog.stateChanged.connect(self.onScaleChange)
        self.scaleLinear.stateChanged.connect(self.onScaleChange)


        self.plotSphere =QtWidgets.QCheckBox('sphere-ob')
        self.plotSphere.setChecked(True)

        self.plotImport =QtWidgets.QCheckBox('imported data')
        self.plotImport.setChecked(False)

        self.dBdT = QtWidgets.QCheckBox('dB/dT')
        self.dBdT.setChecked(True)

        self.BF = QtWidgets.QCheckBox('B Field')
        self.BF.setChecked(False)

        self.ChannelBox = QtWidgets.QComboBox()
        ChannelList = ['Default channels', 'Early channels', 'Mid channels', 'Late channels']
        self.ChannelBox.addItems(ChannelList)
        #self.windows_label = QtWidgets.QLabel('Select time windows to be plotted', self)

        self.plot_container = QtWidgets.QGridLayout()
        #self.plot_container.addWidget(self.windows_label)
        self.plot_container.addWidget(self.ChannelBox)
        self.plot_container.addWidget(self.plotSphere)
        self.plot_container.addWidget(self.scaleLinear)
        self.plot_container.addWidget(self.plotImport,1,1)
        self.plot_container.addWidget(self.ChannelBox, 0,0)
        self.plot_container.addWidget(self.scaleLog,2,1)
        #self.plot_container.addWidget(self.dBdT,2,5)
        #self.plot_container.addWidget(self.BF,2,9)
        self.plot_container.addLayout(self.graph_box,6,0,1,20)
        self.graph_gb.setLayout(self.plot_container)



        #coeff_grid.addLayout(self.graph_box,6,0,1,20)
        coeff_gb = QtWidgets.QGroupBox('Sphere overburden parameters')
        coeff_gb.setLayout(coeff_grid)


        other_grid = QtWidgets.QGridLayout()

        self.read_tem_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/chart_line_delete.png'),
            'Import TEM, XYZ ',
        )

        self.lineBox = QtWidgets.QLineEdit()
        self.lineBox.setEnabled(False)
        self.slider_label = QtWidgets.QLabel('Select Line to be plotted', self)



        other_grid.addWidget(self.slider_label)
        other_grid.addWidget(self.read_tem_btn)
        other_grid.addWidget(self.lineBox)
        self.window_box = QtWidgets.QHBoxLayout()
        self.window_box.addWidget(self.ChannelBox)
        # self.window_box.addWidget(self.earlytime)
        # self.window_box.addWidget(self.midtime)
        # self.window_box.addWidget(self.latetime)
        # other_grid.addLayout(self.window_box,4,0)
        # other_grid.addWidget(self.windows_label,3,0)







        other_gb = QtWidgets.QGroupBox('Imported data plotter')




        other_gb.setLayout(other_grid)

        # Create the update/reset plot buttons

        self.update_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/calculator.png'),
            'Plot Response',
        )
        self.reset_values_btn = QPushButton(
            QtGui.QIcon(':/resources/arrow_undo.png'),
            'Reset Values',
        )
        self.clear_graph_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/arrow_undo.png'),
            'Clear Plot',
        )
        self.reset_values_btn.clicked.connect(self.reset_values)

        self.read_tem_btn.clicked.connect(self.read_tem)

        # self.read_data_btn = QtWidgets.QPushButton(
        #     QtGui.QIcon(':/resources/chart_line_delete.png'), 'Import Waveform Data',
        # )

        # Create the main layout with widgets and plotting area

        container = QtWidgets.QVBoxLayout()
        container.addWidget(coeff_gb)
        container.addWidget(other_gb)
        container.addWidget(self.graph_gb)


        container.addStretch()

        container.addWidget(self.update_btn)
        container.addWidget(self.reset_values_btn)
        container.addWidget(self.clear_graph_btn)

        self.setLayout(container)


        # Populate and reset the widgets with values
        self.reset_values()

    def reset_values(self):
        """
        Sets the default values of the option widgets.
        """
        self.a_sb.setValue(100)
        self.rspop.setText('-200')
        self.thick_ob_sb.setValue(4)
        self.sigma_sp_sb.setValue(0.5)
        self.sigma_ob_sb.setValue(0.03)
        self.strike.setValue(90)
        self.dip.setValue(0)
        self.dipole.setValue(1847300)
        self.pulse.setValue(0.00398)
        self.timedelta_sb.setValue(0.03)
        self.txrx.setText('12,0,56')

    def read_tem(self):
        import os.path
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select TEM File:', "", "TEM data files (*.TEM)")
        if fileName:
            self.xs = 1
            data = pd.read_csv(fileName, sep='\s+', header=None, skiprows=5)
            data2 = data.dropna()
            self.TEM = data2.rename(columns=data2.iloc[0]).drop(data2.index[0])

            del self.TEM['CH10']
            del self.TEM['No']
            del self.TEM['F']
            self.lineID = self.TEM.NORTH.unique()
            self.lineBox.setText(os.path.basename(fileName))

            return self.lineID


    def legend_change(self):
        return


    def onScaleChange(self, state):
        if state == Qt.Checked:
            if self.sender() == self.scaleLinear:
                self.scaleLog.setChecked(False)
            elif self.sender() == self.scaleLog:
                self.scaleLinear.setChecked(False)

    def onWindowChange(self, state):
        if state == Qt.Checked:
            if self.sender() == self.alltime:
                self.earlytime.setChecked(False)
                self.midtime.setChecked(False)
                self.latetime.setChecked(False)
            elif self.sender() == self.earlytime:
                self.alltime.setChecked(False)
                self.latetime.setChecked(False)
                self.midtime.setChecked(False)
            elif self.sender() == self.midtime:
                self.earlytime.setChecked(False)
                self.alltime.setChecked(False)
                self.latetime.setChecked(False)
            elif self.sender() == self.latetime:
                self.alltime.setChecked(False)
                self.earlytime.setChecked(False)
                self.midtime.setChecked(False)

        # Get the currently checked plots


class AppForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # Set the window title
        self.setWindowTitle(APP_NAME)
        self.imported = False
        self.wave = 0

        # Create the options menu in a dock widget
        self.options_menu = OptionsMenu()
        dock = QtWidgets.QDockWidget('Options', self)
        dock.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable
        )
        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea,
        )
        dock.setWidget(self.options_menu)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        # Connect the signals from the options menu
        self.options_menu.update_btn.clicked.connect(self.launch_selenium_Thread)

        self.options_menu.clear_graph_btn.clicked.connect(self.clear_graph)

        if self.options_menu.sphere_x.isChecked() == True:
            self.options_menu.sphere_x.stateChanged.connect(self.redraw_graph)

        if self.options_menu.sphere_z.isChecked() == True:
            self.options_menu.sphere_z.stateChanged.connect(self.redraw_graph)

        self.options_menu.read_data_btn.clicked.connect(self.readCSV)

        #self.options_menu.read_tem_btn.clicked.connect(self.readTEM)


        #self.options_menu.read_tem_btn.clicked.connect(self.read_tem)

        if self.options_menu.sphere_z.isChecked() == True and self.options_menu.sphere_x.isChecked() == True:
            self.fig = Figure()
            self.canvas = backend_qt5agg.FigureCanvasQTAgg(self.fig)
            self.canvas.setParent(self)
            self.ax1 = self.axes = self.fig.add_subplot(111)
            self.ax2 = self.axes = self.fig.add_subplot(211)

        if self.options_menu.sphere_z.isChecked() == False or self.options_menu.sphere_x.isChecked() == False:
            self.fig = Figure()
            self.canvas = backend_qt5agg.FigureCanvasQTAgg(self.fig)
            self.canvas.setParent(self)

        self.status_text = QtWidgets.QLabel("Set paramters and select response components to be plotted")
        self.statusBar().addWidget(self.status_text, 0)
        self.statusBar().setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.progressBar = QtWidgets.QProgressBar(self)
        self.statusBar().addPermanentWidget(self.progressBar, 1)
        self.statusBar().addWidget(self.progressBar)

        # Initialize the graph
        self.clear_graph()

        # Set the graph as the main window widget
        self.setCentralWidget(self.canvas)

        # Create the exit application function in the menubar

        file_exit_action = QtWidgets.QAction('E&xit', self)
        file_exit_action.setToolTip('Exit')
        file_exit_action.setIcon(QtGui.QIcon(':/resources/door_open.png'))
        file_exit_action.triggered.connect(self.close)

        #
        # about_action = QtWidgets.QAction('&About', self)
        # about_action.setToolTip('About')
        # about_action.setIcon(QtGui.QIcon(':/resources/icon_info.gif'))
        # self.connect(
        #     about_action,
        #     QtCore.pyqtSignal('triggered()'),
        #     self.show_about,
        # )

        # Create the menubar add further functionality at later date

        file_menu = self.menuBar().addMenu('&File')
        # file_menu.addAction(file_preview_waveform)
        file_menu.addAction(file_exit_action)
        #file_menu = self.menuBar().addMenu('&Edit')
        #file_menu = self.menuBar().addMenu('&View')
        #help_menu = self.menuBar().addMenu('&Help')
        # help_menu.addAction(about_action)

    def readCSV(self):
        DataName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select CSV File:', '', "CSV data files (*.csv)")
        if DataName == "":
            self.status_text.setText("No waveform data selected")
            return
        else:
            with open(DataName) as input_file:
                self.imported = True
                self.waveformdata = np.genfromtxt(input_file, delimiter=',')
                self.status_text.setText("Successfully loaded and updated waveform parameters")

                if self.waveformdata.shape[1] >= 2:
                    self.windows = self.waveformdata.T[0]
                    self.wave = self.waveformdata.T[1]
                else:
                    self.windows = self.waveformdata.T[0]


    def calculate_data(self):

        """
            A function call to the main function that calculates the response using the user inputted values being
            called from the widgets defined in options_menu.py
        """

        sphere = sphereresponse()
        sphere.a = self.options_menu.a_sb.value()
        sphere.rsp =np.array([0,0,int(self.options_menu.rspop.text())])
        sphere.offset_tx_rx = np.array([int(n) for n in self.options_menu.txrx.text().split(',')], dtype=np.int64)
        sphere.rtx = np.array([int(n) for n in self.options_menu.tx.text().split(',')], dtype=np.int64)
        sphere.thick_ob = self.options_menu.thick_ob_sb.value()
        sphere.sigma_sp = self.options_menu.sigma_sp_sb.value()
        sphere.sigma_ob = self.options_menu.sigma_ob_sb.value()
        sphere.strike = self.options_menu.strike.value()
        sphere.dip = self.options_menu.dip.value()
        sphere.P = self.options_menu.pulse.value()
        sphere.T = self.options_menu.timedelta_sb.value()
        sphere.prof_length = int(self.options_menu.user_profile.text())
        #sphere.prof_end = [int(n) for n in self.options_menu.user_profile.text().split(',')][1]
        if self.options_menu.Xconvention.currentIndex() == 0:
            sphere.Xsign = '+ve'
        if self.options_menu.Xconvention.currentIndex() == 1:
            sphere.Xsign = '-ve'

        if self.imported == True:
            sphere.wave = self.wave
            sphere.windows = self.windows[~np.isnan(self.windows)]

        if self.options_menu.PlotPoint.currentIndex() == 0:
            sphere.PlottingPoint = 'Rx'
        if self.options_menu.PlotPoint.currentIndex() == 1:
            sphere.PlottingPoint = 'Tx'
        if self.options_menu.PlotPoint.currentIndex() == 2:
            sphere.PlottingPoint = 'Mid point'


        # Checks if the sphere is dipping or not passed as value to main routine

        if self.options_menu.dip.value() == 0:
            sphere.apply_dip = 0
        else:
            sphere.apply_dip = 1

            if sphere.sigma_sp == 0:
                sphere.sigma_sp = 0.00000000000001
        if sphere.sigma_ob == 0:
            sphere.sigma_ob = 0.00000000000001
        results = sphere.calculate()

        """
            The following is an if-then loop for plotting the different components of the response given which boxes are checked
            This will be rewritten more efficiently 
        """

        if (self.options_menu.sphere_z.isChecked() and self.options_menu.sphere_x.isChecked()) and self.options_menu.sphere_y.isChecked():

            self.axes = self.fig.add_subplot(3, 1, 1)

            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw)/3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw)/3)
                stop = ((sphere.nw)/3) + ((sphere.nw)/3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            i = int(start)
            while i >= start and i<= stop -1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_x[i],
                               color='0.4')
                i += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('x-component (nT/s)')
            else:
                self.axes.set_ylabel('x-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')
            self.axes = self.fig.add_subplot(3, 1, 2)

            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw) / 3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw) / 3)
                stop = ((sphere.nw) / 3) + ((sphere.nw) / 3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            k = int(start)
            while k >= start and k <= stop - 1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_z[k],
                               color='0.4')
                k += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('z-component (nT/s)')
            else:
                self.axes.set_ylabel('z-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.axes = self.fig.add_subplot(3, 1, 3)

            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw) / 3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw) / 3)
                stop = ((sphere.nw) / 3) + ((sphere.nw) / 3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            j = int(start)
            while j >= start and j <= stop - 1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_y[j],
                               color='0.4')  # will have to change x axis for changing param
                j += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('y-component (nT/s)')
            else:
                self.axes.set_ylabel('y-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.canvas.draw()



        elif self.options_menu.sphere_z.isChecked() and self.options_menu.sphere_x.isChecked() and self.options_menu.sphere_y.isChecked() == False:

            self.axes = self.fig.add_subplot(2, 1, 1)
            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw)/3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw)/3)
                stop = ((sphere.nw)/3) + ((sphere.nw)/3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            i = int(start)
            while i >= start and i<= stop -1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_x[i],
                               color='0.4')
                i += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('x-component (nT/s)')
            else:
                self.axes.set_ylabel('x-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.axes = self.fig.add_subplot(2, 1, 2)
            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw)/3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw)/3)
                stop = ((sphere.nw)/3) + ((sphere.nw)/3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            k = int(start)
            while k >= start and k<= stop -1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_z[k],
                               color='0.4')
                k += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('z-component (nT/s)')
            else:
                self.axes.set_ylabel('z-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.canvas.draw()


        elif self.options_menu.sphere_z.isChecked() and self.options_menu.plotSphere.isChecked() and self.options_menu.plotImport.isChecked():

            self.axes = self.fig.add_subplot(2, 1, 1)


            lines = self.options_menu.TEM.EAST.unique()
            profile_data = self.options_menu.TEM.drop(
                columns=['EAST', 'NORTH', 'LEVEL', 'ELEV', 'STATION', 'COMPONENT'])
            num_lines = len(lines)

            # check if line is EW or NS
            if num_lines == 1:
                x_axis = self.options_menu.TEM.NORTH
            else:
                x_axis = self.options_menu.TEM.EAST

            # check if profile data has multiple components or just z
            num_comp = self.options_menu.TEM.COMPONENT.unique()

            if len(num_comp) == 1 and num_comp == 'Z':
                zcomp = profile_data.values
            if len(num_comp) == 1 and num_comp == 'Y':
                ycomp = profile_data.values
            if len(num_comp) == 1 and num_comp == 'X':
                xcomp = profile_data.values
            if len(num_comp) != 1:
                xcomp = profile_data[profile_data.index % 3 == 0].values
                ycomp = profile_data[profile_data.index % 3 == 1].values
                zcomp = profile_data[profile_data.index % 3 == 2].values


            profile = x_axis.astype(float)

            temprofile = []
            if self.options_menu.sphere_z.isChecked() == True:
                temprofile = zcomp
            if self.options_menu.sphere_x.isChecked() == True:
                temprofile = xcomp
            if self.options_menu.sphere_y.isChecked() == True:
                temprofile = ycomp

            windows = len(np.transpose(temprofile))
            tran = np.transpose(temprofile)
            j = 0

            while j < windows:
                self.axes.plot(profile.astype(int), np.transpose(temprofile.astype(float))[j],color = "red")
                j += 1

            self.axes.set_xlabel('Profile (m)')
            self.axes.set_ylabel('Response (pT)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.axes = self.fig.add_subplot(2, 1, 2)
            z = sphere.H_tot_z
            k = 0
            while k < len(sphere.H_tot_z):
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_z[k],
                               color='0.4')  # will have to change x axis for changing param
                k += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('z-component (nT/s)')
            else:
                self.axes.set_ylabel('z-component (A/m)')
            self.axes.grid(True, which='both', ls='-')

            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.canvas.draw()



        elif self.options_menu.sphere_x.isChecked() and self.options_menu.plotSphere.isChecked() and self.options_menu.plotImport.isChecked():

            self.axes = self.fig.add_subplot(2, 1, 1)
            lines = self.options_menu.TEM.EAST.unique()
            profile_data = self.options_menu.TEM.drop(
                columns=['EAST', 'NORTH', 'LEVEL', 'ELEV', 'STATION', 'COMPONENT'])
            num_lines = len(lines)

            # check if line is EW or NS
            if num_lines == 1:
                x_axis = self.options_menu.TEM.NORTH
            else:
                x_axis = self.options_menu.TEM.EAST

            # check if profile data has multiple components or just z
            num_comp = self.options_menu.TEM.COMPONENT.unique()

            if len(num_comp) == 1 and num_comp == 'Z':
                zcomp = profile_data.values
            if len(num_comp) == 1 and num_comp == 'Y':
                ycomp = profile_data.values
            if len(num_comp) == 1 and num_comp == 'X':
                xcomp = profile_data.values
            if len(num_comp) != 1:
                xcomp = profile_data[profile_data.index % 3 == 0].values
                ycomp = profile_data[profile_data.index % 3 == 1].values
                zcomp = profile_data[profile_data.index % 3 == 2].values

            profile = x_axis.astype(float)

            temprofile = []
            if self.options_menu.sphere_z.isChecked() == True:
                temprofile = zcomp
            if self.options_menu.sphere_x.isChecked() == True:
                temprofile = xcomp
            if self.options_menu.sphere_y.isChecked() == True:
                temprofile = ycomp

            windows = len(np.transpose(temprofile))
            tran = np.transpose(temprofile)
            j = 0

            while j < windows:
                self.axes.plot(profile.astype(int), np.transpose(temprofile.astype(float))[j], color="red")
                j += 1

            self.axes.set_xlabel('Profile (m)')
            self.axes.set_ylabel('Response (pT)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.axes = self.fig.add_subplot(2, 1, 2)
            x = sphere.H_tot_x
            k = 0
            while k < len(sphere.H_tot_x):
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_x[k],
                               color='0.4')  # will have to change x axis for changing param
                k += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('x-component (nT/s)')
            else:
                self.axes.set_ylabel('x-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.canvas.draw()

        elif self.options_menu.sphere_y.isChecked() and self.options_menu.plotSphere.isChecked() and self.options_menu.plotImport.isChecked():

            self.axes = self.fig.add_subplot(2, 1, 1)
            lines = self.options_menu.TEM.EAST.unique()
            profile_data = self.options_menu.TEM.drop(
                columns=['EAST', 'NORTH', 'LEVEL', 'ELEV', 'STATION', 'COMPONENT'])
            num_lines = len(lines)

            # check if line is EW or NS
            if num_lines == 1:
                x_axis = self.options_menu.TEM.NORTH
            else:
                x_axis = self.options_menu.TEM.EAST

            # check if profile data has multiple components or just z
            num_comp = self.options_menu.TEM.COMPONENT.unique()

            if len(num_comp) == 1 and num_comp == 'Z':
                zcomp = profile_data.values
            if len(num_comp) == 1 and num_comp == 'Y':
                ycomp = profile_data.values
            if len(num_comp) == 1 and num_comp == 'X':
                xcomp = profile_data.values
            if len(num_comp) != 1:
                xcomp = profile_data[profile_data.index % 3 == 0].values
                ycomp = profile_data[profile_data.index % 3 == 1].values
                zcomp = profile_data[profile_data.index % 3 == 2].values

            profile = x_axis.astype(float)

            temprofile = []
            if self.options_menu.sphere_z.isChecked() == True:
                temprofile = zcomp
            if self.options_menu.sphere_x.isChecked() == True:
                temprofile = xcomp
            if self.options_menu.sphere_y.isChecked() == True:
                temprofile = ycomp

            windows = len(np.transpose(temprofile))
            tran = np.transpose(temprofile)
            j = 0

            while j < windows:
                self.axes.plot(profile.astype(int), np.transpose(temprofile.astype(float))[j], color="red")
                j += 1

            self.axes.set_xlabel('Profile (m)')
            self.axes.set_ylabel('Response (pT)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.axes = self.fig.add_subplot(2, 1, 2)
            y = sphere.H_tot_y
            k = 0
            while k < len(sphere.H_tot_y):
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_y[k],
                               color='0.4')  # will have to change x axis for changing param
                k += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('y-component (nT/s)')
            else:
                self.axes.set_ylabel('y-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.canvas.draw()


        elif self.options_menu.sphere_z.isChecked() == False and self.options_menu.sphere_x.isChecked() and self.options_menu.sphere_y.isChecked(): #=False

            self.axes = self.fig.add_subplot(2, 1, 1)
            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw)/3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw)/3)
                stop = ((sphere.nw)/3) + ((sphere.nw)/3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            i = int(start)
            while i >= start and i<= stop -1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_x[i],
                               color='0.4')  # will have to change x axis for changing param
                i += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('x-component (nT/s)')
            else:
                self.axes.set_ylabel('x-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')
            # the first subplot in the first figure

            self.axes = self.fig.add_subplot(2, 1, 2)
            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw) / 3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw) / 3)
                stop = ((sphere.nw) / 3) + ((sphere.nw) / 3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            k = int(start)
            while k >= start and k <= stop - 1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_y[k],
                               color='0.4')  # will have to change x axis for changing param
                k += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('y-component (nT/s)')
            else:
                self.axes.set_ylabel('y-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.canvas.draw()
        elif self.options_menu.sphere_z.isChecked() and self.options_menu.sphere_x.isChecked() == False and self.options_menu.sphere_y.isChecked():

            self.axes = self.fig.add_subplot(2, 1, 1)
            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw) / 3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw) / 3)
                stop = ((sphere.nw) / 3) + ((sphere.nw) / 3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            i = int(start)
            while i >= start and i <= stop - 1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_z[i],
                               color='0.4')
                i += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('z-component (nT/s)')
            else:
                self.axes.set_ylabel('z-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.axes = self.fig.add_subplot(2, 1, 2)
            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw)/3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw)/3)
                stop = ((sphere.nw)/3) + ((sphere.nw)/3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            k = int(start)
            while k >= start and k<= stop -1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_y[k],
                               color='0.4')
                k += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('y-component (nT/s)')
            else:
                self.axes.set_ylabel('y-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')

            self.canvas.draw()


        elif self.options_menu.sphere_x.isChecked() and self.options_menu.sphere_z.isChecked() == False and self.options_menu.sphere_y.isChecked() == False and self.options_menu.plotSphere.isChecked():

            self.fig.clf()
            self.axes = self.fig.add_subplot(111)
            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw) / 3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw) / 3)
                stop = ((sphere.nw) / 3) + ((sphere.nw) / 3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            i = int(start)
            while i >= start and i <= stop - 1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_x[i],
                               color='0.4')  # will have to change x axis for changing param
                i += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('x-component (nT/s)')
            else:
                self.axes.set_ylabel('x-component (A/m)')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')
            self.canvas.draw()

        elif self.options_menu.plotImport.isChecked() and self.options_menu.plotSphere.isChecked() == False:

            self.fig.clf()
            self.axes = self.fig.add_subplot(111)
            lines = self.options_menu.TEM.EAST.unique()
            profile_data = self.options_menu.TEM.drop(
                columns=['EAST', 'NORTH', 'LEVEL', 'ELEV', 'STATION', 'COMPONENT'])
            num_lines = len(lines)

            # check if line is EW or NS
            if num_lines == 1:
                x_axis = self.options_menu.TEM.NORTH
            else:
                x_axis = self.options_menu.TEM.EAST

            # check if profile data has multiple components or just z
            num_comp = self.options_menu.TEM.COMPONENT.unique()

            if len(num_comp) == 1 and num_comp == 'Z':
                zcomp = profile_data.values
            if len(num_comp) == 1 and num_comp == 'Y':
                ycomp = profile_data.values
            if len(num_comp) == 1 and num_comp == 'X':
                xcomp = profile_data.values
            if len(num_comp) != 1:
                xcomp = profile_data[profile_data.index % 3 == 0].values
                ycomp = profile_data[profile_data.index % 3 == 1].values
                zcomp = profile_data[profile_data.index % 3 == 2].values

            profile = x_axis.astype(float)

            temprofile = []
            if self.options_menu.sphere_z.isChecked() == True:
                temprofile = zcomp
            if self.options_menu.sphere_x.isChecked() == True:
                temprofile = xcomp
            if self.options_menu.sphere_y.isChecked() == True:
                temprofile = ycomp

            windows = len(np.transpose(temprofile))
            tran = np.transpose(temprofile)
            j = 0

            while j < windows:
                self.axes.plot(profile.astype(int), np.transpose(temprofile.astype(float))[j], color="red")
                j += 1

            self.axes.set_xlabel('Profile (m)')
            self.axes.set_ylabel('Response (pT)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')
            self.canvas.draw()


        elif self.options_menu.sphere_z.isChecked() and self.options_menu.sphere_x.isChecked() == False and self.options_menu.sphere_y.isChecked() == False:

            self.fig.clf()
            self.axes = self.fig.add_subplot(111)
            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw) / 3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw) / 3)
                stop = ((sphere.nw) / 3) + ((sphere.nw) / 3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            k = int(start)
            while k >= start and k <= stop - 1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_z[k],
                               color='0.4')  # will have to change x axis for changing param
                k += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('z-component (nT/s)')
            else:
                self.axes.set_ylabel('z-component (A/m)')
            self.axes.grid(True, which='both', ls='-')

            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')
            self.canvas.draw()

        elif self.options_menu.sphere_z.isChecked() == False and self.options_menu.sphere_x.isChecked() == False and self.options_menu.sphere_y.isChecked():

            self.fig.clf()
            self.axes = self.fig.add_subplot(111)
            if self.options_menu.ChannelBox.currentIndex() == 0:
                start = 0
                stop = len(sphere.H_tot_x)
            elif self.options_menu.ChannelBox.currentIndex() == 3:
                start = 0
                stop = (sphere.nw) / 3
            elif self.options_menu.ChannelBox.currentIndex() == 2:
                start = ((sphere.nw) / 3)
                stop = ((sphere.nw) / 3) + ((sphere.nw) / 3)
            elif self.options_menu.ChannelBox.currentIndex() == 1:
                start = ((sphere.nw) / 3) + ((sphere.nw) / 3)
                stop = sphere.nw
            k = int(start)
            while k >= start and k <= stop - 1:
                self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_y[k],
                               color='0.4')  # will have to change x axis for changing param
                k += 1

            self.axes.set_xlabel('Profile (m)')
            if isinstance(self.wave, int) == False:
                self.axes.set_ylabel('y-component (nT/s)')
            else:
                self.axes.set_ylabel('y-component (A/m)')
            self.axes.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                self.axes.set_yscale('log')
            self.canvas.draw()

        self.progressBar.setRange(0, 1)
        self.status_text.setText("Finished")
        self.statusBar().setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))

    def clear_graph(self):

        self.redraw_graph()

    def redraw_graph(self):

        self.fig.clf()

        self.canvas.draw()

    def updateLabel(self, value):

        self.label.setText(str(value))

    def changeLine(self, value):

        self.label.setText(str(value))

    def launch_selenium_Thread(self):

        """
            A function to prevent the program from becoming unresponsive while the response is being calculated/plotted
        """
        t = threading.Thread(target=self.calculate_data)
        self.status_text.setText("Generating response")

        # Create updating progress bar
        self.statusBar().setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.progressBar.setRange(0, 0)
        t.start()

    def show_about(self):
        """
        Display the "about" dialog box.
        """
        message = '''<font size="+2">%s</font>
            <p>A sphere - overburden response plotter written in Python.
            <p>Written by %s,
            <a href="http://opensource.org/licenses/MIT">MIT Licensed</a>
            <p>Icons from <a href="http://www.famfamfam.com/">famfamfam</a> and
            <a href="http://commons.wikimedia.org/">Wikimedia
            Commons</a>.''' % (APP_NAME, AUTHOR)

        QtWidgets.QMessageBox.about(self, 'About ' + APP_NAME, message)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/resources/icon.svg'))
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    form = AppForm()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()