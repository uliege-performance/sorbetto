from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D


class Point(AbstractGeometricObject2D):
    def __init__(self, x: float, y: float, name: str | None = None):
        assert isinstance(x, float)
        assert isinstance(y, float)
        self._x = x
        self._y = y
        AbstractGeometricObject2D.__init__(self, name)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def draw(self, fig, ax, extent, **plt_kwargs):
        """_summary_

        Args:
            fig (_type_): _description_
            ax (_type_): _description_
            extent (_type_): (x_min, x_max, y_min, y_max)
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
