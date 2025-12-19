# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._abstract_geometric_object_2d import AbstractGeometricObject2D
from ._line import Line
from ._point import Point


class PencilOfLines(AbstractGeometricObject2D):
    """
    This class is used to represent pencils of lines.
    :math:`\\lambda_1 ( a_1 x + b_1 y + c_1 ) + \\lambda_2 ( a_2 x + b_2 y + c_2 ) = 0`
    See https://en.wikipedia.org/wiki/Pencil_(geometry)
    """

    def __init__(
        self, line_1: Line, line_2: Line, name: str | None = None, *assumptions
    ):
        """
        Constructs a new pencil of lines on two lines.

        Args:
            line_1 (Line): the line corresponding to :math:`(\\lambda_1, \\lambda_2)=(1, 0)`
            line_2 (Line): the line corresponding to :math:`(\\lambda_1, \\lambda_2)=(0, 1)`
            name (str | None, optional): _description_. Defaults to None.
        """

        assert isinstance(line_1, Line)
        assert isinstance(line_2, Line)
        self._line_1 = line_1
        self._line_2 = line_2
        AbstractGeometricObject2D.__init__(self, name, *assumptions)

    @property
    def line_1(self) -> Line:
        """
        The line corresponding to :math:`(\\lambda_1, \\lambda_2)=(1, 0)`

        Returns:
            Line: :math:`a_1 x + b_1 y + c_1 = 0`
        """
        return self._line_1

    @property
    def line_2(self) -> Line:
        """
        The line corresponding to :math:`(\\lambda_1, \\lambda_2)=(0, 1)`

        Returns:
            Line: :math:`a_2 x + b_2 y + c_2 = 0`
        """
        return self._line_2

    def _getAllAssumptions(self) -> set:
        all_assumptions = set()
        for assumption in self.assumptions:
            all_assumptions.add(assumption)
        for assumption in self._line_1.assumptions:
            all_assumptions.add(assumption)
        for assumption in self._line_2.assumptions:
            all_assumptions.add(assumption)
        return all_assumptions

    def getLine(self, lambda_1: float, lambda_2: float) -> Line:
        """
        The line corresponding to :math:`(\\lambda_1, \\lambda_2)`.

        Args:
            lambda_1 (float): the value of :math:`\\lambda_1`
            lambda_2 (float): the value of :math:`\\lambda_2`

        Returns:
            Line: the chosen line of the pixel
        """
        assert isinstance(lambda_1, float)
        assert isinstance(lambda_2, float)

        all_assumptions = self._getAllAssumptions()

        a = lambda_1 * self._line_1.a + lambda_2 * self._line_2.a
        b = lambda_1 * self._line_1.b + lambda_2 * self._line_2.b
        c = lambda_1 * self._line_1.c + lambda_2 * self._line_2.c
        name = "line ({:g},{:g}) of {}".format(lambda_1, lambda_2, self)
        return Line(a, b, c, name=name, *all_assumptions)

    def getVertex(self) -> Point:
        """
        Compute the pencil's vertex.

        Returns:
            Point: the vertex
        """

        line_1 = self._line_1
        line_2 = self._line_2

        vertex = line_1.getIntersectionWithLine(line_2)
        if not isinstance(vertex, Point):
            raise RuntimeError(
                "Impossible to compute the pencil's vertex.\n"
                + "The intersection between the two principal lines is {}".format(
                    vertex
                )
            )
        return vertex

    def draw(self, fig: Figure, ax: Axes, extent, lambdas=None, **plt_kwargs):
        """
        Draws the part of the pencil of lines that is within some axis-aligned box in some given Pyplot axes.

        Args:
            fig (_type_): a Pyplot Figure object
            ax (_type_): a Pyplot Axes object
            extent (_type_): the axis-aligned box :math:`(x_{min}, x_{max}, y_{min}, y_{max})`
            lambdas:
            plt_kwargs: options for Pyplot's plot command.
        """

        if lambdas is None:
            n = 11
            for theta in np.linspace(0.5 * np.pi, 1.0 * np.pi, n):
                sin = np.sin(theta)
                cos = np.cos(theta)
                line = self.getLine(sin, cos)
                if plt_kwargs is None:
                    plt_kwargs_bis = dict()
                else:
                    plt_kwargs_bis = plt_kwargs.copy()
                plt_kwargs_bis["linestyle"] = ":"  # dashed line
                line.draw(fig, ax, extent, **plt_kwargs_bis)
            for theta in np.linspace(0.0 * np.pi, 0.5 * np.pi, n):
                sin = np.sin(theta)
                cos = np.cos(theta)
                line = self.getLine(sin, cos)
                if plt_kwargs is None:
                    plt_kwargs_bis = dict()
                else:
                    plt_kwargs_bis = plt_kwargs.copy()
                plt_kwargs_bis["linestyle"] = "-"  # solid line
                line.draw(fig, ax, extent, **plt_kwargs_bis)
        else:
            for lambda_1, lambda_2 in lambdas:
                line = self.getLine(lambda_1, lambda_2)
                line.draw(fig, ax, extent, **plt_kwargs)
        vertex = self.getVertex()
        vertex.draw(fig, ax, extent, **plt_kwargs)

    def __str__(self) -> str:
        line_1 = self._line_1
        line_2 = self._line_2
        return "pencil of lines lambda_1 ({}) + lambda_2 ({}) = 0".format(
            line_1, line_2
        )

    def __eq__(self, other) -> bool:
        # TDOO: in this implementation, we ignore the assumptions. We should check that
        # this is really what we want to do.

        if not isinstance(other, PencilOfLines):
            return NotImplemented

        # We test if the vectors of parameters (a1,b1,c1,a2,b2,c2) of the two pencils are proportional.
        # This is the case if and only if the angle between the two vectors is pi or -pi.
        #
        # WARNING: It would NOT be correct to check the equality of the two line objects between the two pencils!

        def dot(pencil1, pencil2):
            return (
                pencil1._line1.a * pencil2._line1.a
                + pencil1._line1.b * pencil2._line1.b
                + pencil1._line1.c * pencil2._line1.c
                + pencil1._line2.a * pencil2._line2.a
                + pencil1._line2.b * pencil2._line2.b
                + pencil1._line2.c * pencil2._line2.c
            )

        norm_self = math.sqrt(dot(self, self))
        norm_other = math.sqrt(dot(other, other))
        cos_theta = dot(self, other) / norm_self / norm_other
        if math.isclose(cos_theta, -1.0):
            return True
        if math.isclose(cos_theta, 1.0):
            return True
        return False
