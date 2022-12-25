from random import gauss, random
import scipy as sp
import numpy as np
from scipy.fft import fft
import math


class HurstModel(object):
    __instance = None

    def __init__(self):
        self.filename = ''
        self.time_series = []
        self.hurst_list = []
        self.dim_list = []
        if HurstModel.__instance:
            self.__instance = self.get_instance()

    # Метод, обеспечивающий реализацию паттерна Singleton
    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = HurstModel()
        return cls.__instance

    # Выгрузка исходного временного ряда из файла
    def load_data(self, filename):
        self.filename = filename
        path = f'Кардиограммы\\{filename}'  # Путь до файла из директории, в которой находится main.py
        with open(path, 'r') as file:  # Чтение файла
            self.time_series = list(map(float, file.readlines()))

    def send_value(self):
        pass

    # Вычисление показателя Херста для среза временного ряда
    @staticmethod
    def hurst(time_series, timepoint: int, coeff: float):
        n = len(time_series[:timepoint])  # Кол-во элементов
        mean_value = sum(time_series[:timepoint]) / n  # Среднее
        deviation_list = [x-mean_value for x in time_series[:timepoint]]  # Подсчет отклонений
        amplitude = max(deviation_list)-min(deviation_list)  # Размах отклонений
        std = (sum([(x - mean_value) ** 2 for x in time_series[:timepoint]]) / n) ** 0.5  # Стандартное отклонение
        return math.log(amplitude / std) / math.log(coeff * n)  # Вычисление показателя Херста

    # Вычисление списков показателей Херста и фрактальной размерности для каждого среза (начиная с 5го элемента)
    def hurst_calculate(self):
        self.hurst_list = []
        self.dim_list = []
        for i in range(4, len(self.time_series) + 1):
            self.hurst_list.append(HurstModel.hurst(time_series=self.time_series, timepoint=i, coeff=0.5))
            self.dim_list.append(2 - self.hurst_list[-1])
            self.send_value()

    def generate_timeserires(self):
        sigma = 1
        H = 0.5
        N = np.power(2, 10)
        Fourier_seq = [gauss(0, sigma)] + [
            gauss(0, 1) * np.exp(2 * np.pi * complex(0, 1) * random()) / (np.power(i, H + 0.5)) for i in
            range(1, int(N / 2))] + [
                          gauss(0, sigma) * (2 * np.pi * complex(0, 1) * random()).real / (np.power(N / 2, H + 0.5))]
        Fourier_seq += [Fourier_seq[N - i].conjugate() for i in range(int(N / 2) + 1, N)]
        self.time_series = list(map(float, sp.fft.ifft(Fourier_seq)))
