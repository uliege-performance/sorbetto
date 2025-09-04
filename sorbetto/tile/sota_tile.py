from sorbetto.flavor.sota_flavor import SOTAFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.tile.numeric_tile import NumericTile


class SOTATile(NumericTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        flavor: SOTAFlavor,
        resolution: int = 1001,
    ):
        super().__init__(
            name=name,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
        )
        self._performances = self.flavor.performances

    @property
    def flavor(self) -> SOTAFlavor:
        return super().flavor  # type: ignore

    @property
    def performances(self) -> TwoClassClassificationPerformance:
        return self._performances

    @performances.setter
    def performances(self, value: TwoClassClassificationPerformance):
        self._performances = value

    def getExplanation(self) -> str:
        return "Explanation for this tile is not implemented yet"
