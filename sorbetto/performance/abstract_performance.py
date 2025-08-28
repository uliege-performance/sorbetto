from abc import ABC, abstractmethod


class AbstractPerformance(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def getMassFunction(self):
        pass

    @property
    def name(self) -> str:
        return self._name
