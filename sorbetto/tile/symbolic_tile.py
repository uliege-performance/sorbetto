from sorbetto.tile.abstract_tile import AbstractTile


class AbstractSymbolicTile(AbstractTile):
    def __init__(
        self, name, parameterization, symbolic_flavor, entities_list, resolution=1001
    ):
        AbstractTile.__init__(
            self,
            parameterization=parameterization,
            flavor=symbolic_flavor,
            resolution=resolution,
            name=name,
        )
