# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math

import matplotlib.ticker as ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._abstract_geometric_object_2d import AbstractGeometricObject2D
from ._line import Line
from ._line_segment import LineSegment
from ._point import Point


class Ruler(AbstractGeometricObject2D):
    #    - un point (x, y) par lequel la règle passe, et la valeur v en ce point
    #    - un vecteur, avec une valeur de delta valeur correspondant à ce vecteur
    #    - les bornes de valeur (min, max) entre lesquelles la règle doit aller

    def __init__(
        self,
        x: float,
        y: float,
        v: float,
        dx: float,
        dy: float,
        dv: float,
        vmin: float = -math.inf,
        vmax: float = math.inf,
        ticks=None,
        name: str | None = None,
        *assumptions,
    ):
        """
        Initializes a new Ruler object that is along a line passing through the
        point :math:`(x,y)` where the value is :math:`v`, the direction being
        given by the vector :math:`(dx,dy)` for which the increment of value is
        :math:`dv`. The ruler goes from the value :math:`v_{min}` to the value
        :math:`v_{max}`.

        Args:
            x (float): _description_
            y (float): _description_
            v (float): _description_
            dx (float): _description_
            dy (float): _description_
            dv (float): _description_
            vmin (float, optional): _description_. Defaults to -math.inf.
            vmax (float, optional): _description_. Defaults to math.inf.
            ticks (optional):
            name (str | None, optional): _description_. Defaults to None.
        """
        assert isinstance(x, float) and math.isfinite(x)
        self._x = x
        assert isinstance(y, float) and math.isfinite(y)
        self._y = y
        assert isinstance(v, float) and math.isfinite(v)
        self._v = v
        assert isinstance(dx, float) and math.isfinite(dx)
        self._dx = dx
        assert isinstance(dy, float) and math.isfinite(dy)
        self._dy = dy
        assert not math.isclose(dx * dx + dy * dy, 0.0)
        assert isinstance(dv, float) and math.isfinite(dv)
        self._dv = dv
        assert not math.isclose(dv, 0.0)
        assert isinstance(vmin, float) and math.isfinite(vmin)
        self._vmin = vmin
        assert isinstance(vmax, float) and math.isfinite(vmax)
        self._vmax = vmax
        assert vmin < vmax
        self._ticks = ticks
        AbstractGeometricObject2D.__init__(self, name, *assumptions)

    def getLine(self) -> Line:
        a = self._dy
        b = -self._dx
        c = -(a * self._x + b * self._y)
        return Line(a, b, c, name="line supporting the ruler")

    def getValue(self, point: Point) -> float:
        assert isinstance(point, Point)
        # Find lambda such that (x, y) + lambda (dx, dy) is the closes (with the
        # Euclidean distance) to the given point.
        vec_x = point.x - self._x
        vec_y = point.y - self._y
        dot_product_num = vec_x * self._dx + vec_y * self._dy
        dot_product_den = self._dx * self._dx + self._dy * self._dy
        lambda_ = dot_product_num / dot_product_den
        return self._v + lambda_ * self._dv

    def getTickPosition(self, value: float) -> Point:
        #     value = v + lambda * dv
        # <=> lambda = ( value - v ) / dv
        lambda_ = (value - self._v) / self._dv
        x = self._x + lambda_ * self._dx
        y = self._y + lambda_ * self._dy
        return Point(x, y)

    def draw(self, fig: Figure, ax: Axes, extent, **plt_kwargs):
        line = self.getLine()

        visible = line.getIntersectionWithAxisAlignedBox(extent)
        if not isinstance(visible, LineSegment):
            return  # nothing to draw

        p1 = visible.p1
        v1 = self.getValue(p1)
        v1 = max(v1, self._vmin)
        v1 = min(v1, self._vmax)

        p2 = visible.p2
        v2 = self.getValue(p2)
        v2 = max(v2, self._vmin)
        v2 = min(v2, self._vmax)

        min_visible_value = min(v1, v2)
        max_visible_value = max(v1, v2)

        point_min_visible_value = self.getTickPosition(min_visible_value)
        point_max_visible_value = self.getTickPosition(max_visible_value)
        line = LineSegment(point_min_visible_value, point_max_visible_value)
        line.draw(fig, ax, extent, **plt_kwargs)

        if self._ticks is None:
            n = 10  # ?
            locator = ticker.MaxNLocator(nbins=n)
            ticks = locator.tick_values(min_visible_value, max_visible_value)
        else:
            ticks = self._ticks

        dx = point_max_visible_value.x - point_min_visible_value.x
        dy = point_max_visible_value.y - point_min_visible_value.y
        angle = math.atan2(dy, dx) * 180 / math.pi - 90
        if angle < -90:
            angle += 180
        for value in ticks:
            tick_position = self.getTickPosition(value)
            tick_position.draw(fig, ax, extent, **plt_kwargs)
            ax.text(
                tick_position.x,
                tick_position.y,
                "  ${:g}$  ".format(value),
                c="tab:purple",
                verticalalignment="baseline",
                rotation=angle,
                fontsize="x-small",
            )

    def __eq__(self, other):
        return NotImplemented
