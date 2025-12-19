# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)

if TYPE_CHECKING:
    from sorbetto.tile import Tile

from sorbetto.core import Named


class AbstractAnnotation(ABC, Named):
    """
    This is the base class for all annotations, which are things that are drawn on top of Tiles.
    """

    def __init__(self, name: str | None = None):
        """
        Initializes a new annotation.

        Args:
            name (str | None, optional): the annotation name.
        """
        ABC.__init__(self)
        Named.__init__(self, "unnamed annotation", name)

    @abstractmethod
    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        pass

    @abstractmethod
    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool:
        """
        Checks if this Annotation is compatible with the given constraint on importances.

        Args:
            constraint (ConstraintRelativeImportanceSatisfyingUnsatisfying): a constraint on importances.

        Returns:
            bool: True if this Annotation is compatible with the given constraint, False otherwise.
        """
        ...

    @abstractmethod
    def isCompatibleWithConstraintOnClassPriors(
        self, constraint: ConstraintFixedClassPriors
    ) -> bool:
        """
        Checks if this Annotation is compatible with the given constraint on performances.

        Args:
            constraint (ConstraintFixedClassPriors): a constraint on performances.

        Returns:
            bool: True if this Annotation is compatible with the given constraint, False otherwise.
        """
        ...

    @abstractmethod
    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        """
        Checks if this Annotation is compatible with the given constraint on performances.

        Args:
            constraint (ConstraintFixedPredictionRates): a constraint on performances.

        Returns:
            bool: True if this Annotation is compatible with the given constraint, False otherwise.
        """
        ...

    @abstractmethod
    def getConstraintOnImportances(
        self,
    ) -> ConstraintRelativeImportanceSatisfyingUnsatisfying | None: ...

    @abstractmethod
    def getConstraintOnClassPriors(self) -> ConstraintFixedClassPriors | None: ...

    @abstractmethod
    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None: ...

    def __str__(self) -> str:
        return self.name
