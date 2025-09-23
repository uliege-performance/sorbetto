# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import numpy as np

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore


class BestValueFlavor(AbstractNumericFlavor):
    """
    TODO actual description

    Example of Best Value Flavor: the SOTA Flavor.
    """

    def __init__(
        self,
        performances: FiniteSetOfTwoClassClassificationPerformances,
        name: str = "Unnamed Best Value Flavor",
        colormap: Any = None,
    ):
        super().__init__(name=name, colormap=colormap)

        assert isinstance(performances, FiniteSetOfTwoClassClassificationPerformances)

        self._performances = performances

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performances

    def __call__(
        self,
        importance: Importance | np.ndarray,
    ) -> float | np.ndarray:
        values = RankingScore._compute(
            importance=importance, performance=self._performances
        )

        ans = np.max(values, axis=0, keepdims=False)
        if isinstance(ans, np.ndarray) and ans.size == 1:
            return ans.item()
        else:
            return ans

    def getDefaultColormap(self):
        return "gray"

    def getLowerBound(self) -> float:
        return 0.0

    def getUpperBound(self) -> float:
        return 1.0
