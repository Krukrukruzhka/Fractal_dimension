import math


class HurstModel(object):
    __instance = None

    def __init__(self):
        self.filename = ''
        self.kardio_list = []
        self.hurst_list = []
        self.res_list = []
        if HurstModel.__instance:
            self.__instance = self.get_instance()

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = HurstModel()
        return cls.__instance

    def load_data(self, filename):
        self.filename = filename
        path = f'Кардиограммы\\{filename}'  # Ссылка на файл
        with open(path, 'r') as file:
            self.kardio_list = list(map(float, file.readlines()))

    @staticmethod
    def hurst(time_series, timepoint: int, coeff: float):
        r = max(time_series[:timepoint]) - min(time_series[:timepoint])  # Размах
        n = len(time_series[:timepoint])  # Кол-во элементов
        mean = sum(time_series[:timepoint]) / n  # Среднее
        std = (sum([(i - mean) ** 2 for i in time_series[:timepoint]]) / n) ** 0.5  # Стандартное отклонение
        return math.log(r / std) / math.log(coeff * n)

    def hurst_calculate(self):
        print('hurst_calculate start')
        self.hurst_list = []
        for i in range(4, len(self.kardio_list)+1):
            self.hurst_list.append(self.hurst(time_series=self.kardio_list, timepoint=i, coeff=0.4))
        self.res_list = [1 if i > 1 else i for i in self.hurst_list]
        print('hurst_calculate stop')
