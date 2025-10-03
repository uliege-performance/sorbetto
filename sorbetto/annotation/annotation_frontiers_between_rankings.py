# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
import math
from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.parameterization.parameterization_default import ParameterizationDefault
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
from sorbetto.ranking.ranking_score import RankingScore

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationFrontiersBetweenRankings(AbstractAnnotation):
    def __init__(
        self, performnances: FiniteSetOfTwoClassClassificationPerformances, name=None
    ):
        assert isinstance(performnances, FiniteSetOfTwoClassClassificationPerformances)
        self._performances = performnances
        if len(performnances) >= 15:
            message = "{} froentiers are going to be computed. That's a lot!".format(
                len(performnances)
            )
            logging.warning(message)
        super().__init__(name)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)

        plt_kwargs = dict()
        plt_kwargs["color"] = [0.7, 0.7, 0.7]

        if isinstance(tile.parameterization, ParameterizationDefault):
            # TODO: RankingScore.equivalent is only for the default parameterization
            extent = tile.parameterization.getExtent()
            performances = self._performances
            for i, p1 in enumerate(performances):
                for j, p2 in enumerate(performances):
                    if i < j:
                        curve = RankingScore.equivalent(p1, p2)
                        curve.draw(fig, ax, extent, **plt_kwargs)
        else:
            message = (
                "AnnotationFrontiersBetweenRankings only works for ParameterizationDefault in this version.\n"
                "See RankingScore.equivalent for more information about this limitation."
            )
            logging.warning(message)

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
        Checks if all performances used in the Annotation's definition satisfy the
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

    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        """
        Checks if all performances used in the Annotation's definition satisfy the
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

    def getConstraintOnImportances(
        self,
    ) -> ConstraintRelativeImportanceSatisfyingUnsatisfying | None:
        return None

    def getConstraintOnClassPriors(self) -> ConstraintFixedClassPriors | None:
        return None

    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        return None
