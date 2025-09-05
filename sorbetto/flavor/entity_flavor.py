from typing import Any

import matplotlib.colors
import numpy as np

from sorbetto.core.entity import Entity
from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore


class EntityFlavor(AbstractSymbolicFlavor[Entity]):
    """
    For a given rank :math:`r`, the *Entity Flavor* is the mathematical function that
    gives, to any Importance :math:`I`  (that is, some application-specific preferences), the
    entity ranked :math:`r`-th according to the ordering of performances induced by the
    Ranking Score :math:`R_I` corresponding to the importance :math:`I`.
    """

    def __init__(
        self,
        rank: int,
        entity_list: list[Entity] | set[Entity],
        name: str = "Unnamed Entity Flavor",
        colormap: Any = None,
    ):
        super().__init__(name=name, colormap=colormap)

        self._rank = rank
        self._entity_set = set(entity_list)
        self._nb_entities = len(entity_list)
        self._performances: FiniteSetOfTwoClassClassificationPerformances | None = None

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def entity_set(self) -> set[Entity]:
        return self._entity_set

    @property
    def nb_entities(self) -> int:
        return self._nb_entities

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        if self._performances is None:
            self._performances = FiniteSetOfTwoClassClassificationPerformances(
                [e.performance for e in self._getSortedCodomain()]
            )

        return self._performances

    def __call__(
        self,
        importance: Importance | np.ndarray,
    ) -> float | np.ndarray:
        values = RankingScore._compute(
            importance=importance,
            performance=self.performances,
        )
        # performances[i] corresponds to entity self.reverse_mapper(i+1)
        # so it is valid to argsort and +1, because it IS a value from the
        # mapped codomain
        return np.argsort(-values, axis=0)[self._rank - 1] + 1

    def getDefaultColormap(self):
        colors = [e.color for e in self._getSortedCodomain()]
        return matplotlib.colors.ListedColormap(colors)

    def getCodomain(self):
        """Returns the co-domain of the flavor.
        In Entity flavor, the co-domain is the set of all possible ranks.
        """
        return self._entity_set

    def _getSortedCodomain(self) -> list[Entity]:
        """Returns the codomain of the flavor, sorted in a stable way.

        Uses the Entity name for sorting

        Returns:
            The codomain of the flavor, sorted in a stable way.
        """
        if self._sorted_codomain is None:
            self._sorted_codomain = sorted(
                self.getCodomain(),
                key=lambda e: e.name,
            )
        return self._sorted_codomain
