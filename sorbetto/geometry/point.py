from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D


class Point(AbstractGeometricObject2D):
    """
    This class is used to represent points.
    See https://en.wikipedia.org/wiki/Point_(geometry)
    """

    def __init__(self, x: float, y: float, name: str | None = None):
        """
        Constructs a new point :math:`(x,y)` based on its coordinates and an optional name.

        Args:
            x (float): the first coordinate of the point
            y (float): the second coordinate of the point
            name (str | None, optional): the name
        """
        assert isinstance(x, float)
        assert isinstance(y, float)
        self._x = x
        self._y = y
        AbstractGeometricObject2D.__init__(self, name)

    @property
    def x(self) -> float:
        """
        The first coordinate, :math:`x`, of the point :math:`(x,y)`.

        Returns:
            float: :math:`x`
        """
        return self._x

    @property
    def y(self) -> float:
        """
        The second coordinate, :math:`y`, of the point :math:`(x,y)`.

        Returns:
            float: :math:`y`
        """
        return self._y

    def draw(self, fig: Figure, ax: Axes, extent, **plt_kwargs):
        """
        If the point is withing some axis-aligned box, then plots it in some given Pyplot axes.

        Args:
            fig (_type_): a Pyplot Figure object
            ax (_type_): a Pyplot Axes object
            extent (_type_): the axis-aligned box :math:`(x_{min}, x_{max}, y_{min}, y_{max})`
            plt_kwargs: options for Pyplot's plot command.
        """
        x_min = extent[0]
        x_max = extent[1]
        assert x_max > x_min

        y_min = extent[2]
        y_max = extent[3]
        assert y_max > y_min

        x = self._x
        y = self._y

        if x < x_min or x > x_max:
            return
        if y < y_min or y > y_max:
            return

        ax.plot(x, y, plt_kwargs)

    def __str__(self) -> str:
        return "point ({:g}, {:g})".format(self.x, self.y)
