from typing import Any

import numpy as np

from sorbetto.core.entity import Entity
from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore


class EntityFlavor(AbstractSymbolicFlavor):
    """
    For a given rank $r$, the *Entity Flavor* is the mathematical function that
    gives, to any Importance $I$  (that is, some application-specific preferences), the
    entity ranked $r$-th according to the ordering of performances induced by the
    Ranking Score $R_I$ corresponding to the importance $I$.
    """

    def __init__(
        self,
        rank: int,
        entity_list: list[Entity],
        name: str = "Unnamed Entity Flavor",
        colormap: Any = None,
    ):
        super().__init__(name=name, colormap=colormap)

        self._rank = rank
        self._entity_list = entity_list
        self._nb_entities = len(entity_list)
        self._performances = FiniteSetOfTwoClassClassificationPerformances(
            [e.performance for e in entity_list]
        )

    @property
    def rank(self) -> int:
        return self._rank

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
            importance=importance,
            performance=self._performances,
        )

        return np.argsort(-values, axis=0)[self._rank]

    def getDefaultColormap(self):
        # FIXME discrete colormap
        return "rainbow"

    def getCodomain(self):
        """Returns the co-domain of the flavor.
        In Entity flavor, the co-domain is the set of all possible ranks.
        """
        return set(range(1, self._nb_entities + 1))
