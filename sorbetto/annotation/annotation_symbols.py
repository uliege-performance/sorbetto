from typing import TYPE_CHECKING

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy.ndimage import generate_binary_structure, label

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.core.matplotlib_utils import filter_properties_for_text

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationSymbols(AbstractAnnotation):
    """
    This type of annotation can be used to write over a SymbolicTile the names
    of the symbols that are present in this Tile, above them, for the large
    enough connected components.
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

        from sorbetto.tile.symbolic_tile import SymbolicTile

        if not isinstance(tile, SymbolicTile):
            message = "Trying to draw an annotation of type AnnotationSymbols on a Tile that is not a SymbolicTile. This makes no sense."
            raise RuntimeError(message)

        options_for_text = filter_properties_for_text(self._plt_kwargs)

        # parameterization = tile.parameterization
        # min_x, max_x = parameterization.getBoundsParameter1()
        # min_y, max_y = parameterization.getBoundsParameter2()

        struct = generate_binary_structure(2, 3)

        vec_x = tile._vec_x
        vec_j = np.linspace(0, vec_x.size - 1, vec_x.size)
        vec_y = tile._vec_y
        vec_i = np.linspace(0, vec_y.size - 1, vec_y.size)
        mat_value = tile._mat_value

        values = np.unique(mat_value)
        for value in values:
            symbol = tile.flavor.reverse_mapper(value)

            # find each connected component (cc) and label its gravity center
            labeled_array, num_cc = label(mat_value == value, structure=struct)
            for cc in range(1, num_cc + 1):
                all_i, all_j = np.where(labeled_array == cc)

                # compute the relative size of the zone in the Tile
                coverage = all_i.size / mat_value.size
                if coverage >= 0.025:  # large enough
                    # compute the gravity center in matrix coordinates
                    mean_i = all_i.mean()
                    mean_j = all_j.mean()
                    i = int(np.round(mean_i))
                    j = int(np.round(mean_j))
                    if mat_value[i, j] != value:
                        # the gravity center does not belong to the zone :-(
                        # let's find the point of the zone that is the closest to the gravity center.
                        di = all_i - i
                        dj = all_j - j
                        d2 = di * di + dj * dj
                        k = np.where(d2 == np.min(d2))
                        j = all_j[k][0]
                        i = all_i[k][0]
                        # TODO: now, (i, j) is on the border of the the zone. We can still improve it
                        # by "pushing" the point inside the zone.
                    x = np.interp(mean_j, vec_j, vec_x)
                    y = np.interp(mean_i, vec_i, vec_y)
                    tiny = 6
                    ax.text(
                        x,
                        y,
                        symbol,
                        ha="center",
                        va="center",
                        color="black",
                        fontsize=tiny,
                        **options_for_text,
                    )
