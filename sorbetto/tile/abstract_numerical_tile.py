from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.abstract_tile import AbstractTile


class AbstractNumericalTile(AbstractTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        flavor: AbstractNumericFlavor,
        resolution: int = 1001,
    ):
        super().__init__(name, parameterization, flavor, resolution)
        self._flavor: AbstractNumericFlavor
