# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod
from typing import Any

from sorbetto.flavor.abstract_flavor import AbstractFlavor


class AbstractNumericFlavor(AbstractFlavor):
    """
    A numeric flavor is a function that gives a real number to show on a Tile for any
    given importance values.
    """

    def __init__(self, name: str = "Unnamed Numeric Flavor", colormap: Any = None):
        super().__init__(name=name, colormap=colormap)

    @abstractmethod
    def getLowerBound(self) -> float: ...

    @abstractmethod
    def getUpperBound(self) -> float: ...

    @property
    def lowerBound(self) -> float:
        return self.getLowerBound()

    @property
    def upperBound(self) -> float:
        return self.getUpperBound()
