# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D
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


class AnnotationGeometric(AbstractAnnotation):
    """
    This type of annotation can be used with any fixed geometric object.
    """

    def __init__(
        self, geom: AbstractGeometricObject2D, name: str | None = None, **plt_kwargs
    ):
        """
        Initializes a new annotation for a geometric object.

        Args:
            geom (AbstractGeometricObject2D): the geometric object.
            name (str | None, optional): the annotation name.
        """

        assert isinstance(geom, AbstractGeometricObject2D)
        self._geom = geom

        if name is None:
            name = geom.name
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)
        parameterization = tile.parameterization
        extent = parameterization.getExtent()
        self._geom.draw(fig, ax, extent, **self._plt_kwargs)

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
        # TODO: take a look at the assumptions linked to the geometric object
        raise NotImplementedError()

    def getConstraintOnClassPriors(self) -> ConstraintFixedClassPriors | None:
        # TODO: take a look at the assumptions linked to the geometric object
        raise NotImplementedError()

    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        # TODO: take a look at the assumptions linked to the geometric object
        raise NotImplementedError()
