import math


class HerstModel(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.kardio_list = []
        link = f'Кардиограммы\\{filename}'  # Ссылка на файл
        with open(link, 'r') as file:
            self.kardio_list = list(map(float, file.readlines()))
        self.herst_list = []

    def __herst(self, index, coeff):
        r = max(self.kardio_list[:index]) - min(self.kardio_list[:index])  # Размах
        n = len(self.kardio_list[:index])  # Кол-во элементов
        mean = sum(self.kardio_list[:index]) / n  # Среднее
        std = (sum([(i - mean) ** 2 for i in self.kardio_list[:index]]) / n) ** 0.5  # Стандартное отклонение
        return math.log(r / std) / math.log(coeff * n)

    def dimCalculate(self):
        self.dim_list = []
        for i in range(4, len(self.kardio_list)+1):
            self.dim_list.append(2-self.__herst(index=i, coeff=0.5))
