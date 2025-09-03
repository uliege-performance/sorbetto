import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.tile import Tile


class NumericTile(Tile):
    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: AbstractNumericFlavor,
        name: str = "Unnamed Numeric Tile",
        resolution: int = 1001,
    ):
        assert isinstance(flavor, AbstractNumericFlavor)
        Tile.__init__(
            self,
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
        )

    def draw(
        self, fig: Figure | None = None, ax: Axes | None = None
    ) -> tuple[Figure, Axes]:
        if fig is None:
            fig = plt.figure()
            ax = fig.gca()
        elif ax is None:
            ax = fig.gca()

        # im =
        ax.imshow(
            self.mat_value,
            origin="lower",
            interpolation="bilinear",
            cmap=self._flavor.getDefaultColormap(),
            extent=self._zoom,  # extent is (left, right, bottom, top)
            vmin=self._flavor.getLowerBound(),
            vmax=self._flavor.getUpperBound(),
        )
        Tile.draw(self, fig, ax)
        return fig, ax

    def getExplanation(self) -> str:
        return "Sorry, we cannont provide yet an explanation for this Tile."
