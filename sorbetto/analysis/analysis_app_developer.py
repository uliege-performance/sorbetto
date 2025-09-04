import os

import matplotlib.pyplot as plt

from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.core.entity import Entity
from sorbetto.flavor.entity_flavor import EntityFlavor
from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.entity_tile import EntityTile
from sorbetto.tile.tile import Tile
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
        self._performances = FiniteSetOfTwoClassClassificationPerformances(
            [entity.performance for entity in entities]
        )

        AbstractAnalysis.__init__(self, parameterization, resolution)

    @property
    def entities(self) -> list[Entity]:
        return self._entities

    @entities.setter
    def entities(self, value: list[Entity]):
        self._entities = value

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performances

    @performances.setter
    def performances(self, value: FiniteSetOfTwoClassClassificationPerformances):
        self._performances = value

    def getEntityTile(self, rank) -> EntityTile:
        flavor = EntityFlavor(rank=rank, entity_list=self.entities)

        entity_tile = EntityTile(
            parameterization=self._parameterization,
            flavor=flavor,
            resolution=self._resolution,
            name=f"Entity Tile for rank {rank}",
        )

        return entity_tile

    def getValueTile(self, entity: Entity, name: str | None = None) -> ValueTile:
        if name is None:
            name = f"Value Tile for {entity.name}"
        return self._getValueTile(entity=entity, name=name)

    def getCorrelationTile(self, score, correlation_fct):
        performances = self.performances
        return self._getCorrelationTile(
            performances=performances,
            correlation_fct=correlation_fct,
            name="Correlation Tile",
            score=score,
        )

    def getRankingTile(self, entity: Entity, rank: int):
        return self._getRankingTile(
            entity=entity,
            entitiy_list=self.entities,
            name=f"Ranking Tile for rank {rank}",
        )

    def saveAllValueTiles(self, save_dir: str | None = None):
        if save_dir is None:
            raise ValueError("save_dir must be specified")

        os.makedirs(save_dir, exist_ok=True)

        for entity in self.entities:
            value_tile = self.getValueTile(entity)

            filename = os.path.join(save_dir, f"value_tile_{entity.name}.png")
            fig, ax = value_tile.draw()

            plt.savefig(filename)
            plt.close()

    def saveAllEntityTiles(self, save_dir: str | None = None):
        if save_dir is None:
            raise ValueError("save_dir must be specified")

        os.makedirs(save_dir, exist_ok=True)

        for rank in range(len(self.entities)):
            entity_tile = self.getEntityTile(rank)

            filename = os.path.join(save_dir, f"entity_tile_{rank}.png")
            fig, ax = entity_tile.draw()

            plt.savefig(filename)
            plt.close()

    def getAdvice(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO

    def genTiles(self):
        # TODO ?
        raise NotImplementedError("Method not implemented yet.")
