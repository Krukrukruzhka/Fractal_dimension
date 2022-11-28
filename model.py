import math


class HerstModel(object):
    def __init__(self):
        self.filename = ''
        self.kardio_list = []
        self.herst_list = []
        self.dim_list = []

    def loadData(self, filename):
        self.filename = filename
        link = f'Кардиограммы\\{filename}'  # Ссылка на файл
        with open(link, 'r') as file:
            self.kardio_list = list(map(float, file.readlines()))

    def herst(self, timepoint: int, coeff: float):
        r = max(self.kardio_list[:timepoint]) - min(self.kardio_list[:timepoint])  # Размах
        n = len(self.kardio_list[:timepoint])  # Кол-во элементов
        mean = sum(self.kardio_list[:timepoint]) / n  # Среднее
        std = (sum([(i - mean) ** 2 for i in self.kardio_list[:timepoint]]) / n) ** 0.5  # Стандартное отклонение
        return math.log(r / std) / math.log(coeff * n)

    def herstCalculate(self):
        self.herst_list = []
        for i in range(4, len(self.kardio_list)+1):
            self.herst_list.append(self.herst(timepoint=i, coeff=0.5))
        self.dim_list = [2-i for i in self.herst_list]