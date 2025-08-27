from abc import abstractmethod

class Performance:

    def __init__(self, name:str):
        self._name = name

    @abstractmethod
    def getMassFunction(self):
        pass

    def getName(self) -> str:
        return self._name
