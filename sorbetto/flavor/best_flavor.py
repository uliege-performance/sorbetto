from typing import Any

import numpy as np

from sorbetto.core.entity import Entity
from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore


class BestFlavor(AbstractNumericFlavor):
    """
    TODO actual description

    Example of Best Flavor: the SOTA Flavor.
    """

    def __init__(
        self,
        performances: FiniteSetOfTwoClassClassificationPerformances,
        entity_list: list[Entity],
        name: str = "Unnamed SOTA Flavor",
        colormap: Any = None,
    ):
        super().__init__(name=name, colormap=colormap)

        self._entity_list = entity_list
        self._nb_entities = len(entity_list)
        self._performances = performances

    @property
    def entity_list(self) -> list[Entity]:
        return self._entity_list

    @property
    def nb_entities(self) -> int:
        return self._nb_entities

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

        return np.max(values, axis=0)

    def getDefaultColormap(self):
        return "gray"

    def getLowerBound(self):
        return 0.0

    def getUpperBound(self):
        return 1.0
