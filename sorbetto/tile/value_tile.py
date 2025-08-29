from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.geometry.pencil import Pencil
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.asbtract_tile import AbstractTile

# from sorbetto.tile.numeric_tile import AbstractNumericTile


class ValueTile(AbstractTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        flavor: AbstractSymbolicFlavor,
        resolution: int = 1001,
    ):
        super().__init__(
            name=name,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
        )

    def getVUT(self):
        """
        Computes the volume

        See :cite:t:`Pierard2024TheTile-arxiv`, Section 3.1. (with default parameterization)
        """

        ...  # TODO

    def asPencil(self) -> Pencil: ...  # TODO
