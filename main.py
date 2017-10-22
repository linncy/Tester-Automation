import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtCore import Qt
from ui_mainwindow import Ui_MainWindow

class main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
    def connect(self):
        print('a')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #win = MyCalc()
    win = main()
    win.show()
    sys.exit(app.exec_())