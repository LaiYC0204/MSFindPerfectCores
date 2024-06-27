from PyQt5 import QtWidgets, QtCore, QtGui

import MSFindPerfectCoresUI

class Main(QtWidgets.QMainWindow, MSFindPerfectCoresUI.Ui_MSFindPerfectCores):
    def __init__(self):
         super().__init__()
         self.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())