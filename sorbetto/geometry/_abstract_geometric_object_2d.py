# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.core import Named


class AbstractGeometricObject2D(ABC, Named):
    def __init__(self, name: str | None = None, *assumptions):
        self._assumptions = assumptions
        ABC.__init__(self)
        Named.__init__(self, "unnamed geometric object", name)

    @abstractmethod
    def draw(self, fig: Figure, ax: Axes, extent, **plt_kwargs) -> None: ...

    @property
    def assumptions(self) -> tuple:
        return self._assumptions

    @abstractmethod
    def __eq__(self, other) -> bool:
        # TODO: should we ignore the assumptions in these tests or take them into account?
        ...
