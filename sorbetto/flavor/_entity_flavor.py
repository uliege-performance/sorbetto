# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import matplotlib.colors
import numpy as np

from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
    Entity,
    Importance,
    RankingScore,
)

from ._abstract_symbolic_flavor import AbstractSymbolicFlavor


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
        assert isinstance(rank, int)
        assert rank >= 1
        assert rank <= len(entity_list)

        self._rank = rank

        self._entity_set = set(entity_list)
        self._nb_entities = len(entity_list)

        self._performances: FiniteSetOfTwoClassClassificationPerformances | None = None

        super().__init__(name=name, colormap=colormap)

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
        assert (
            isinstance(importance, Importance)
            or isinstance(importance, np.ndarray)
            and importance.shape[-1] == 4
        )  # TODO: RankingScore also supports list[Importance]. Why not here?

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

    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintRelativeImportanceSatisfyingUnsatisfying): a constraint on importances.

        Returns:
            bool: True
        """
        assert isinstance(
            constraint, ConstraintRelativeImportanceSatisfyingUnsatisfying
        )
        return True

    def isCompatibleWithConstraintOnClassPriors(
        self, constraint: ConstraintFixedClassPriors
    ) -> bool:
        """
        Checks if the performances of all entities used in the Flavor's definition
        satisfy the given constraint on performances.

        Args:
            constraint (ConstraintFixedClassPriors): a constraint on performances.

        Returns:
            bool: True if the constraint is satisfied, and False otherwise.
        """
        assert isinstance(constraint, ConstraintFixedClassPriors)
        for entity in self._entity_set:
            performance = entity.performance
            if not constraint(performance):
                return False
        return True

    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        """
        Checks if the performances of all entities used in the Flavor's definition
        satisfy the given constraint on performances.

        Args:
            constraint (ConstraintFixedPredictionRates): a constraint on performances.

        Returns:
            bool: True if the constraint is satisfied, and False otherwise.
        """
        assert isinstance(constraint, ConstraintFixedPredictionRates)
        for entity in self._entity_set:
            performance = entity.performance
            if not constraint(performance):
                return False
        return True
