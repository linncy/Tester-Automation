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
	def __init__(self, parent=None, width=5, height=4, dpi=80):
		plt.close()
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

	def real_time_plot_multicurve(self,x_data,y_data,label_data,num_of_curve):#Example of point_data: [[10,[1,2,3,4,5,6,7]],[10.4,[7,6,5,4,3,2,1]]] namely, [[x,[ydata1,ydata2,ydata3...]]]
		self.axes.cla() # Clear the current axes (From matpltlib.org/api/axes_api.html)
		self.fig.suptitle('T-C-f')
		for i in range(num_of_curve):
			command='line'+str(i+1)+'=self.axes.plot(x_data,y_data[%d],label=label_data[%d])'%(i,i)
			print(command)
			exec(command)
			print('plot line %s'%str(i+1))
		print(x_data)
		print(y_data[0])
		print(label_data[0])
		self.axes.set_ylabel('C')
		self.axes.set_xlabel('T')
		self.axes.grid(True)
		self.axes.legend(loc='upper center', bbox_to_anchor=(0.8,1.16),ncol=3,fancybox=True,shadow=True)
		self.draw()

class MatplotlibWidget(QWidget):
	def __init__(self, parent=None):
		super(MatplotlibWidget, self).__init__(parent)
		self.initUi()

	def initUi(self):
		self.layout = QVBoxLayout(self)
		self.mpl = MyMplCanvas(self, width=5, height=4, dpi=80)
		#self.mpl.start_static_plot()
		self.mpl_ntb=NavigationToolbar(self.mpl, self)
		self.layout.addWidget(self.mpl)
		self.layout.addWidget(self.mpl_ntb)