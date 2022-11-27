from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
import sys
import design
import model


class LabApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.handler = None
        self.setupUi(self)
        self.pushButton.clicked.connect(self.browse_folder)
        self.pushButton_2.clicked.connect(self.calculate)

    def create_scene(self, data, title: str, filename: str):
        plt.figure(figsize=(10, 5))
        plt.plot(data)
        plt.grid()
        plt.title(title)
        plt.savefig(filename)
        scene = QtWidgets.QGraphicsScene(self)
        item = QtWidgets.QGraphicsPixmapItem(QPixmap(filename))
        scene.addItem(item)
        return scene

    def browse_folder(self):
        self.plainTextEdit.clear()
        self.graphicsView.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_2.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_3.setScene(QtWidgets.QGraphicsScene(self))
        file_url = QtWidgets.QFileDialog.getOpenFileUrl(self, "Выберите файл", "Кардиограммы")
        filename = file_url[0].url().split('/')[9]
        self.handler = model.HerstModel(filename=filename)
        self.label_3.setText(f"Текущий файл: {filename}")
        for point in self.handler.kardio_list:
            self.plainTextEdit.appendPlainText(str(point))
        self.graphicsView.setScene(self.create_scene(self.handler.kardio_list, 'Кардиограмма', 'fig1.png'))

    def calculate(self):
        self.graphicsView_2.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_3.setScene(QtWidgets.QGraphicsScene(self))
        self.handler.herstCalculate()
        self.graphicsView_2.setScene(self.create_scene(self.handler.herst_list, 'Показатель Херста', 'fig2.png'))
        self.graphicsView_3.setScene(self.create_scene(self.handler.dim_list, 'Размерность', 'fig3.png'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LabApp()
    window.show()
    app.exec_()
