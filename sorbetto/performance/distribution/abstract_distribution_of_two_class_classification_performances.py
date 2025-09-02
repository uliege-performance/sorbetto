import itertools
from abc import ABC, abstractmethod

import numpy as np

from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification import (
    TwoClassClassificationPerformance,
)


def generate_grid(grid_size: int):
    vec_fpr = vec_tpr = np.linspace(0, 1, num=grid_size)
    mat_fpr, mat_tpr = np.meshgrid(vec_fpr, vec_tpr, indexing="xy")

    return mat_fpr, mat_tpr


class AbstractDistributionOfTwoClassClassificationPerformances(ABC):
    def __init__(self, name):
        self._name = name

        super().__init__()

    @property
    def name(self) -> str:
        return self._name

    # def getSupport () -> ???

    @abstractmethod
    def drawAtRandom(
        self, numPerformances
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        pass

    @abstractmethod
    def getMean(self) -> TwoClassClassificationPerformance:
        pass

    def __str__(self):
        txt = f"{self._name}: Distribution of two-class classification performances"
        return txt
