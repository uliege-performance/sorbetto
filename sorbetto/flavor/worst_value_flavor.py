# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import Any

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
from sorbetto.ranking.importance import Importance
from sorbetto.ranking.ranking_score import RankingScore


class WorstValueFlavor(AbstractNumericFlavor):
    """
    TODO actual description

    Example of Worst Value Flavor: the Baseline Flavor.
    """

    def __init__(
        self,
        performances: FiniteSetOfTwoClassClassificationPerformances,
        name: str = "Unnamed Worst Value Flavor",
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
        assert (
            isinstance(importance, Importance)
            or isinstance(importance, np.ndarray)
            and importance.shape[-1] == 4
        )  # TODO: RankingScore also supports list[Importance]. Why not here?

        values = RankingScore._compute(
            importance=importance, performance=self._performances
        )

        ans = np.min(values, axis=0, keepdims=False)
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
        Checks if all performances used in the Flavor's definition satisfy the
        given constraint on performances.

        Args:
            constraint (ConstraintFixedClassPriors): a constraint on performances.

        Returns:
            bool: True if the constraint is satisfied, and False otherwise.
        """
        assert isinstance(constraint, ConstraintFixedClassPriors)
        prior_pos = constraint.getPriorPos()

        min_prior_pos = self._performances.getMinPriorPos()
        if not math.isclose(min_prior_pos, prior_pos):
            return False

        max_prior_pos = self._performances.getMaxPriorPos()
        if not math.isclose(max_prior_pos, prior_pos):
            return False

        return True

    def isCompatibleWithOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        """
        Checks if all performances used in the Flavor's definition satisfy the
        given constraint on performances.

        Args:
            constraint (ConstraintFixedPredictionRates): a constraint on performances.

        Returns:
            bool: True if the constraint is satisfied, and False otherwise.
        """
        assert isinstance(constraint, ConstraintFixedPredictionRates)
        rate_pos = constraint.getRatePos()

        min_rate_pos = self._performances.getMinRatePos()
        if not math.isclose(min_rate_pos, rate_pos):
            return False

        max_rate_pos = self._performances.getMaxRatePos()
        if not math.isclose(max_rate_pos, rate_pos):
            return False

        return True
