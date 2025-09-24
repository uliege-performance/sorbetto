from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.core.matplotlib_utils import (
    filter_properties_for_plot,
    filter_properties_for_text,
)

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationMax(AbstractAnnotation):
    """
    This type of annotation can be used to place a text on the Tile, next to the point
    corresponding to the maximum value, the text giving information about this maximum.
    """

    def __init__(
        self,
        **plt_kwargs,
    ):
        """
        Initializes the annotation.
        """

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, "maximum")

    def _whatShouldWeDraw(self, tile: "Tile") -> tuple[float, float, str]:
        from sorbetto.tile.numeric_tile import NumericTile

        if not isinstance(tile, NumericTile):
            raise RuntimeError(
                "Trying to draw an annotation of type AnnotationMax on a Tile that is not a NumericTile. This makes no sense."
            )

        x, y, v = tile.maximize()
        label = "max: {:g}\n@ ({:g}, {:g})".format(v, x, y)
        return x, y, label

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)

        options_for_text = filter_properties_for_text(self._plt_kwargs)
        options_for_plot = filter_properties_for_plot(self._plt_kwargs)

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

        ax.plot(x, y, "o", **options_for_plot)

        if x < (2.0 * min_x + 1.0 * max_x) / 3.0:
            dx, ha = 1.0, "left"
        elif x <= (1.0 * min_x + 2.0 * max_x) / 3.0:
            dx, ha = 0.0, "center"
        else:
            dx, ha = -1.0, "right"
        dx *= 0.025 * (max_x - min_x)

        if y < (2.0 * min_y + 1.0 * max_y) / 3.0:
            dy, va = 1.0, "baseline"
        elif y <= (1.0 * min_y + 2.0 * max_y) / 3.0:
            if dx == 0.0:
                dy, va = -1.0, "top"
            else:
                dy, va = 0.0, "center_baseline"
        else:
            dy, va = -1.0, "top"
        dy *= 0.025 * (max_y - min_y)

        ax.text(x + dx, y + dy, label, ha=ha, va=va, **options_for_text)
