from sorbetto.tile.abstract_tile import AbstractTile


class AbstractSymbolicTile(AbstractTile):
    def __init__(self, name, parameterization, flavor, resolution=1001):
        AbstractTile.__init__(
            self,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
            name=name,
        )
