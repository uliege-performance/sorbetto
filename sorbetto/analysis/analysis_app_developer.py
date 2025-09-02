from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.core.entity import Entity
from sorbetto.flavor.entity_flavor import EntityFlavor
from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.entity_tile import EntityTile
from sorbetto.tile.symbolic_tile import AbstractSymbolicTile
from sorbetto.tile.value_tile import ValueTile


class AnalysisForAppDeveloper(AbstractAnalysis):
    def __init__(
        self,
        entities: list[Entity],
        parameterization: AbstractParameterization,
        resolution: int = 1001,
        **kwargs,
    ):
        self._entities = entities

        AbstractAnalysis.__init__(self, parameterization, resolution)

    def getEntityTile(self, rank) -> AbstractSymbolicTile:
        flavor = EntityFlavor()

        entity_tile = EntityTile(
            entities_list=self._entities,
            parameterization=self._parameterization,
            flavor=flavor,
            resolution=self._resolution,
            name=f"Entity Tile for rank {rank}",
            rank=rank,
        )

        return entity_tile

    def getValueTile(self, entity: Entity) -> ValueTile:
        # TODO: choose if entity or entity_name /entity_id
        flavor = ValueFlavor()
        performance = entity.performance
        return ValueTile(
            performance=performance,
            flavor=flavor,
            parameterization=self._parameterization,
            resolution=self._resolution,
        )

    def getAdvice(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO
