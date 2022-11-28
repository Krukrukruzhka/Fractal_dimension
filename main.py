import controller
import sys
from PyQt5 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = controller.LabApp()
    window.show()
    app.exec_()
