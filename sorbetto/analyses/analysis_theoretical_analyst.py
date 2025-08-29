from sorbetto.analyses.abstract_analysis import AbstractAnalysis
from sorbetto.tile.abstract_numeric_tile import AbstractNumericTile


class AnalysisForTheoreticalAnalyst(AbstractAnalysis):
    """
    For an example, see :cite:t:`Pierard2024TheTile-arxiv`, Figure 4.
    For an example, see :cite:t:`Pierard2024TheTile-arxiv`, Figure 7.
    """

    def __init__(
        self, performances, score, parameterization, resolution=1001, **kwargs_options
    ):
        ...  # TODO
        AbstractAnalysis.__init__(self, parameterization, resolution)

    def getPearsonCorrelationTile(self) -> AbstractNumericTile: ...  # TODO

    def getKendallCorrelationTile(self) -> AbstractNumericTile: ...  # TODO

    def getSpearmanCorrelationTile(self) -> AbstractNumericTile: ...  # TODO
