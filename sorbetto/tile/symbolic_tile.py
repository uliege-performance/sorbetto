from sorbetto.tile.abstract_tile import AbstractTile


class AbstractSymbolicTile(AbstractTile):
    def __init__(self, name, parameterization, flavor, entities_list, resolution=1001):
        self._entities = entities_list
        AbstractTile.__init__(
            self,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
            name=name,
        )

    @property
    def entities(self):
        return self._entities
