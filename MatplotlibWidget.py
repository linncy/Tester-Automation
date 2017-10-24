import sys
import random
import matplotlib
import numpy as np

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MyMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)
		self.axes.hold(True)
		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def start_static_plot(self):
		self.fig.suptitle('Test')
		np.random.seed(42)
		x = np.linspace(0, 5, 100)
		y = 2*np.sin(x) + 0.3*x**2
		y_data = y + np.random.normal(scale=0.3, size=100)
		y_data2 = y - np.random.normal(scale=0.3, size=100)
		line1=self.axes.plot(x, y)
		line2=self.axes.plot(x,y_data)
		line3=self.axes.plot(x,y_data2)
		self.axes.set_ylabel('Y Axe')
		self.axes.set_xlabel('X Axe')
		self.axes.grid(True)

class MatplotlibWidget(QWidget):
	def __init__(self, parent=None):
		super(MatplotlibWidget, self).__init__(parent)
		self.initUi()

	def initUi(self):
		self.layout = QVBoxLayout(self)
		self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
		self.mpl.start_static_plot()
		self.mpl_ntb=NavigationToolbar(self.mpl, self)
		self.layout.addWidget(self.mpl)
		self.layout.addWidget(self.mpl_ntb)