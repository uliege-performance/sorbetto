# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.geometry import Point
from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)

from ._abstract_annotation import AbstractAnnotation
from ._annotation_text import AnnotationText

if TYPE_CHECKING:
    from sorbetto.tile import Tile


class AnnotationMax(AbstractAnnotation):
    """
    This type of annotation can be used to place a text on the Tile, next to the point
    corresponding to the maximum value, the text giving information about this maximum.
    """

    def __init__(
        self,
        **plt_kwargs,
    ):
        """
        Initializes the annotation.
        """

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, "maximum")

    def _whatShouldWeDraw(self, tile: "Tile") -> tuple[float, float, str]:
        from sorbetto.tile import NumericTile

        if not isinstance(tile, NumericTile):
            raise RuntimeError(
                "Trying to draw an annotation of type AnnotationMax on a Tile that is not a NumericTile. This makes no sense."
            )

        x, y, v = tile.maximize()
        label = "max: {:g}\n@ ({:g}, {:g})".format(v, x, y)
        return x, y, label

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile import Tile

        assert isinstance(tile, Tile)
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)

        x, y, label = self._whatShouldWeDraw(tile)

        parameterization = tile.parameterization
        min_x, max_x = parameterization.getBoundsParameter1()
        min_y, max_y = parameterization.getBoundsParameter2()
        try:
            assert x >= min_x and x <= max_x
            assert y >= min_y and y <= max_y
        except AssertionError:
            raise RuntimeError(
                "Trying to place a marker on the Tile outside the parameterization limits."
            )

        loc = Point(x, y)
        annotation_text = AnnotationText(loc, label, **self._plt_kwargs)
        annotation_text.draw(tile, fig, ax)

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
            constraint (ConstraintFixedClassPriors): a constraint on performances.

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
        return None

    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        return None
