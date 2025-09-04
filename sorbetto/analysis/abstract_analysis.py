from abc import ABC, abstractmethod

import numpy as np

from sorbetto.core.entity import Entity
from sorbetto.flavor.correlation_flavor import CorrelationFlavor
from sorbetto.flavor.entity_flavor import EntityFlavor
from sorbetto.flavor.ranking_flavor import RankingFlavor
from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.tile.correlation_tile import CorrelationTile
from sorbetto.tile.entity_tile import EntityTile
from sorbetto.tile.ranking_tile import RankingTile
from sorbetto.tile.tile import Tile
from sorbetto.tile.value_tile import ValueTile


class AbstractAnalysis(ABC):
    def __init__(
        self, parameterization: AbstractParameterization, resolution: int = 1001
    ):
        ABC.__init__(self)

        if not isinstance(parameterization, AbstractParameterization):
            raise TypeError(
                f"parameterization must be an instance of AbstractParameterization, got {type(parameterization)}"
            )
        self._parameterization = parameterization

        if not isinstance(resolution, int):
            raise TypeError(f"resolution must be an integer, got {type(resolution)}")
        self._resolution = resolution

    @property
    def parameterization(self) -> AbstractParameterization:
        return self._parameterization

    @parameterization.setter
    def parameterization(self, value: AbstractParameterization):
        if not isinstance(value, AbstractParameterization):
            raise TypeError(
                f"parameterization must be an instance of AbstractParameterization, got {type(value)}"
            )
        self._parameterization = value

    @property
    def resolution(self) -> int:
        return self._resolution

    @resolution.setter
    def resolution(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"resolution must be an integer, got {type(value)}")
        self._resolution = value

    @abstractmethod
    def genTiles(self):  # generator
        ...

    def _getValueTile(self, entity: Entity, name: str | None = None) -> ValueTile:
        if name is None:
            name = "Value Tile"

        performance = entity.performance
        flavor = ValueFlavor(performance=performance)
        return ValueTile(
            flavor=flavor,
            parameterization=self.parameterization,
            resolution=self.resolution,
            name=name,
        )

    def _getEntityTile(
        self, rank: int, entities: list[Entity], name: str | None = None
    ) -> EntityTile:
        if name is None:
            name = f"Entity Tile for rank {rank}"

        flavor = EntityFlavor(rank=rank, entity_list=entities)

        entity_tile = EntityTile(
            parameterization=self.parameterization,
            flavor=flavor,
            resolution=self.resolution,
            name=name,
        )

        return entity_tile

    def _getRankingTile(
        self, entity: Entity, entity_list: list[Entity], name: str | None = None
    ) -> RankingTile:
        if name is None:
            name = f"Ranking Tile for entity {entity.name}"
        flavor = RankingFlavor(entity=entity, entity_list=entity_list)
        ranking_tile = RankingTile(
            name=name,
            parameterization=self.parameterization,
            flavor=flavor,
            resolution=self.resolution,
        )

        return ranking_tile

    def _getCorrelationTile(
        self,
        performances: FiniteSetOfTwoClassClassificationPerformances
        | TwoClassClassificationPerformance,
        correlation_fct: str,
        score,
        name="Correlation Tile",
    ):
        correlation_flavor = CorrelationFlavor(
            performances=performances,
            correlation_coefficient=correlation_fct,
            score=score,
        )
        correlation_tile = CorrelationTile(
            name=name,
            parameterization=self.parameterization,
            flavor=correlation_flavor,
            resolution=self.resolution,
        )

        return correlation_tile

    def _getAllValueTiles(self, entities: list[Entity], name="All Value Tiles"):
        tiles = []
        for entity in entities:
            tile = self._getValueTile(entity=entity, name=name)
            tiles.append(tile)
        return tiles

    def _getAllEntityTiles(self, entities: list[Entity], name="All Entity Tiles"):
        tiles = []
        for rank in range(len(entities)):
            tile = self._getEntityTile(rank=rank, entities=entities, name=name)
            tiles.append(tile)
        return tiles

    def _getAllRankingTiles(self, entities: list[Entity], name="All Ranking Tiles"):
        tiles = []
        for entity in entities:
            tile = self._getRankingTile(entity=entity, entitiy_list=entities, name=name)
            tiles.append(tile)
        return tiles

    def _getAllCorrelationTiles(
        self,
        performances: FiniteSetOfTwoClassClassificationPerformances
        | TwoClassClassificationPerformance,
        correlation_fct: str,
        score,
        name="All Correlation Tiles",
    ):
        tiles = []
        for score in score:
            tile = self._getCorrelationTile(
                performances=performances,
                correlation_fct=correlation_fct,
                score=score,
                name=name,
            )
            tiles.append(tile)
        return tiles

    def _compare_tiles(self, tile1: Tile, tile2: Tile) -> np.ndarray:
        if not isinstance(tile1, Tile):
            raise TypeError(f"tile1 must be an instance of Tile, got {type(tile1)}")
        if not isinstance(tile2, Tile):
            raise TypeError(f"tile2 must be an instance of Tile, got {type(tile2)}")
        if tile1.resolution != tile2.resolution:
            raise ValueError("Tiles must have the same resolution to be compared.")
        if tile1.parameterization != tile2.parameterization:
            raise ValueError(
                "Tiles must have the same parameterization to be compared."
            )

        diff = tile1.mat_value - tile2.mat_value
        return diff
