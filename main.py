import sys, os, random
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QTableView
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from ui_mainwindow import Ui_MainWindow
import visa
import csv
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from MatplotlibWidget import *

import numpy as numpy
from numpy import random as nr
import threading
from time import ctime,sleep
from multiprocessing import Process

rm = visa.ResourceManager()
ERRORS=0.1
temp_data=[] #画图数据点
ydata=[] #画图数据点
label_data=[] #画图中曲线标签

class main(QMainWindow, Ui_MainWindow):

    Ui_MainWindow.model=QtGui.QStandardItemModel(0,3);#model初始化
    Ui_MainWindow.model.setHorizontalHeaderLabels(['T(K)','C(F)','f(Hz)'])#model初始化
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


#模拟curveplot在很多数据点的情况下的响应性能
    def debug_curveplot(self):
        #----Parameter regarding Exp------
        num_of_curve=7
        startF=3
        startT=10.0
        stopT=300
        stepT=0.4
        #---------------------------------
        T=startT
        while(T<=stopT):
            aSetofData=[]
            for i in range(num_of_curve):
                f=num_of_curve+0.5*i
                aSetofData.append([nr.randint(0,3)+2*i,f])
            main.curveplot(self,aSetofData,T)
            QApplication.processEvents()
            T=T+stepT

#响应Connect Instruments按钮的功能。连接所有仪器并弹窗提示。

    def connect(self):
        self.table(10.423456,+3.38211E-07,10**5.5)#for debug
       # self.curveplot([[+3.38211E-07,3.5],[+2.38211E-07,4.0],[+1.38211E-07,4.5]],10.4)#for debug
       # self.curveplot([[+3.38211E-07,3.5],[+2.38211E-07,4.0],[+1.38211E-07,4.5]],11.4)#for debug
       # self.curveplot([[+3.38211E-07,3.5],[+2.38211E-07,4.0],[+1.38211E-07,4.5]],12.4)#for debug
        self.debug_curveplot() #for debug
        if len(rm.list_resources())==0:
            print('No Device Found.')
        else:
            print('Device Found:', rm.list_resources())
        try:
            cm22c = rm.open_resource('GPIB0::12::INSTR')
            print("CM22C Successfully Connected")
            lcr4284a = rm.open_resource('GPIB0::25::INSTR')
            print("LCR4284A Successfully Connected")
            QMessageBox.information(self,"Connect Instruments","Connected instruemnts successfully.",QMessageBox.Ok|QMessageBox.Ok)
        except:
            print('Connection Error')
            QMessageBox.critical(self,"Connect Instruments","Fail to connect relevant instruments. Please check the connection.",QMessageBox.Ok|QMessageBox.Ok)



#table()完成向tableview中写入新的一行数据
    # def table(self, row, column, data):
    #     '''表格添加数据：第row行，column列数据更改为data'''
    #     self.model.setItem(row, column, QStandardItem('%G'%data))
    #     self.tableView.setModel(self.model)

    def table(self,T,C,f):
        self.model.appendRow([
            QtGui.QStandardItem('%G'%T),
            QtGui.QStandardItem('%G'%C),
            QtGui.QStandardItem('%G'%f),
            ])
        self.tableView.setModel(self.model)
      #  print(self.model)
        # for row in range(3):
        #     for column in range(3):
        #         item = QtGui.QStandardItem("row %s, column %s"%(row,column))
        #         self.model.setItem(row, column, item)  

    def curveplot(self,data,temp):  #data=aSetofData example: [[+3.38211E-07,3.5],[+4.13321E-07,4.0]]
        num_of_curve=len(data)
        if len(ydata)==0:
            for i in range(num_of_curve):
                ydata.append([])
        if len(label_data)==0:
            for i in range(num_of_curve):
                label_data.append('f=%sHz'%str(data[i][1]))
        for i in range(num_of_curve):
            ydata[i].append(data[i][0])
        temp_data.append(temp)
        # self.widgetGraphic.mpl.real_time_plot_multicurve(self.mpl,point_data,num_of_curve)
        self.widgetGraphic.mpl.real_time_plot_multicurve(temp_data,ydata,label_data,num_of_curve)
        # self.widgetGraphic.mpl.start_static_plot()


