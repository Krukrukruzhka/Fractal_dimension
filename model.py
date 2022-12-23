import math
import controller


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
        n = len(time_series[:timepoint])  # Кол-во элементов
        mean_value = sum(time_series[:timepoint]) / n  # Среднее
        deviation_list = [x-mean_value for x in time_series[:timepoint]]
        amplitude = max(deviation_list)-min(deviation_list)  # Размах отклонений
        std = (sum([(x - mean_value) ** 2 for x in time_series[:timepoint]]) / n) ** 0.5  # Стандартное отклонение
        return math.log(amplitude / std) / math.log(coeff * n)

    def hurst_calculate(self):
        self.hurst_list = []
        self.res_list = []
        for i in range(4, len(self.kardio_list)+1):
            self.hurst_list.append(HurstModel.hurst(time_series=self.kardio_list, timepoint=i, coeff=0.5))
            self.res_list.append(2-self.hurst_list[-1])
