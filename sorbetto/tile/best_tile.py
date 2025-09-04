from sorbetto.flavor.best_flavor import BestFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.numeric_tile import NumericTile


class BestTile(NumericTile):
    """
    Example of Best Tile: the SOTA Tile.
    """

    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: BestFlavor,
        name: str = "Best Tile",
        resolution: int = 1001,
    ):
        super().__init__(
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
        )

    @property
    def flavor(self) -> BestFlavor:
        return super().flavor  # type: ignore

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self.flavor.performances

    def getExplanation(self) -> str:
        return "Explanation for this tile is not implemented yet"
