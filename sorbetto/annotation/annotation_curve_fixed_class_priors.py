# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)
from sorbetto.performance.constraint_fixed_prediction_rates import (
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking.constraint_relative_importance_satisfying_unsatisfying import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationCurveFixedClassPriors(AbstractAnnotation):
    def __init__(
        self,
        priorPos: float | ConstraintFixedClassPriors,
        name: str | None = None,
        **plt_kwargs,
    ):
        if isinstance(priorPos, ConstraintFixedClassPriors):
            priorPos = priorPos.getPriorPos()
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        self._priorPos = priorPos

        if name is None:
            name = "locus of performance orderings putting all no-skill performances with the class priors ({:g}, {:g}) on an equal footing".format(
                1.0 - priorPos, priorPos
            )
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)

        flavor = tile.flavor
        if isinstance(flavor, ValueFlavor):
            performance = flavor.performance
            priorPos = performance.pfn + performance.ptp
            if not math.isclose(priorPos, self._priorPos, abs_tol=1e-6):
                message = "wrong class priors: the value flavor is for ({}, {}) while the curve is for ({}, {})"
                message = message.format(
                    1.0 - priorPos, priorPos, 1.0 - self._priorPos, self._priorPos
                )
                raise RuntimeError(message)

        parameterization = tile.parameterization
        extent = parameterization.getExtent()

        curve = parameterization.locateOrderingsPuttingNoSkillPerformancesOnAnEqualFootingForFixedClassPriors(
            self._priorPos
        )

        curve.draw(fig, ax, extent, **self._plt_kwargs)

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
        assert isinstance(constraint, ConstraintFixedClassPriors)
        return math.isclose(constraint.getPriorPos(), self._priorPos)

    def isCompatibleWithOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintFixedPredictionRates): a constraint on performances.

        Returns:
            bool: True
        """
        assert isinstance(constraint, ConstraintFixedPredictionRates)
        return True

    def getConstraintOnImportances(
        self,
    ) -> ConstraintRelativeImportanceSatisfyingUnsatisfying | None:
        return None

    def getConstraintOnClassPriors(self) -> ConstraintFixedClassPriors | None:
        return ConstraintFixedClassPriors(priorPos=self._priorPos)

    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        return None
