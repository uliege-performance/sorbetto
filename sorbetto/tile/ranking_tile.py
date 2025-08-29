from sorbetto.core.entity import Entity
from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.numeric_tile import AbstractNumericTile


class RankingTile(AbstractNumericTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        symbolic_flavor: AbstractSymbolicFlavor,
        entities_list: list[Entity],
        resolution: int = 1001,
    ):
        super().__init__(
            name, parameterization, symbolic_flavor, entities_list, resolution
        )
