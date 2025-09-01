import numpy as np

from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.flavor.baseline_flavor import BaselineFlavor
from sorbetto.flavor.sota_flavor import SOTAFlavor
from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.abstract_numerical_tile import AbstractNumericalTile
from sorbetto.tile.value_tile import ValueTile


class AnalysisForMethodDesigner(AbstractAnalysis):
    def __init__(
        self,
        performance: FiniteSetOfTwoClassClassificationPerformances,
        competitors,
        parameterization: AbstractParameterization,
        resolution: int = 1001,
        **kwargs,
    ):
        self._parameterization = parameterization
        self._performance = performance  # what is that ?

        print("Why competitors?")

        AbstractAnalysis.__init__(self, parameterization, resolution)

    @property
    def parameterization(self):
        return self._parameterization

    @property
    def performance(self):
        return self._performance

    def getNoSkillTile(
        self,
    ) -> AbstractNumericalTile:  # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 9.
        ...  # TODO

    def getBaselineValueTile(self) -> AbstractNumericalTile:
        flavor = BaselineFlavor()
        values = ValueTile(
            performance=self._performance,
            parameterization=self._parameterization,
            flavor=flavor,
            resolution=self._resolution,
            name="Baseline Value Tile",
        )

        return np.min(values, axis=0)

    def getStateOfTheArtValueTile(self) -> AbstractNumericalTile:
        flavor = SOTAFlavor()
        values = ValueTile(
            performance=self._performance,
            parameterization=self._parameterization,
            flavor=flavor,
            resolution=self._resolution,
            name="SOTA Value Tile",
        )

        return np.max(values, axis=0)

    def getValueTile(self, id) -> ValueTile:
        flavor = ValueFlavor()
        values = ValueTile(
            performance=self._performance[id],
            parameterization=self._parameterization,
            flavor=flavor,
            resolution=self._resolution,
            name="Value Tile",
        )

        return values

    def getRankingTile(self) -> AbstractNumericalTile: ...  # TODO

    def drawInROC(self, fig, ax):  # and options ?
        ...  # TODO

    def getAdvice(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO

    def genTiles(self):
        # TODO: discuss if this should retieve the SOTA tile
        return self.getStateOfTheArtValueTile()
