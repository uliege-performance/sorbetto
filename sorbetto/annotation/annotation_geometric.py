from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


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

        if name is None:
            name = geom.name
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)
        parameterization = tile.parameterization
        extent = parameterization.getExtent()
        self._geom.draw(fig, ax, extent, **self._plt_kwargs)
