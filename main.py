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

from MatplotlibWidget import *

rm = visa.ResourceManager()
ERRORS=0.1
temp_data=[] #画图数据点
ydata=[] #画图数据点
label_data=[] #画图中曲线标签
# cm22c = rm.open_resource('GPIB1::12::INSTR')
# print("CM22C Successfully Connected")
# lcr4284a = rm.open_resource('GPIB1::25::INSTR')
# print("LCR4284A Successfully Connected")

class main(QMainWindow, Ui_MainWindow):

    Ui_MainWindow.model=QtGui.QStandardItemModel(0,3);#model初始化
    Ui_MainWindow.model.setHorizontalHeaderLabels(['T(K)','C(F)','f(Hz)'])#model初始化
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


    def cvsweep(self):
#---------------------------
        startV=-2 #
        stopV=0.55
        stepV=0.05
#---------------------------
        V=startV
        lcr4284a.write("BIAS:STAT 1") #开DC，测CV下要开DC BIAS
        lcr4284a.write("VOLT 25MV")
        lcr4284a.write("FREQ "+'1000')
        while(V<=stopV):
            lcr4284a.write("BIAS:VOLT %f"%V)
            sleep(0.1)
            fetc=lcr4284a.query("FETC?")
            self.table(V,float(fetc[:12]),0)
            V=V+stepV



#模拟curveplot在很多数据点的情况下的响应性能
    def debug_curveplot(self):
        #----Parameter regarding Exp------
        num_of_curve=7
        startF=3
        startT=10.0
        stopT=14
        stepT=0.4
        #---------------------------------
        counter=0
        total_steps=int((stopT-startT)/stepT)+1
        T=startT
        while(T<=stopT+stepT):
            aSetofData=[]
            for i in range(num_of_curve):
                f=num_of_curve+0.5*i
                aSetofData.append([nr.randint(0,3)+2*i,f])
                self.table(T,aSetofData[i][0],f)
            main.curveplot(self,aSetofData,T)
            print(counter/total_steps*100+1)
            self.progressBar.setValue(counter/total_steps*100+1)
            QApplication.processEvents()
            counter+=1
            T=T+stepT

    def on_instrument_TemperatureController(self):
        print(-1)

#响应Connect Instruments按钮的功能。连接所有仪器并弹窗提示。

    def connect(self):
        self.cvsweep()
       # self.table(10.423456,+3.38211E-07,10**5.5)#for debug
       # self.curveplot([[+3.38211E-07,3.5],[+2.38211E-07,4.0],[+1.38211E-07,4.5]],10.4)#for debug
       # self.curveplot([[+3.38211E-07,3.5],[+2.38211E-07,4.0],[+1.38211E-07,4.5]],11.4)#for debug
       # self.curveplot([[+3.38211E-07,3.5],[+2.38211E-07,4.0],[+1.38211E-07,4.5]],12.4)#for debug
       # self.debug_curveplot() #for debug
        if len(rm.list_resources())==0:
            print('No Device Found.')
        else:
            print('Device Found:', rm.list_resources())
        try:
            cm22c = rm.open_resource('GPIB1::12::INSTR')
            print("CM22C Successfully Connected")
            lcr4284a = rm.open_resource('GPIB1::25::INSTR')
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
                label_data.append('f=10E%sHz'%str(data[i][1]))
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
        #self.widgetGraphic.mpl.axes.cla()
        #self.widgetGraphic.mpl.clf() 
        

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
        #total_steps=(StartT-StopT)/StepT+1
        counter=0
        print(StartT,StopT,StepT,Startf,Stopf,Multiplef,LevelV,BiasV,strIntegration)
        #print('Total Step: %d'%total_steps)
        print('Sweep Start on loop1, Input Channel A')
        point_data=[] #清空画图数据点
        label_data=[] #清空画图中曲线标签
        self.cleartable() #清空表
        cm22c.write('loop 1:setpt %9.6f'%float(StartT))
        cm22c.write('control')
        # while(not((float(cm22c.query("input? a"))<=float(Startf)*(1+ERRORS))and(float(cm22c.query("input? a"))>=float(Startf)*(1-ERRORS)))):
        #      print(float(cm22c.query("input? a")),float(Start)*(1+ERRORS))
        #      sleep(0.2)
        T=float(StartT)
        while T<=float(StopT)+float(StepT):
            cm22c.write('loop 1:setpt %9.6f'%T)
            nowT=cm22c.query("input? a")
            # while((float(cm22c.query("input? a"))<=T*(1+ERRORS))and(float(cm22c.query("input? a"))>=T*(1-ERRORS))):
            #     print(float(cm22c.query("input? a"),T))
            #     sleep(0.2)
            inputa=cm22c.query("input? a")
            print(inputa)
            aSetofData=[]
            f=float(Startf)
            while (f<=float(Stopf)):
                print("FREQ "+'%6.3f'%10**f)
                print(lcr4284a.write("FREQ "+'%6.3f'%10**f))
                if (lcr4284a.query("*OPC?")):
                    freq=lcr4284a.query("FREQuency?")
                    sleep(0.1)
                    fetc=lcr4284a.query("FETC?")
                    print(fetc)
#                self.table(self,inputa,fetc[0],freq) 实际值
                self.table(float(inputa),float(fetc[:12]),10**f)#温度实际值，电容实际值，频率理想值
                aSetofData.append([float(fetc[:12]),f]) #某一温度下的一组C-f数据
                f=f+float(Multiplef)
            counter+=1
            #self.progressBar.setValue(counter/total_steps*100+1)
            self.curveplot(aSetofData,float(inputa))#某一温度下的一组C-f数据+温度值 aSetofData example: [[+3.38211E-07,3.5],[+4.13321E-07,4.0]]
            QApplication.processEvents()#处理事件的同时刷新页面
            T=T+float(StepT)
        cm22c.write('stop')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = main()
    win.show()
    sys.exit(app.exec_())