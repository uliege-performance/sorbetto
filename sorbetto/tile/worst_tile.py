from sorbetto.flavor.worst_flavor import WorstFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.tile.numeric_tile import NumericTile


class WorstTile(NumericTile):
    """
    Example of Worst Tile: the Baseline Tile.
    """

    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: WorstFlavor,
        name: str = "Worst Tile",
        resolution: int = 1001,
    ):
        super().__init__(
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
        )
        self._performances = self.flavor.performances

    @property
    def flavor(self) -> WorstFlavor:
        return super().flavor  # type: ignore

    @property
    def performances(self) -> TwoClassClassificationPerformance:
        return self._performances

    @performances.setter
    def performances(self, value: TwoClassClassificationPerformance):
        self._performances = value

    def getExplanation(self) -> str:
        return "Explanation for this tile is not implemented yet"
