import logging
from typing import TYPE_CHECKING

import matplotlib.ticker as ticker
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationIsovalueCurves(AbstractAnnotation):
    """
    This type of annotation can be used to draw isovalue curves on numeric tile.
    """

    def __init__(self, levels=None, name: str | None = None, **plt_kwargs):
        """_summary_

        Args:
            levels (_type_, optional): _description_. Defaults to None.
            name (str | None, optional): _description_. Defaults to None.
        """

        if levels is not None:
            assert isinstance(levels, list)
            assert all(isinstance(x, float) for x in levels)
        self._levels = levels

        if name is None:
            name = "isovalue curves"
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    @staticmethod
    def _get_auto_levels(mat_values: np.ndarray) -> np.ndarray:
        max_val = np.max(mat_values)
        min_val = np.min(mat_values)

        if np.abs(max_val - min_val) < 1e-6:
            return np.empty(0)

        locator = ticker.MaxNLocator(nbins=20)
        levels = locator.tick_values(min_val, max_val)
        return levels

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.numeric_tile import NumericTile

        if not isinstance(tile, NumericTile):
            message = "It makes no sense to draw isovalue curves on a Tile that is not numeric."
            logging.warning(message)
            return

        mat_values = tile.mat_value
        if mat_values is None:
            message = "It seems that there is no background image in this Tile."
            logging.warning(message)
            return
        assert isinstance(mat_values, np.ndarray)

        levels = self._levels
        if levels is None:
            levels = self._get_auto_levels(mat_values)

        vec_x = tile._vec_x
        assert isinstance(vec_x, np.ndarray)
        vec_y = tile._vec_y
        assert isinstance(vec_y, np.ndarray)

        cs = ax.contour(
            vec_x,
            vec_y,
            mat_values,
            levels=levels,
            colors="cornflowerblue",
            **self._plt_kwargs,
        )
        tiny = 6
        ax.clabel(cs, inline=True, fontsize=tiny, **self._plt_kwargs)
