from PyQt5 import QtCore


class MyTimer(QtCore.QTimer):
    def __init__(self):
        super().__init__()
        self.counter = 0


