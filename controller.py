from PyQt5 import QtWidgets
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
        model.HerstModel.get_instance()
        self.timer = mytimer.MyTimer()
        self.timer.timeout.connect(self.display_plots)
        self.progressBar.hide()  # replace to design.py
        self.pushButton.clicked.connect(self.browse_folder)
        self.pushButton_2.clicked.connect(self.calculate)
        self.pushButton_3.clicked.connect(self.edit_file)
        self.pushButton_4.clicked.connect(self.hide_plots)

    def edit_file(self):
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
        self.handler.herst_calculate()

    def hide_plots(self):
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

    def create_scene(self, data, index: int, title: str, filename: str, width: int, height: int, with_tail: bool,
                     y_title: str):
        plt.figure(figsize=(width, height))
        plt.xlim((-1, len(data)+1))
        plt.ylim((min(data)-0.2, max(data)+0.2))
        if with_tail:
            plt.plot(list(range(index - 1, len(data))), data[index-1:], color='red', linewidth=2)
        plt.plot(list(range(index)), data[:index], color='blue', linewidth=2)
        plt.ylabel(y_title)
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
        plot_settings = {'data': self.handler.kardio_list,
                         'index': index+3,
                         'title': 'Кардиограмма',
                         'filename': 'fig1.png',
                         'width': width,
                         'height': height,
                         'with_tail': True,
                         'y_title': ''
                        }
        self.graphicsView.setScene(self.create_scene(**plot_settings))

        plot_settings = {'data': self.handler.herst_list,
                         'index': index,
                         'title': 'Показатели Херста в каждый момент кардиограммы',
                         'filename': 'fig2.png',
                         'width': width,
                         'height': height,
                         'with_tail': False,
                         'y_title': 'Показатель Херста'
                        }
        self.graphicsView_2.setScene(self.create_scene(**plot_settings))

        plot_settings = {'data': self.handler.dim_list,
                         'index': index,
                         'title': 'Стабильность ритма в каждый момент кардиограммы (0 - нестабильна, 1 - стабильна)',
                         'filename': 'fig3.png',
                         'width': width,
                         'height': height,
                         'with_tail': False,
                         'y_title': 'Стабильность'
                         }
        self.graphicsView_3.setScene(self.create_scene(**plot_settings))

    def browse_folder(self):
        self.plainTextEdit.clear()
        self.__clear_plots()
        file_url = QtWidgets.QFileDialog.getOpenFileUrl(self, "Выберите файл", "Кардиограммы")
        filename = file_url[0].url().split('/')[9]
        self.handler.load_data(filename=filename)
        self.label_3.setText(f"Текущий файл: {filename}")
        for point in self.handler.kardio_list:
            self.plainTextEdit.appendPlainText(str(point))
        self.__set_access(True)

    def calculate(self):
        self.__clear_plots()
        self.__set_access(False)
        self.handler.herst_calculate()
        self.progressBar.show()
        self.progressBar.setMaximum(len(self.handler.herst_list))
        self.timer.start(10)
