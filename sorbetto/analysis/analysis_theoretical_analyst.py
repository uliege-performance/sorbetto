import numpy as np
import scipy.stats

from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.distribution.distribution_two_class_classification import (
    AbstractDistributionOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification import (
    FiniteSetOfTwoClassClassificationPerformances
)
from sorbetto.tile.abstract_numeric_tile import AbstractNumericTile


class AnalysisForTheoreticalAnalyst(AbstractAnalysis):
    """
    For an example, see :cite:t:`Pierard2024TheTile-arxiv`, Figure 4.
    For an example, see :cite:t:`Pierard2024TheTile-arxiv`, Figure 7.
    """

    def __init__(
        self,
        performances: np.ndarray
        | AbstractDistributionOfTwoClassClassificationPerformances,
        score: list | callable,
        parameterization: AbstractParameterization,
        resolution=1001,
        **kwargs,
    ):
        ...  # TODO
        AbstractAnalysis.__init__(self, parameterization, resolution)

        # TODO: Shouldn't these checks be in FiniteSetOfTwoClassClassificationPerformances?       
        if isinstance(performances, np.ndarray):
            if performances.ndim != 2 or performances.shape[1] != 4:
                raise ValueError(
                    f"performances must be a 2D numpy array with shape (n, 4), got {performances.shape}"
                )
            if not np.issubdtype(performances.dtype, np.floating):
                raise TypeError(
                    f"performances must be a numpy array of floats, got {performances.dtype}"
                )
            if np.any(performances < 0) or np.any(performances > 1):
                raise ValueError(
                    "performances must be in the range [0, 1], got values outside this range"
                )
            
            list_performances = FiniteSetOfTwoClassClassificationPerformances(performances)

                
                
            self._performances = 

    def getPearsonCorrelationTile(self) -> AbstractNumericTile:  # TODO
        correlation_fct = scipy.stats.pearsonr

    def getKendallCorrelationTile(self) -> AbstractNumericTile:  # TODO
        correlation_fct = scipy.stats.kendalltau

    def getSpearmanCorrelationTile(self) -> AbstractNumericTile:  # TODO
        correlation_fct = scipy.stats.spearmanr
