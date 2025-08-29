import numpy as np
import scipy.stats

from sorbetto.analysis.abstract_analysis import AbstractAnalysis
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.distribution.distribution_two_class_classification import (
    AbstractDistributionOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore
from sorbetto.tile.abstract_numeric_tile import AbstractNumericTile
from sorbetto.tile.correlation_tile import CorrelationTile


class AnalysisForTheoreticalAnalyst(AbstractAnalysis):
    """
    For an example, see :cite:t:`Pierard2024TheTile-arxiv`, Figure 4.
    For an example, see :cite:t:`Pierard2024TheTile-arxiv`, Figure 7.
    """

    def __init__(
        self,
        performances: np.ndarray
        | AbstractDistributionOfTwoClassClassificationPerformances,
        score: list | callable | RankingScore,
        parameterization: AbstractParameterization,
        resolution: int = 1001,
        colormap: str = None,  # FIXME: it should not be only a string... should include option to clamp colorbar, choose min/max, etc.
        **kwargs,  # TODO: annontations
    ):
        AbstractAnalysis.__init__(self, parameterization, resolution)

        if not isinstance(performances, np.ndarray) and not isinstance(
            performances, AbstractDistributionOfTwoClassClassificationPerformances
        ):
            raise TypeError(
                f"performances must be a numpy array or an instance of AbstractDistributionOfTwoClassClassificationPerformances, got {type(performances)}"
            )
        elif isinstance(performances, np.ndarray):
            # TODO: Shouldn't these following checks be in FiniteSetOfTwoClassClassificationPerformances?
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
            list_performances = FiniteSetOfTwoClassClassificationPerformances(
                performances
            )
            self._performances = list_performances
        elif isinstance(
            performances, AbstractDistributionOfTwoClassClassificationPerformances
        ):
            self._performances = performances

        if (
            not isinstance(score, list)
            and not callable(score)
            and not isinstance(score, RankingScore)
        ):
            raise TypeError(
                f"score must be an instance of RankingScore, a callable, or a list, got {type(score)}"
            )
        elif isinstance(score, list):
            self._score = score
        elif callable(score):
            ptn = np.array([performance.ptn for performance in self._performances])
            pfp = np.array([performance.pfp for performance in self._performances])
            pfn = np.array([performance.pfn for performance in self._performances])
            ptp = np.array([performance.ptp for performance in self._performances])
            self._score = score(ptn, pfp, pfn, ptp)
        elif isinstance(score, RankingScore):
            self._score = [score(performance) for performance in self._performances]

        if not isinstance(parameterization, AbstractParameterization):
            raise TypeError(
                f"parameterization must be an instance of AbstractParameterization, got {type(parameterization)}"
            )
        self._parameterization = parameterization

        if not isinstance(resolution, int):
            raise TypeError(f"resolution must be an integer, got {type(resolution)}")
        self._resolution = resolution

        if colormap is not None and not isinstance(colormap, str):
            raise TypeError(f"colormap must be a string, got {type(colormap)}")
        self._colormap = colormap

    def getPearsonCorrelationTile(
        self,
    ) -> AbstractNumericTile:  # FIXME when CorrelationTile is done
        correlation_fct = scipy.stats.pearsonr
        return CorrelationTile(
            self._parameterization,
            self._score,
            self._performances,
            correlation_fct,
            self._resolution,
            self._colormap,
        )

    def getKendallCorrelationTile(
        self,
    ) -> AbstractNumericTile:  # FIXME when CorrelationTile is done
        correlation_fct = scipy.stats.kendalltau
        return CorrelationTile(
            self._parameterization,
            self._score,
            self._performances,
            correlation_fct,
            self._resolution,
            self._colormap,
        )

    def getSpearmanCorrelationTile(
        self,
    ) -> AbstractNumericTile:  # FIXME when CorrelationTile is done
        correlation_fct = scipy.stats.spearmanr
        return CorrelationTile(
            self._parameterization,
            self._score,
            self._performances,
            correlation_fct,
            self._resolution,
            self._colormap,
        )
