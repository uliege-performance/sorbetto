# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import Self

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._abstract_geometric_object_2d import AbstractGeometricObject2D
from ._line_segment import LineSegment
from ._point import Point


# TODO: should Line inherit from BilinearCurve ?
class Line(AbstractGeometricObject2D):
    """
    This class is used to represent a line.
    :math:`a x + b y + c = 0`
    See https://en.wikipedia.org/wiki/Line_(geometry)
    """

    def __init__(
        self, a: float, b: float, c: float, name: str | None = None, *assumptions
    ):
        """
        Constructs a new line :math:`a x + b y + c = 0`.

        Args:
            a (float): the parameter :math:`a`
            b (float): the parameter :math:`b`
            c (float): the parameter :math:`c`
            name (str | None, optional): the name
        """
        assert isinstance(a, float)
        assert isinstance(b, float)
        assert isinstance(c, float)
        self._a = a
        self._b = b
        self._c = c

        assert not (
            math.isclose(a, 0.0, abs_tol=1e-8) and math.isclose(b, 0.0, abs_tol=1e-8)
        )

        AbstractGeometricObject2D.__init__(self, name, *assumptions)

    @property
    def a(self) -> float:
        """
        The parameter :math:`a` of the line :math:`a x + b y + c = 0`

        Returns:
            float: :math:`a`
        """
        return self._a

    @property
    def b(self) -> float:
        """
        The parameter :math:`b` of the line :math:`a x + b y + c = 0`

        Returns:
            float: :math:`b`
        """
        return self._b

    @property
    def c(self) -> float:
        """
        The parameter :math:`c` of the line :math:`a x + b y + c = 0`

        Returns:
            float: :math:`c`
        """
        return self._c

    def getX(self, y) -> float:
        a = self._a
        b = self._b
        c = self._c

        x = -(b * y + c) / a
        return x

    def getY(self, x) -> float:
        a = self._a
        b = self._b
        c = self._c

        y = -(a * x + c) / b
        return y

    def getNormalized(self) -> Self:
        r"""
        Computes the normalized form of the line, that is :math:`a' x + b' y + c' = 0`
        such that :math:`a'^2 + b'^2 = 1` and :math:`(a',b',c') \propto (a,b,c)`.

        Returns:
            Line: the line :math:`a' x + b' y + c' = 0`
        """

        a = self._a
        b = self._b
        c = self._c

        k = math.hypot(a, b)
        return Line(a / k, b / k, c / k, self.name, *self.assumptions)

    def getIntersectionWithLine(self, other: Self) -> Self | Point | None:
        """
        Computes the intersection of the line with another one.

        Args:
            other (Self): the other line

        Returns:
            Self | Point | None: the intersection.
        """

        # implementation of Cramer's rule
        # see https://en.wikipedia.org/wiki/Cramer%27s_rule

        all_assumptions = set()
        for assumption in self.assumptions:
            all_assumptions.add(assumption)
        for assumption in other.assumptions:
            all_assumptions.add(assumption)
        name = "intersection between {} and {}".format(self, other)

        a1 = self._a
        b1 = self._b
        c1 = self._c

        a2 = other._a
        b2 = other._b
        c2 = other._c

        den = a1 * b2 - b1 * a2
        if den == 0.0:  # lines are parallel
            l1 = self.normalize()
            l2 = other.normalize()
            if l1._a * l2._a + l1._b * l2._b >= 0:
                d = math.fabs(l1._c - l2.c)  # distance between the two lines
            else:
                d = math.fabs(l1._c + l2.c)  # distance between the two lines
            if d < 1e-8:  # parallel and confounded lines
                return Line(self._a, self._b, self._c, name, *all_assumptions)
            else:  # parallel and not confounded lines
                # TODO: should be an "empty object" with the right assumptions
                return None
        else:
            x = (b1 * c2 - c1 * b2) / den
            y = (c1 * a2 - a1 * c2) / den
            assert math.isclose(a1 * x + b1 * y + c1, 0.0, abs_tol=1e-6)
            assert math.isclose(a2 * x + b2 * y + c2, 0.0, abs_tol=1e-6)
            return Point(x, y, name, *all_assumptions)

    def getIntersectionWithAxisAlignedBox(self, extent) -> LineSegment | Point | None:
        """
        Computes the intersection of the line with any given axis-aligned box.

        Args:
            extent (_type_): the axis-aligned box :math:`(x_{min}, x_{max}, y_{min}, y_{max})`

        Returns:
            LineSegment | Point | None: the intersection, or None if there is no intersection.
        """

        x_min, x_max, y_min, y_max = extent
        assert x_max > x_min
        assert y_max > y_min

        a = self._a
        b = self._b

        tol = 1e-8

        points = list()
        if b != 0.0:
            x = x_min
            y = self.getY(x)
            if (y_min - tol <= y) and (y <= y_max + tol):
                point = x, y
                points.append(point)

            x = x_max
            y = self.getY(x)
            if (y_min - tol <= y) and (y <= y_max + tol):
                point = x, y
                points.append(point)

        if a != 0.0:
            y = y_min
            x = self.getX(y)
            if (x_min - tol <= x) and (x <= x_max + tol):
                point = x, y
                points.append(point)

            y = y_max
            x = self.getX(y)
            if (x_min - tol <= x) and (x <= x_max + tol):
                point = x, y
                points.append(point)

        if len(points) == 0:
            return None  # TODO: should be an "empty object" with the right assumptions
        elif len(points) == 1:
            p = points[0]
            return Point(p[0], p[1], self.name, *self.assumptions)
        elif len(points) == 2:
            p1 = points[0]
            p1 = Point(p1[0], p1[1], "endpoint 1")
            p2 = points[-1]
            p2 = Point(p2[0], p2[1], "endpoint 2")
            return LineSegment(p1, p2, self.name, *self.assumptions)
        else:
            # Find the two furthest points
            # Choose the point p1 arbitrarily
            p1 = points[0]
            # Finding the point p2 that is the furthest form p1.
            p2 = p1
            for p0 in points:
                d01_sq = (p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2
                d21_sq = (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2
                if d01_sq > d21_sq:
                    p2 = p0
            # Finding the point p1 that is the furthest form p2.
            for p0 in points:
                d02_sq = (p0[0] - p2[0]) ** 2 + (p0[1] - p2[1]) ** 2
                d12_sq = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
                if d02_sq > d12_sq:
                    p1 = p0
            p1 = Point(p1[0], p1[1], "endpoint 1")
            p2 = Point(p2[0], p2[1], "endpoint 2")
            return LineSegment(p1, p2, self.name, *self.assumptions)

    def draw(self, fig: Figure, ax: Axes, extent, **plt_kwargs):
        """
        Draws the part of the line that is within some axis-aligned box in some given Pyplot axes.

        Args:
            fig (_type_): a Pyplot Figure object
            ax (_type_): a Pyplot Axes object
            extent (_type_): the axis-aligned box :math:`(x_{min}, x_{max}, y_{min}, y_{max})`
            plt_kwargs: options for Pyplot's plot command.
        """

        intersection = self.getIntersectionWithAxisAlignedBox(extent)
        if intersection is not None:
            intersection.draw(fig, ax, extent, **plt_kwargs)

    def __str__(self) -> str:
        a = self._a
        b = self._b
        c = self._c
        return "line ({}) x + ({}) y + ({}) = 0".format(a, b, c)

    def __eq__(self, other) -> bool:
        # TDOO: in this implementation, we ignore the assumptions. We should check that
        # this is really what we want to do.

        if not isinstance(other, Line):
            return NotImplemented

        # We test if the vectors of parameters (a,b,c) of the two lines are proportional.
        # This is the case if and only if the angle between the two vectors is pi or -pi.

        def dot(line1, line2):
            return line1._a * line2._a + line1._b * line2._b + line1._c * line2._c

        norm_self = math.sqrt(dot(self, self))
        norm_other = math.sqrt(dot(other, other))
        cos_theta = dot(self, other) / norm_self / norm_other
        if math.isclose(cos_theta, -1.0):
            return True
        if math.isclose(cos_theta, 1.0):
            return True
        return False
