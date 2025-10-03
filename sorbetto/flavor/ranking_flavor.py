# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)
from sorbetto.performance.constraint_fixed_prediction_rates import (
    ConstraintFixedPredictionRates,
)
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.constraint_relative_importance_satisfying_unsatisfying import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)
from sorbetto.ranking.entity import Entity
from sorbetto.ranking.importance import Importance
from sorbetto.ranking.ranking_score import RankingScore


class RankingFlavor(AbstractNumericFlavor):
    """
    For a given rank :math:`r`, the *Entity Flavor* is the mathematical function that
    gives, to any Importance :math:`I`  (that is, some application-specific preferences), the
    entity ranked :math:`r`-th according to the ordering of performances induced by the
    Ranking Score :math:`R_I` corresponding to the importance :math:`I`.
    """

    def __init__(
        self,
        entity: Entity,
        entity_list: list[Entity],
        name: str = "Unnamed Ranking Flavor",
        colormap: Any = None,
    ):
        super().__init__(name=name, colormap=colormap)
        self._entity = entity
        self._entity_list = entity_list
        self._nb_entities = len(entity_list)
        self._performances = FiniteSetOfTwoClassClassificationPerformances(
            [e.performance for e in entity_list]
        )
        try:
            self._id_entity = self._entity_list.index(entity)
        except ValueError as exc:
            raise ValueError(
                "The given entity was not found in the given entity list."
            ) from exc

    @property
    def entity(self) -> Entity:
        return self._entity

    @property
    def entity_list(self) -> list[Entity]:
        return self._entity_list

    @property
    def nb_entities(self) -> int:
        return self._nb_entities

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performances

    @property
    def id_entity(self) -> int:
        return self._id_entity

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
            importance=importance, performance=self._performances
        )

        # TODO check behaviour of argsort(argsort()) with multiple identical values
        # and allow user to choose between 'min', 'max', 'mean', ...
        ranks = np.argsort(-values, axis=0)
        rank_entities = np.argsort(ranks, axis=0) + 1
        return rank_entities[self._id_entity]

    def getDefaultColormap(self):
        return plt.get_cmap("rainbow", self.nb_entities)

    def getLowerBound(self) -> float:
        return 1.0

    def getUpperBound(self) -> float:
        return float(self._nb_entities)

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
        for entity in self._entity_list:
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
        for entity in self._entity_list:
            performance = entity.performance
            if not constraint(performance):
                return False
        return True
