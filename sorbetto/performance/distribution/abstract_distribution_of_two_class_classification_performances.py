from abc import ABC, abstractmethod

from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class AbstractDistributionOfTwoClassClassificationPerformances(ABC):
    """
    This is the base class for all distributions of two-class classification performances.
    """

    def __init__(self, name):
        self._name = name

        super().__init__()

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def drawOneAtRandom(self) -> TwoClassClassificationPerformance: ...

    @abstractmethod
    def drawAtRandom(
        self, numPerformances: int
    ) -> FiniteSetOfTwoClassClassificationPerformances: ...

    @abstractmethod
    def getMean(self) -> TwoClassClassificationPerformance: ...

    def __str__(self):
        txt = f"{self._name}: Distribution of two-class classification performances"
        return txt
