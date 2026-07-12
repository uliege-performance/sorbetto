# Copyright (c) 2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.flavor._ranking_flavor import RankingFlavor
from sorbetto.flavor._value_flavor import ValueFlavor
from sorbetto.parameterization._parameterization_default import ParameterizationDefault
from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking._constraint_relative_importance_satisfying_unsatisfying import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)

from ._abstract_annotation import AbstractAnnotation

if TYPE_CHECKING:
    from sorbetto.tile import Tile


# TODO: in a future version, it could be interesting to write along the curves
#  something like "no-skill for c_-" and "no-skill for c_+". Matplotlib does
#  not support writing along curves. However, there is some code available for
#  this at https://stackoverflow.com/a/44521963


class AnnotationNoSkillFixedClassPriors(AbstractAnnotation):
    """
    This annotation can be used on Tiles specific for a given performance, that
    is those with a ValueFlavor or a RankingFlavor.
    """

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
            name = "no-skill curves"
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile import Tile

        assert isinstance(tile, Tile)
        parameterization = tile.parameterization
        if not isinstance(parameterization, ParameterizationDefault):
            # TODO : make this class more generic !
            raise NotImplementedError()
        extent = parameterization.getExtent()

        # TODO: the following is not generic enough for someone extending the library
        # with another flavor specific for a given performance. All flavors that are
        # specific for a given performance could implement an interface specifying it.
        flavor = tile.flavor
        if isinstance(flavor, ValueFlavor):
            performance = flavor.performance
            color = "hotpink"
        elif isinstance(flavor, RankingFlavor):
            entity = flavor.entity
            performance = entity.performance
            color = "k"
        else:
            raise NotImplementedError()

        assert math.fabs(performance._prior_pos() - self._priorPos) < 1e-8

        plt_kwargs = self._plt_kwargs.copy()
        if "color" not in plt_kwargs.keys():
            plt_kwargs["color"] = color

        curve = parameterization._locateNoSkillForNegativeClassFixedClassPriors(
            performance
        )
        curve.draw(fig, ax, extent, **plt_kwargs)

        curve = parameterization._locateNoSkillForPositiveClassFixedClassPriors(
            performance
        )
        curve.draw(fig, ax, extent, **plt_kwargs)

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
        There is no known compatibility issues.

        Args:
            constraint (ConstraintFixedClassPriors): a constraint on importances.

        Returns:
            bool: True
        """
        assert isinstance(constraint, ConstraintFixedClassPriors)
        return True

    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintFixedPredictionRates): a constraint on importances.

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
        return ConstraintFixedClassPriors(self._priorPos)

    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        return None
