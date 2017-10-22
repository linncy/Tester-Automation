import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from ui_mainwindow import Ui_MainWindow
import visa
rm = visa.ResourceManager()

class main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def connect(self):
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
    
    def startTCf(self):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #win = MyCalc()
    win = main()
    win.show()
    sys.exit(app.exec_())