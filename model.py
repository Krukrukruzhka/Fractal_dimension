import math


class HerstModel(object):
    __instance = None

    def __init__(self):
        self.filename = ''
        self.kardio_list = []
        self.herst_list = []
        self.dim_list = []
        if HerstModel.__instance:
            self.__instance = self.get_instance()

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = HerstModel()
        return cls.__instance

    def load_data(self, filename):
        self.filename = filename
        link = f'Кардиограммы\\{filename}'  # Ссылка на файл
        with open(link, 'r') as file:
            self.kardio_list = list(map(float, file.readlines()))

    @staticmethod
    def herst(data, timepoint: int, coeff: float):
        r = max(data[:timepoint]) - min(data[:timepoint])  # Размах
        n = len(data[:timepoint])  # Кол-во элементов
        mean = sum(data[:timepoint]) / n  # Среднее
        std = (sum([(i - mean) ** 2 for i in data[:timepoint]]) / n) ** 0.5  # Стандартное отклонение
        return math.log(r / std) / math.log(coeff * n)

    def herst_calculate(self):
        self.herst_list = []
        for i in range(4, len(self.kardio_list)+1):
            self.herst_list.append(self.herst(data=self.kardio_list, timepoint=i, coeff=0.5))
        self.dim_list = [2-i for i in self.herst_list]
