from PyQt5 import QtWidgets
import controller
import sys


# Обработчик исключений
def exception(error_type, value, traceback):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Ошибка")
    msg.setText(f'Ошибка: {error_type}, {value}')
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.exec_()


# Точка запуска программы
if __name__ == '__main__':
    sys.excepthook = exception
    app = QtWidgets.QApplication(sys.argv)
    window = controller.LabApp()
    window.show()
    app.exec_()
