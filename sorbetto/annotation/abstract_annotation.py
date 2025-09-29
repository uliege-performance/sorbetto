# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile

from sorbetto.core.named import Named


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

    def __str__(self) -> str:
        return self.name
