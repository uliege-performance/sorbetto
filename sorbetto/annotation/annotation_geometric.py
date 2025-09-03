from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D
from sorbetto.tile.asbtract_tile import AbstractTile


class AnnotationGeometric(AbstractAnnotation):
    """
    This type of annotation can be used with any fixed geometric object.
    """

    def __init__(
        self, geom: AbstractGeometricObject2D, name: str | None = None, **plt_kwargs
    ):
        """
        Initializes a new annotation for a geometric object.

        Args:
            geom (AbstractGeometricObject2D): the geometric object.
            name (str | None, optional): the annotation name.
        """

        assert isinstance(geom, AbstractGeometricObject2D)
        self._geom = geom

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: AbstractTile, fig: Figure, ax: Axes) -> None:
        assert isinstance(tile, AbstractTile)
        parameterization = tile.getParameterization()
        min1, max1 = parameterization.getBoundsParameter1()
        min2, max2 = parameterization.getBoundsParameter2()
        extent = [min1, max1, min2, max2]
        self._geom.draw(fig, ax, extent, self._plt_kwargs)
