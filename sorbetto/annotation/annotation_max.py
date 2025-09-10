from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationMax(AbstractAnnotation):
    """
    This type of annotation can be used to place a text on the Tile, next to the point
    corresponding to the minimum value, the text giving information about this minimum.
    """

    def __init__(
        self,
        **plt_kwargs,
    ):
        """
        Initializes the annotation.
        """

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, "minimum")

    def _whatShouldWeDraw(self, tile: "Tile") -> tuple[float, float, str]:
        from sorbetto.tile.value_tile import ValueTile

        if not isinstance(tile, ValueTile):
            raise RuntimeError(
                "Trying to draw an annotation of type AnnotationMax on a Tile that is not a ValueTile. This makes no sense."
            )

        x, y, v = tile.maximize()
        label = "max: {:g}\n@ ({:g}, {:g})".format(v, x, y)
        return x, y, label

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)

        x, y, label = self._whatShouldWeDraw(tile)

        parameterization = tile.parameterization
        min_x, max_x = parameterization.getBoundsParameter1()
        min_y, max_y = parameterization.getBoundsParameter2()
        try:
            assert x >= min_x and x <= max_x
            assert y >= min_y and y <= max_y
        except AssertionError:
            raise RuntimeError(
                "Trying to place a marker on the Tile outside the parameterization limits."
            )
        center_x = 0.5 * (min_x + max_x)
        center_y = 0.5 * (min_y + max_y)
        ax.plot(x, y, "o", **self._plt_kwargs)
        if x < center_x:
            if y < center_y:
                ax.text(x, y, label, ha="left", va="bottom", **self._plt_kwargs)
            else:
                ax.text(x, y, label, ha="left", va="top", **self._plt_kwargs)
        else:
            if y < center_y:
                ax.text(x, y, label, ha="right", va="bottom", **self._plt_kwargs)
            else:
                ax.text(x, y, label, ha="right", va="top", **self._plt_kwargs)
