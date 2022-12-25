from abc import ABC, abstractmethod


class AbstractObserver(ABC):
    @abstractmethod
    def update(self):
        pass


class GraphicsSet:
    def __init__(self):
        self.observers = set()

    def add(self, observer):
        self.observers.add(observer)

    def remove(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
