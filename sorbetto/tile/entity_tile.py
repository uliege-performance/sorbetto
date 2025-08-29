from sorbetto.core.entity import Entity
from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.symbolic_tile import AbstractSymbolicTile


class EntityTile(AbstractSymbolicTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        symbolic_flavor: AbstractSymbolicFlavor,
        entities_list: list[Entity],
        resolution: int = 1001,
    ):
        self._mapper = {i: entity for i, entity in enumerate(entities_list)}

        super().__init__(
            name, parameterization, symbolic_flavor, entities_list, resolution
        )

    @property
    def mapper(self) -> dict[int, Entity]:
        return self._mapper