#响应clear按钮，清空model并重新初始化model，更新tableView
    def cleartable(self): 
        temp_data=[] #for debug
        ydata=[] #for debug
        label_data=[] #for debug
        self.model.clear()
        Ui_MainWindow.model=QtGui.QStandardItemModel(0,3);#model初始化
        Ui_MainWindow.model.setHorizontalHeaderLabels(['T(K)','C(F)','f(Hz)'])#model初始化
        self.tableView.setModel(self.model)

#响应save按钮，存储当前tableView数据到csv中
    def savetable(self):
        with open("TCf.csv","w", newline='') as datacsv:
            csvwriter = csv.writer(datacsv,dialect=("excel"))
            csvwriter.writerow(["T(K)","C(F)","f(Hz)"])
            lenrow=self.model.rowCount()
            lencolumn=self.model.columnCount()
            for row in range(lenrow):
                data=[]
                for column in range(lencolumn):
                    data.append(self.model.data(self.model.index(row, column)))
                csvwriter.writerow(data)
            print('row:',lenrow,'col:',lencolumn)
        datacsv.close()
        print('Successfully Saved')


    def startTCf(self):
        cm22c.write('stop') #Stop all control loops at first.
        print('Start T-C-f Sweep.')
        StartT=self.boxStartT.text()
        StopT=self.boxStopT.text()
        StepT=self.boxStepT.text()
        Startf=self.boxStartf.text()
        Stopf=self.boxStopf.text()
        Multiplef=self.boxMultiplef.text()
        LevelV=self.boxLevelV.text()
        BiasV=self.boxBiasV.text()        
        if self.rButtonSHORT.isChecked():
            strIntegration='SHOR,'
        elif self.rButtonMEDIUM.isChecked():
            strIntegration='MED,'
        elif self.rButtonLONG.isChecked():
            strIntegration='LONG,'
        print(StartT,StopT,StepT,Startf,Stopf,Multiplef,LevelV,BiasV,strIntegration)
        print('Sweep Start on loop1, Input Channel A')
        point_data=[] #清空画图数据点
        label_data=[] #清空画图中曲线标签
        self.cleartable(self) #清空表
        cm22c.write('loop 1:setpt %9.6f'%StartT)
        cm22c.write('control')
        while(not((cm22c.query("input? a")<=Startf*(1+ERRORS))and(cm22c.query("input? a")>=Startf*(1-ERRORS)))):
            next
        T=StartT
        while T<=StopT:
            cm22c.write('loop 1:setpt %9.6f'%T)
            while(not((cm22c.query("input? a")<=T*(1+ERRORS))and(cm22c.query("input? a")>=T*(1-ERRORS)))):
                next
            inputa=cm22c.query("input? a")
            print(inputa)
            aSetofData=[]
            f=Startf
            while (f<=Stopf):
                print("FREQ "+'%6.3f'%10**i)
                print(lcr4284a.write("FREQ "+'%6.3f'%10**f))
                if (lcr4284a.query("*OPC?")):
                    freq=lcr4284a.query("FREQuency?")
                    fetc=lcr4284a.query("FETC?")
                    print(fetc)
#                self.table(self,inputa,fetc[0],freq) 实际值
                self.table(self,inputa,fetc[0],10**f)#温度实际值，电容实际值，频率理想值
                aSetofData.append([fetc[0],f]) #某一温度下的一组C-f数据
                f=f+Multiplef
            self.curveplot(self,aSetofData,inputa)#某一温度下的一组C-f数据+温度值 aSetofData example: [[+3.38211E-07,3.5],[+4.13321E-07,4.0]]
            QApplication.processEvents()#处理事件的同时刷新页面
            T=T+StepT

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = main()
    win.show()
    sys.exit(app.exec_())