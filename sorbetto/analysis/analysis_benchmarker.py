from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.core.entity import Entity
from sorbetto.flavor.entity_flavor import EntityFlavor
from sorbetto.flavor.ranking_flavor import RankingFlavor
from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.abstract_numerical_tile import AbstractNumericalTile
from sorbetto.tile.entity_tile import EntityTile
from sorbetto.tile.ranking_tile import RankingTile
from sorbetto.tile.symbolic_tile import AbstractSymbolicTile
from sorbetto.tile.value_tile import ValueTile


class AnalysisForBenchmarker(AbstractAnalysis):
    def __init__(
        self,
        entities: list[Entity],
        parameterization: AbstractParameterization,
        resolution: int = 1001,
        **kwargs,
    ):
        self._entities = entities

        self._performance = FiniteSetOfTwoClassClassificationPerformances(
            [ent.performance for ent in entities]
        )
        AbstractAnalysis.__init__(self, parameterization, resolution)

    @property
    def performance(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performance

    @property
    def entities(self) -> list[Entity]:
        return self._entities

    def drawInROC(self, fig: Figure, ax: Axes):  # and options ?
        ...  # TODO

    def getValueTile(self, entity_id) -> ValueTile:
        flavor = ValueFlavor()
        # get id of the entity
        for i, ent in enumerate(self.entities):
            if ent.name == entity_id:
                entity_index = i
                break

        return ValueTile(
            performance=self._performance,
            parameterization=self._parameterization[entity_index],
            flavor=flavor,
            resolution=self._resolution,
            name=f"Value Tile for {entity_id}",
        )

    def getNoSkillTile(
        self,
    ) -> AbstractNumericalTile:  # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 9.
        ...  # TODO

    def getRelativeSkillTile(self) -> AbstractNumericalTile: ...  # TODO

    def getRankingTile(self, entity_id) -> AbstractNumericalTile:
        flavor = RankingFlavor()
        # get id of the entity
        for i, ent in enumerate(self.entities):
            if ent.name == entity_id:
                entity_index = i
                break

        return RankingTile(
            performance=self._performance,
            entity_id=entity_index,
            parameterization=self._parameterization,
            flavor=flavor,
            resolution=self._resolution,
            name=f"Ranking Tile for {entity_id}",
        )

    def getAdviceBasedOnRankingTiles(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO

    def getEntityTile(self, rank) -> AbstractSymbolicTile:
        flavor = EntityFlavor()
        return EntityTile(
            performance=self._performance,
            parameterization=self._parameterization,
            flavor=flavor,
            resolution=self._resolution,
            name=f"Entity Tile for rank {rank}",
            rank=rank,
        )

    def getAdviceBasedOnEntityTiles(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO
