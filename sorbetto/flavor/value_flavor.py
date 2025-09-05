from typing import Any

import numpy as np

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.ranking.ranking_score import RankingScore


class ValueFlavor(AbstractNumericFlavor):
    """
    For a given performance, the *Value Flavor* is the mathematical function that
    gives, to any importance :math:`I`  (that is, some application-specific preferences), the
    value taken by the Ranking Score :math:`R_I` corresponding to this importance.
    """

    def __init__(
        self,
        performance: TwoClassClassificationPerformance,
        name: str = "Unnamed Value Flavor",
        colormap: Any = None,
    ):
        super().__init__(name=name, colormap=colormap)
        self._performance = performance

    @property
    def performance(self) -> TwoClassClassificationPerformance:
        return self._performance

    def __call__(
        self,
        importance: Importance | np.ndarray,
    ) -> float | np.ndarray:
        return RankingScore._compute(
            importance=importance,
            performance=self._performance,
        )

    def getDefaultColormap(self):
        return "gray"

    def getLowerBound(self):
        return 0.0

    def getUpperBound(self):
        return 1.0
