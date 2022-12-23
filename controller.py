from PyQt5.QtGui import QPixmap, QKeySequence
from observer import GraphicsSet
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PIL import Image
import mytimer
import design
import model


class LabApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    __instance = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.handler = model.HurstModel()
        model.HurstModel.get_instance()
        self.graphics_set = GraphicsSet()
        self.graphics_set.add(self.graphicsView)
        self.graphics_set.add(self.graphicsView_2)
        self.graphics_set.add(self.graphicsView_3)
        self.timer = mytimer.MyTimer()
        self.timer.timeout.connect(self.display_plots)
        self.progressBar.hide()  # replace to design.py
        self.pushButton.clicked.connect(self.browse_folder)
        self.pushButton_2.clicked.connect(self.calculate)
        self.pushButton_3.clicked.connect(self.edit_file)
        self.pushButton_4.clicked.connect(self.hide_plots)
        self.__create_shortcuts()
        self.actionOpen_Ctrl_O.triggered.connect(self.browse_folder)
        self.actionSave_Ctrl_S.triggered.connect(self.edit_file)
        if LabApp.__instance:
            self.__instance = self.get_instance()

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = LabApp()
        return cls.__instance

    def __create_shortcuts(self):
        QtWidgets.QShortcut(QKeySequence("Ctrl+O"), self).activated.connect(self.browse_folder)
        QtWidgets.QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.edit_file)
        # QtWidgets.QShortcut(QKeySequence("Ctrl+O"), self).activated.connect(self.browse_folder)
        # QtWidgets.QShortcut(QKeySequence("Ctrl+O"), self).activated.connect(self.browse_folder)

    def edit_file(self):
        print('edit_file start')
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
                    s = s + i
            self.handler.kardio_list.append(float(s))
            file.writelines(list(map(lambda x: str(x) + '\n', self.handler.kardio_list)))
        self.handler.hurst_calculate()
        print('edit_file stop')

    def hide_plots(self):
        print('hide_plots start')
        count_of_graphics = 3
        if not self.checkBox.isChecked():
            count_of_graphics -= 1
            self.graphicsView.hide()
            self.graphics_set.remove(self.graphicsView)
        else:
            self.graphicsView.show()
        if not self.checkBox_2.isChecked():
            count_of_graphics -= 1
            self.graphicsView_2.hide()
            self.graphics_set.remove(self.graphicsView_2)
        else:
            self.graphicsView_2.show()
        if not self.checkBox_3.isChecked():
            count_of_graphics -= 1
            self.graphicsView_3.hide()
            self.graphics_set.remove(self.graphicsView_3)
        else:
            self.graphicsView_3.show()
        height = int((self.height() - (count_of_graphics + 1) * 10) / count_of_graphics)
        y = 10
        if self.checkBox.isChecked():
            self.graphicsView.setGeometry(self.graphicsView.x(), y, self.graphicsView.width(), height)
            y += height + 10
            self.graphics_set.add(self.graphicsView)
        if self.checkBox_2.isChecked():
            self.graphicsView_2.setGeometry(self.graphicsView.x(), y, self.graphicsView.width(), height)
            y += height + 10
            self.graphics_set.add(self.graphicsView_2)
        if self.checkBox_3.isChecked():
            self.graphicsView_3.setGeometry(self.graphicsView.x(), y, self.graphicsView.width(), height)
            y += height + 10
            self.graphics_set.add(self.graphicsView_3)
        print('hide_plots stop')

    def __clear_plots(self):
        self.graphicsView.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_2.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_3.setScene(QtWidgets.QGraphicsScene(self))
        self.graphicsView_4.setScene(QtWidgets.QGraphicsScene(self))
        self.label_2.setText('')

    def __set_access(self, flag: bool):
        self.pushButton.setEnabled(flag)
        self.pushButton_2.setEnabled(flag)
        self.pushButton_3.setEnabled(flag)
        self.pushButton_4.setEnabled(flag)
        self.groupBox.setEnabled(flag)

    def notify(self, counter):
        for observer in self.graphics_set.observers:
            self.draw_graphics(counter, observer)

    def display_plots(self):
        print('display_plots start')
        self.timer.counter += 1
        self.progressBar.setValue(self.timer.counter)
        self.notify(self.timer.counter)
        if self.timer.counter == len(self.handler.hurst_list):
            self.timer.stop()
            self.timer.counter = 0
            self.__set_access(True)
            self.progressBar.hide()
            if self.handler.res_list[-1] >= 0.5:
                self.label_2.setText('Пациент здоров')
                self.draw_result('src\\im1.jpg')
            elif self.handler.res_list[-1] <= 0.4:
                self.label_2.setText('Наблюдаются отклонения')
                self.draw_result('src\\im3.png')
            else:
                self.label_2.setText('Требуется дополнительное обследование')
                self.draw_result('src\\im2.png')
            print('display_plots stop')
            return

    def draw_result(self, path: str):
        print('draw_result start')
        img = Image.open(path)
        img = img.resize((self.graphicsView_4.width() - 10, self.graphicsView_4.height() - 10))
        img.save(path)
        scene = QtWidgets.QGraphicsScene(self)
        item = QtWidgets.QGraphicsPixmapItem(QPixmap(path))
        scene.addItem(item)
        self.graphicsView_4.setScene(scene)
        print('draw_result stop')

    def create_graphics(self, data, endpoint: int, title: str, filename: str, width: int, height: int, with_tail: bool,
                        y_title: str):
        print('create_graphics start')
        plt.figure(figsize=(width, height))
        plt.xlim((-1, len(data) + 1))
        plt.ylim((min(data) - 0.2, max(data) + 0.2))
        if with_tail:
            plt.plot(list(range(endpoint - 1, len(data))), data[endpoint - 1:], color='red', linewidth=2)
        plt.plot(list(range(endpoint)), data[:endpoint], color='blue', linewidth=2)
        plt.ylabel(y_title)
        plt.grid()
        plt.title(title)
        plt.savefig(filename)
        plt.close()
        scene = QtWidgets.QGraphicsScene(self)
        item = QtWidgets.QGraphicsPixmapItem(QPixmap(filename))
        scene.addItem(item)
        print('create_graphics stop')
        return scene

    def draw_graphics(self, endpoint: int, graphic):
        print('draw_graphics start')
        width = 1
        height = 1
        if not graphic.isHidden():
            width = self.graphicsView.width() // 100 - 0.2
            height = self.graphicsView.height() // 100 - 0.2

        plot_settings = {'data': self.handler.kardio_list,
                         'endpoint': endpoint + 3,
                         'title': 'Исходный временной ряд',
                         'filename': 'src\\fig1.png',
                         'width': width,
                         'height': height,
                         'with_tail': True,
                         'y_title': ''
                         }
        if graphic == self.graphicsView:
            graphic.setScene(self.create_graphics(**plot_settings))

        plot_settings = {'data': self.handler.hurst_list,
                         'endpoint': endpoint,
                         'title': 'Показатели Херста на каждой итерации алгоритма',
                         'filename': 'src\\fig2.png',
                         'width': width,
                         'height': height,
                         'with_tail': False,
                         'y_title': 'Показатель Херста'
                         }
        if graphic == self.graphicsView_2:
            graphic.setScene(self.create_graphics(**plot_settings))

        plot_settings = {'data': self.handler.res_list,
                         'endpoint': endpoint,
                         'title': 'Фрактальная размерность на каждой итерации алгоритма',
                         'filename': 'src\\fig3.png',
                         'width': width,
                         'height': height,
                         'with_tail': False,
                         'y_title': 'Стабильность'
                         }
        if graphic == self.graphicsView_3:
            graphic.setScene(self.create_graphics(**plot_settings))
        print('draw_graphics stop')

    def browse_folder(self):
        print('browse_folder start')
        self.plainTextEdit.clear()
        self.__clear_plots()
        file_url = QtWidgets.QFileDialog.getOpenFileUrl(self, "Выберите файл", "Кардиограммы")
        filename = file_url[0].url().split('/')[9]
        self.handler.load_data(filename=filename)
        self.label_3.setText(f"Текущий файл: {filename}")
        for point in self.handler.kardio_list:
            self.plainTextEdit.appendPlainText(str(point))
        self.__set_access(True)
        print('browse_folder stop')

    def calculate(self):
        print('calculate start')
        self.__clear_plots()
        self.__set_access(False)
        self.handler.hurst_calculate()
        self.progressBar.show()
        self.progressBar.setMaximum(len(self.handler.hurst_list))
        self.timer.start(10)
        print('calculate stop')
