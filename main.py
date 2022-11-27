from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
import sys
import design
import model
import mytimer


class LabApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.handler = None
        self.setupUi(self)
        self.timer = mytimer.MyTimer()
        self.timer.timeout.connect(self.display_plot)
        self.progressBar.hide()
        self.pushButton.clicked.connect(self.browse_folder)
        self.pushButton_2.clicked.connect(self.calculate)

    def __clear_plots(self):
        self.graphicsView.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_2.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_3.setScene(QtWidgets.QGraphicsScene(self))

    def display_plot(self):
        self.timer.counter += 1
        self.progressBar.setValue(self.timer.counter)
        self.draw_graphics(self.timer.counter, 6, 3)
        if self.timer.counter == len(self.handler.herst_list):
            self.timer.stop()
            self.timer.counter = 0
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.progressBar.hide()
            return

    def create_scene(self, data, index: int, title: str, filename: str, width: int, height: int):
        plt.figure(figsize=(width, height))
        plt.plot(list(range(index - 1, len(data))), data[index-1:], color='red')
        plt.plot(list(range(index)), data[:index], color='blue')
        plt.grid()
        plt.title(title)
        plt.savefig(filename)
        plt.clf()
        plt.close()
        scene = QtWidgets.QGraphicsScene(self)
        item = QtWidgets.QGraphicsPixmapItem(QPixmap(filename))
        scene.addItem(item)
        return scene

    def draw_graphics(self, index: int, width: int, height: int):
        self.graphicsView.setScene(self.create_scene(self.handler.kardio_list, index+3, 'Кардиограмма',
                                                         'fig1.png', width, height))
        self.graphicsView_2.setScene(self.create_scene(self.handler.herst_list, index, 'Показатель Херста',
                                                       'fig2.png', width, height))
        self.graphicsView_3.setScene(self.create_scene(self.handler.dim_list, index, 'Размерность',
                                                       'fig3.png', width, height))

    def browse_folder(self):
        self.plainTextEdit.clear()
        self.__clear_plots()
        file_url = QtWidgets.QFileDialog.getOpenFileUrl(self, "Выберите файл", "Кардиограммы")
        filename = file_url[0].url().split('/')[9]
        self.handler = model.HerstModel(filename=filename)
        self.label_3.setText(f"Текущий файл: {filename}")
        for point in self.handler.kardio_list:
            self.plainTextEdit.appendPlainText(str(point))
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)

    def calculate(self):
        self.__clear_plots()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.handler.herstCalculate()
        print(len(self.handler.herst_list) - len(self.handler.kardio_list))
        self.progressBar.show()
        self.progressBar.setMaximum(len(self.handler.herst_list))
        self.timer.start(300)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LabApp()
    window.show()
    app.exec_()
