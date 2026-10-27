# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.core.matplotlib_utils import filter_properties_for_plot

from ._abstract_geometric_object_2d import AbstractGeometricObject2D
from ._point import Point


class LineSegment(AbstractGeometricObject2D):
    """
    This class is used to represent line segments.
    See https://en.wikipedia.org/wiki/Line_segment
    """

    def __init__(self, p1: Point, p2: Point, name: str | None = None, *assumptions):
        """
        Constructs a new line segment based on the two endpoints.

        Args:
            p1 (Point): the first endpoint
            p2 (Point): the second endpoint
            name (str | None, optional): the name
        """
        assert isinstance(p1, Point)
        assert isinstance(p2, Point)
        self._p1 = p1
        self._p2 = p2
        AbstractGeometricObject2D.__init__(self, name, *assumptions)

    @property
    def p1(self) -> Point:
        """
        The first endpoint.

        Returns:
            Point: :math:`p_1`
        """
        return self._p1

    @property
    def p2(self) -> Point:
        """
        The second endpoint.

        Returns:
            Point: :math:`p_2`
        """
        return self._p2

    def draw(self, fig: Figure, ax: Axes, extent, **plt_kwargs):
        """
        Plots the line segment in some given Pyplot axes.
        TODO: extent is currently ignored.

        Args:
            fig (_type_): a Pyplot Figure object
            ax (_type_): a Pyplot Axes object
            extent (_type_): the axis-aligned box :math:`(x_{min}, x_{max}, y_{min}, y_{max})`
            plt_kwargs: options for Pyplot's plot command.
        """
        p1 = self._p1
        p2 = self._p2

        options_for_plot = filter_properties_for_plot(plt_kwargs)

        options_for_plot_bis = dict()
        options_for_plot_bis["linestyle"] = "-"
        if options_for_plot is not None:
            options_for_plot_bis.update(options_for_plot)

        ax.plot([p1.x, p2.x], [p1.y, p2.y], **options_for_plot_bis)

    def __str__(self) -> str:
        p1 = self._p1
        p2 = self._p2
        return "line segment between {} and {}".format(p1, p2)

    def __eq__(self, other) -> bool:
        # TDOO: in this implementation, we ignore the assumptions. We should check that
        # this is really what we want to do.

        if not isinstance(other, LineSegment):
            return NotImplemented
        if self._p1 == other._p1 and self._p2 == other._p2:
            return True
        if self._p1 == other._p2 and self._p2 == other._p1:
            return True
        return False
