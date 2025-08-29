from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.tile.abstract_numeric_tile import AbstractNumericTile
from sorbetto.tile.value_tile import ValueTile


class AnalysisForMethodDesigner(AbstractAnalysis):
    def __init__(
        self,
        performance,
        competitors,
        parameterization,
        resolution=1001,
        **kwargs,
    ):
        ...  # TODO
        AbstractAnalysis.__init__(self, parameterization, resolution)

    def getNoSkillTile(
        self,
    ) -> AbstractNumericTile:  # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 9.
        ...  # TODO

    def getBaselineValueTile(self) -> AbstractNumericTile: ...  # TODO

    def getStateOfTheArtValueTile(self) -> AbstractNumericTile: ...  # TODO

    def getValueTile(self) -> ValueTile: ...  # TODO

    def getRankingTile(self) -> AbstractNumericTile: ...  # TODO

    def drawInROC(self, fig, ax):  # and options ?
        ...  # TODO

    def getAdvice(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO
