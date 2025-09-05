import logging
from typing import Any, Callable, Literal

import numpy as np
from scipy import stats
from tqdm import tqdm

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.ranking.ranking_score import RankingScore


class CorrelationFlavor(AbstractNumericFlavor):
    """
    For a given performance, the *Correlation Flavor* is the mathematical function
    that gives, to any importance :math:`I`  (that is, some application-specific preferences),
    the correlation, using a defined correlation coefficient (e.g., Pearson's r),
    between a score :math:`X` and the Ranking Score :math:`R_I` corresponding to this
    importance.
    """

    def __init__(
        self,
        performances: FiniteSetOfTwoClassClassificationPerformances,
        score: Callable[
            [
                TwoClassClassificationPerformance
                | FiniteSetOfTwoClassClassificationPerformances
            ],
            np.ndarray,
        ],
        correlation_coefficient: Literal[
            "pearson_r", "spearman_rho", "kendall_tau"
        ] = "pearson_r",
        name: str = "Correlation Flavor",
        colormap: Any = None,
    ):
        super().__init__(name=name, colormap=colormap)
        self._performances = performances
        self._score = score
        self._correlation_coefficient = correlation_coefficient

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performances

    @property
    def score(
        self,
    ) -> Callable[
        [
            TwoClassClassificationPerformance
            | FiniteSetOfTwoClassClassificationPerformances
        ],
        np.ndarray,
    ]:
        return self._score

    @property
    def correlation_coefficient(self) -> str:
        return self._correlation_coefficient

    def __call__(
        self,
        importance: Importance | np.ndarray,
    ):
        try:  # try if X is vectorized
            x_scores: list | np.ndarray = self._score(self._performances)
        except Exception as e:  # else fallback to loop
            logging.warning(
                "The score given to the Correlation Flavor is not vectorized. "
                "Continuing with sequential loop.\n"
                f"Got : {e!r}.\n"
            )
            x_scores = [self._score(p) for p in self._performances]

        value_scores = RankingScore._compute(
            importance=importance, performance=self._performances
        )

        correlation = np.empty((value_scores.shape[1], value_scores.shape[2]))
        if self._correlation_coefficient == "pearson_r":

            def corr_func(x, y):
                return stats.pearsonr(x, y).correlation  # type:ignore
        elif self._correlation_coefficient == "spearman_rho":

            def corr_func(x, y):
                return stats.spearmanr(x, y).correlation  # type:ignore
        elif self._correlation_coefficient == "kendall_tau":

            def corr_func(x, y):
                return stats.kendalltau(x, y).correlation  # type:ignore
        else:
            raise ValueError(
                f"Unknown correlation coefficient: {self._correlation_coefficient}. "
                "Available options are 'pearson_r' and 'spearman_rho' and 'kendall_tau'."
            )

        for x in tqdm(range(value_scores.shape[1])):
            for y in range(value_scores.shape[2]):
                correlation[x, y] = corr_func(x_scores, value_scores[:, x, y])
        return correlation

    def getDefaultColormap(self):
        return "gist_rainbow"

    def getLowerBound(self):
        return -1.0

    def getUpperBound(self):
        return 1.0
