import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.core.entity import Entity
from sorbetto.flavor.best_flavor import BestFlavor
from sorbetto.flavor.worst_flavor import WorstFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.best_tile import BestTile
from sorbetto.tile.tile import Tile
from sorbetto.tile.worst_tile import WorstTile


class AnalysisForMethodDesigner(AbstractAnalysis):
    def __init__(
        self,
        entities: list[Entity],
        parameterization: AbstractParameterization,
        resolution: int = 1001,
    ):
        if not isinstance(entities, list):
            raise TypeError(f"entities must be a list, got {type(entities)}")
        for item in entities:
            if not isinstance(item, Entity):
                raise TypeError(
                    f"all items in entities must be instances of Entity, got {type(item)}"
                )

        if not isinstance(parameterization, AbstractParameterization):
            raise TypeError(
                f"parameterization must be an instance of AbstractParameterization, got {type(parameterization)}"
            )

        if not isinstance(resolution, int):
            if isinstance(resolution, float):
                resolution = int(resolution)
            else:
                raise TypeError(f"resolution must be an int, got {type(resolution)}")

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
        if not isinstance(value, list):
            raise TypeError(f"entities must be a list, got {type(value)}")
        for item in value:
            if not isinstance(item, Entity):
                raise TypeError(
                    f"all items in entities must be instances of Entity, got {type(item)}"
                )
        self._entities = value

    @property
    def performances(self):
        return self._performances

    @performances.setter
    def performances(self, value: FiniteSetOfTwoClassClassificationPerformances):
        if not isinstance(value, FiniteSetOfTwoClassClassificationPerformances):
            raise TypeError(
                f"performance must be an instance of FiniteSetOfTwoClassClassificationPerformances, got {type(value)}"
            )
        self._performances = value

    def getNoSkillTile(
        self,
    ) -> Tile:  # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 9.
        ...  # TODO

    def getBaselineValueTile(self, name: str = "Baseline Value Tile") -> Tile:
        flavor = WorstFlavor(performances=self.performances, entity_list=self.entities)
        tile = WorstTile(
            parameterization=self.parameterization,
            flavor=flavor,
            resolution=self._resolution,
            name=name,
        )

        return tile

    def getSOTAValueTile(self, name: str = "SOTA Value Tile") -> Tile:
        flavor = BestFlavor(performances=self.performances, entity_list=self.entities)
        tile = BestTile(
            parameterization=self.parameterization,
            flavor=flavor,
            resolution=self._resolution,
            name=name,
        )

        return tile

    def getValueTile(self, entity: Entity, name: str = "Value Tile") -> Tile:
        return self._getValueTile(entity=entity, name=name)

    def getRankingTile(self, entity: Entity, name: str | None = None) -> Tile:
        if name is None:
            name = f"Ranking Tile for {entity.name}"

        return self._getRankingTile(
            entity=entity, entitiy_list=self.entities, name=name
        )

    def compare_tiles(self, entity: Entity) -> np.ndarray:
        baseline_tile = self.getBaselineValueTile()
        sota_tile = self.getSOTAValueTile()
        value_tile = self.getValueTile(entity=entity)

        difference_baseline_entity = np.abs(
            self._compare_tiles(baseline_tile, value_tile)
        )
        difference_sota_entity = np.abs(self._compare_tiles(sota_tile, value_tile))

        return difference_baseline_entity, difference_sota_entity

    def drawInROC(self, fig: Figure, ax: Axes):  # and options ?
        ...  # TODO

    def getAdvice(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO

    def genTiles(self):
        # TODO: discuss if this should retieve the SOTA tile
        ...
