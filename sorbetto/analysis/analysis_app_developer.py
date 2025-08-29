from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.abstract_symbolic_tile import AbstractSymbolicTile
from sorbetto.tile.value_tile import ValueTile


class AnalysisForAppDeveloper(AbstractAnalysis):
    def __init__(
        self,
        min_a,
        max_a,
        min_b,
        max_b,
        performances,
        parameterization: AbstractParameterization,
        resolution=1001,
        **kwargs,
    ):
        ...  # TODO
        AbstractAnalysis.__init__(self, parameterization, resolution)

    def getEntityTile(self, rank) -> AbstractSymbolicTile: ...  # TODO

    def getValueTile(self, entity) -> ValueTile: ...  # TODO

    def getAdvice(self, fmt) -> str:  # fmt can be: txt, html, latex
        ...  # TODO
