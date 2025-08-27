class AbstractNumericFlavor(AbstractFlavor):
    def __init__(self, name=None):
        return

    @abstractmethod
    def getLowerBound(self):
        return

    @abstractmethod
    def getUpperBound(self):
        return
