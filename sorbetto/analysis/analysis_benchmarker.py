from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.tile.abstract_numeric_tile import AbstractNumericTile
from sorbetto.tile.abstract_symbolic_tile import AbstractSymbolicTile
from sorbetto.tile.value_tile import ValueTile


class AnalysisForBenchmarker(AbstractAnalysis):
    def __init__(self, performances, parameterization, resolution=1001, **kwargs):
        ...  # TODO
        AbstractAnalysis.__init__(self, parameterization, resolution)

    def drawInROC(self, fig, ax):  # and options ?
        ...  # TODO

    def getValueTile(self, entity) -> ValueTile: ...  # TODO

    def getNoSkillTile(
        self,
    ) -> AbstractNumericTile:  # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 9.
        ...  # TODO

    def getRelativeSkillTile(self) -> AbstractNumericTile: ...  # TODO

    def getRankingTile(self, entity) -> AbstractNumericTile: ...  # TODO

    def getAdviceBasedOnRankingTiles(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO

    def getEntityTile(self, rank) -> AbstractSymbolicTile: ...  # TODO

    def getAdviceBasedOnEntityTiles(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO
