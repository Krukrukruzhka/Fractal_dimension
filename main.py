import controller
import sys
from PyQt5 import QtWidgets


def exception(type, value, traceback):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Ошибка")
    msg.setText(f'Ошибка: {type}, {value}')
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.exec_()


if __name__ == '__main__':
    sys.excepthook = exception
    app = QtWidgets.QApplication(sys.argv)
    window = controller.LabApp()
    window.show()
    app.exec_()
