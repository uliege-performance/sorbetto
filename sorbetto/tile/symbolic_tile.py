import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.tile import Tile


class SymbolicTile(Tile):
    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: AbstractSymbolicFlavor,
        name: str = "Symbolic Tile",
        resolution: int = 1001,
        disable_colorbar: bool = False,
    ):
        assert isinstance(flavor, AbstractSymbolicFlavor)
        Tile.__init__(
            self,
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
            disable_colorbar=disable_colorbar,
        )

    @property
    def flavor(self) -> AbstractSymbolicFlavor:
        return super().flavor  # type: ignore

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
            cmap=self.flavor.colormap,
            extent=self._zoom,  # extent is (left, right, bottom, top)
            vmin=0,
            vmax=len(self.flavor.getCodomain()) - 1,
        )
        Tile.draw(self, fig, ax)
        return fig, ax

    def getExplanation(self) -> str:
        return "Sorry, we cannont provide yet an explanation for this Tile."
