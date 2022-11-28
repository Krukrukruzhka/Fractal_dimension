from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
import design
import model
import mytimer


class LabApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.handler = model.HerstModel()
        self.timer = mytimer.MyTimer()
        self.timer.timeout.connect(self.display_plots)
        self.progressBar.hide()  # Это нужно будет перенести в design.py в самом конце
        self.pushButton.clicked.connect(self.browse_folder)
        self.pushButton_2.clicked.connect(self.calculate)
        self.pushButton_3.clicked.connect(self.editFile)
        self.pushButton_4.clicked.connect(self.hidePlots)

    def editFile(self):
        self.__clear_plots()
        self.handler.kardio_list = []
        with open(f'Кардиограммы\\{self.handler.filename}', 'w+') as file:
            s = ''
            for i in self.plainTextEdit.toPlainText():
                if i == '\n':
                    if s != '':
                        self.handler.kardio_list.append(float(s))
                    s = ''
                else:
                    s = s+i
            self.handler.kardio_list.append(float(s))
            file.writelines(list(map(lambda x: str(x)+'\n', self.handler.kardio_list)))
        self.handler.herstCalculate()

    def hidePlots(self):
        count = 3
        if not self.checkBox.isChecked():
            count -= 1
            self.graphicsView.hide()
        else:
            self.graphicsView.show()
        if not self.checkBox_2.isChecked():
            count -= 1
            self.graphicsView_2.hide()
        else:
            self.graphicsView_2.show()
        if not self.checkBox_3.isChecked():
            count -= 1
            self.graphicsView_3.hide()
        else:
            self.graphicsView_3.show()
        height = int((self.height() - (count+1)*10)/count)
        y = 10
        if self.checkBox.isChecked():
            self.graphicsView.setGeometry(self.graphicsView.x(), y, self.graphicsView.width(), height)
            y += height + 10
        if self.checkBox_2.isChecked():
            self.graphicsView_2.setGeometry(self.graphicsView.x(), y, self.graphicsView.width(), height)
            y += height + 10
        if self.checkBox_3.isChecked():
            self.graphicsView_3.setGeometry(self.graphicsView.x(), y, self.graphicsView.width(), height)
            y += height + 10
        if self.handler:
            self.draw_graphics(len(self.handler.herst_list))

    def __clear_plots(self):
        self.graphicsView.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_2.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_3.setScene(QtWidgets.QGraphicsScene(self))

    def __set_access(self, flag: bool):
        self.pushButton.setEnabled(flag)
        self.pushButton_2.setEnabled(flag)
        self.pushButton_3.setEnabled(flag)
        self.pushButton_4.setEnabled(flag)
        self.groupBox.setEnabled(flag)

    def display_plots(self):
        self.timer.counter += 1
        self.progressBar.setValue(self.timer.counter)
        self.draw_graphics(self.timer.counter)
        if self.timer.counter == len(self.handler.herst_list):
            self.timer.stop()
            self.timer.counter = 0
            self.__set_access(True)
            self.progressBar.hide()
            return

    def create_scene(self, data, index: int, title: str, filename: str, width: int, height: int, with_tail: bool):
        plt.figure(figsize=(width, height))
        plt.xlim((-1, len(data)+1))
        plt.ylim((min(data)-0.2, max(data)+0.2))
        if with_tail:
            plt.plot(list(range(index - 1, len(data))), data[index-1:], color='red', linewidth=2)
        plt.plot(list(range(index)), data[:index], color='blue', linewidth=2)
        plt.grid()
        plt.title(title)
        plt.savefig(filename)
        plt.close()
        scene = QtWidgets.QGraphicsScene(self)
        item = QtWidgets.QGraphicsPixmapItem(QPixmap(filename))
        scene.addItem(item)
        return scene

    def draw_graphics(self, index: int):
        width = 1
        height = 1
        if not self.graphicsView.isHidden():
            width = self.graphicsView.width()//100 - 0.2
            height = self.graphicsView.height()//100 - 0.2
        elif not self.graphicsView_2.isHidden():
            width = self.graphicsView_2.width()//100 - 0.2
            height = self.graphicsView_2.height()//100 - 0.2
        elif not self.graphicsView_3.isHidden():
            width = self.graphicsView_3.width()//100 - 0.2
            height = self.graphicsView_3.height()//100 - 0.2
        self.graphicsView.setScene(self.create_scene(self.handler.kardio_list, index+3, 'Кардиограмма',
                                                         'fig1.png', width, height, True))
        self.graphicsView_2.setScene(self.create_scene(self.handler.herst_list, index, 'Показатель Херста',
                                                       'fig2.png', width, height, False))
        self.graphicsView_3.setScene(self.create_scene(self.handler.dim_list, index, 'Размерность',
                                                       'fig3.png', width, height, False))

    def browse_folder(self):
        self.plainTextEdit.clear()
        self.__clear_plots()
        file_url = QtWidgets.QFileDialog.getOpenFileUrl(self, "Выберите файл", "Кардиограммы")
        filename = file_url[0].url().split('/')[9]
        self.handler.loadData(filename=filename)
        self.label_3.setText(f"Текущий файл: {filename}")
        for point in self.handler.kardio_list:
            self.plainTextEdit.appendPlainText(str(point))
        self.__set_access(True)

    def calculate(self):
        self.__clear_plots()
        self.__set_access(False)
        self.handler.herstCalculate()
        self.progressBar.show()
        self.progressBar.setMaximum(len(self.handler.herst_list))
        self.timer.start(100)