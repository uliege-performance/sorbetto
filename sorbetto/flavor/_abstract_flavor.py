# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from sorbetto.core import Named
from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
    Importance,
)


class AbstractFlavor(ABC, Named):
    """
    A flavor is a function of importance values.
    It can be represented graphically with Tiles.
    """

    # TODO: I guess that a colormap should be:
    #           - either None
    #           - or a np.ndarray of dimension 2 with 3 or 4 columns
    #           - or a matplotlib.colors.Colormap object
    #           - or a name

    def __init__(self, name: str | None = None, colormap: Any = None):
        self._colormap = colormap
        ABC.__init__(self)
        Named.__init__(self, "unnamed Flavor", name)

    @property
    def colormap(self) -> Any:
        if self._colormap is None:
            return self.getDefaultColormap()
        return self._colormap

    @colormap.setter
    def colormap(self, colormap: Any) -> None:
        self._colormap = colormap

    @abstractmethod
    def __call__(self, importance: Importance | np.ndarray) -> Any:
        """Computes the value of the flavor for the given importance value(s).


        Args:
            importance (Importance | np.ndarray): The importance value(s). Either a
                single Importance object or a numpy array of shape (..., 4), in which
                case the last dimension corresponds to (itn, ifp, ifn, itp).


        Returns:
            The value of the flavor evaluated at the given importance(s)
        """

    @abstractmethod
    def getDefaultColormap(self) -> Any: ...

    @abstractmethod
    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool: ...

    @abstractmethod
    def isCompatibleWithConstraintOnClassPriors(
        self, constraint: ConstraintFixedClassPriors
    ) -> bool: ...

    @abstractmethod
    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool: ...
