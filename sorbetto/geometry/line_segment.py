from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D
from sorbetto.geometry.point import Point


class LineSegment(AbstractGeometricObject2D):
    """
    This class is used to represent line segments.
    See https://en.wikipedia.org/wiki/Line_segment
    """

    def __init__(self, p1: Point, p2: Point, name: str | None = None):
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
        AbstractGeometricObject2D.__init__(self, name)

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

        ax.plot([p1.x, p2.x], [p1.y, p2.y], "-", plt_kwargs)

    def __str__(self) -> str:
        p1 = self._p1
        p2 = self._p2
        return "line segment between {} and {}".format(p1, p2)
