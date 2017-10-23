import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QTableView
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from ui_mainwindow import Ui_MainWindow
import visa
import csv

rm = visa.ResourceManager()
ERRORS=0.1

class main(QMainWindow, Ui_MainWindow):

    Ui_MainWindow.model=QtGui.QStandardItemModel(0,3);#model初始化
    Ui_MainWindow.model.setHorizontalHeaderLabels(['T(K)','C(F)','f(Hz)'])#model初始化
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

#响应Connect Instruments按钮的功能。连接所有仪器并弹窗提示。

    def connect(self):
        self.table(10.400000,+3.38211E-07,+3.15789E+03)#for debug
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

#响应clear按钮，清空model并重新初始化model，更新tableView
    def cleartable(self): 
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
            f=Startf
            while (f<=Stopf):
                print("FREQ "+'%6.3f'%10**i)
                print(lcr4284a.write("FREQ "+'%6.3f'%10**f))
                if (lcr4284a.query("*OPC?")):
                    freq=lcr4284a.query("FREQuency?")
                    fetc=lcr4284a.query("FETC?")
                    print(fetc)
                self.table(self,inputa,fetc[0],freq)
                f=f+Multiplef
            T=T+StepT

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = main()
    win.show()
    sys.exit(app.exec_())