from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationImportanceCompass(AbstractAnnotation):
    """
    This type of annotation can be used to place the importance compass on the Tile.
    """

    def __init__(
        self,
        **plt_kwargs,
    ):
        """
        Initializes the annotation.
        """

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, "importance compass")

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)

        parameterization = tile.parameterization
        min_x, max_x = parameterization.getBoundsParameter1()
        min_y, max_y = parameterization.getBoundsParameter2()
        center_x = 0.5 * (min_x + max_x)
        center_y = 0.5 * (min_y + max_y)

        lx = 0.25 * (max_x - min_x)
        ly = 0.25 * (max_y - min_y)
        ax.arrow(
            center_x,
            center_y,
            -lx,
            0,
            head_width=0.05,
            head_length=0.03,
            linewidth=1,
            length_includes_head=True,
            facecolor=None,
            **self._plt_kwargs,
        )
        ax.arrow(
            center_x,
            center_y,
            lx,
            0,
            head_width=0.05,
            head_length=0.03,
            linewidth=1,
            length_includes_head=True,
            facecolor=None,
            **self._plt_kwargs,
        )
        ax.arrow(
            center_x,
            center_y,
            0,
            -ly,
            head_width=0.05,
            head_length=0.03,
            linewidth=1,
            length_includes_head=True,
            facecolor=None,
            **self._plt_kwargs,
        )
        ax.arrow(
            center_x,
            center_y,
            0,
            ly,
            head_width=0.05,
            head_length=0.03,
            linewidth=1,
            length_includes_head=True,
            facecolor=None,
            **self._plt_kwargs,
        )

        x = center_x
        y = 0.2 * min_y + 0.8 * max_y
        text = "more importance on\nfalse negatives ($fn$)"
        ax.text(x, y, text, ha="center", va="bottom", **self._plt_kwargs)

        x = center_x
        y = 0.8 * min_y + 0.2 * max_y
        text = "more importance on\nfalse positives ($fp$)"
        ax.text(x, y, text, ha="center", va="top", **self._plt_kwargs)

        x = 0.2 * min_x + 0.8 * max_x
        y = center_y
        text = "more importance on\ntrue positives ($tp$)"
        ax.text(
            x,
            y,
            text,
            rotation=-90,
            ha="center",
            va="bottom",
            rotation_mode="anchor",
            **self._plt_kwargs,
        )

        x = 0.8 * min_x + 0.2 * max_x
        y = center_y
        text = "more importance on\ntrue negatives ($tn$)"
        ax.text(
            x,
            y,
            text,
            rotation=90,
            ha="center",
            va="bottom",
            rotation_mode="anchor",
            **self._plt_kwargs,
        )
