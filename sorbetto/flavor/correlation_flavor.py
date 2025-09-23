# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import Any, Callable, Literal

import numpy as np
from scipy import stats

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.ranking.ranking_score import RankingScore


# TODO: rename this class as ScoreCorrelationFlavor or CorrelationWithScoreFlavor?
class CorrelationFlavor(AbstractNumericFlavor):
    """
    For a given performance, the *Correlation Flavor* is the mathematical function
    that gives, to any importance :math:`I`  (that is, some application-specific preferences),
    the correlation, using a defined correlation coefficient (e.g., Pearson's r),
    between the Ranking Score :math:`R_I` corresponding to this
    importance and another score :math:`X`.
    """

    def __init__(
        self,
        performances: FiniteSetOfTwoClassClassificationPerformances,
        other_score: Callable[
            [
                TwoClassClassificationPerformance
                | FiniteSetOfTwoClassClassificationPerformances
            ],
            np.ndarray,
        ],
        correlation_coefficient_name: Literal[
            "pearson_r", "spearman_rho", "kendall_tau"
        ] = "pearson_r",
        name: str = "Correlation Flavor",
        colormap: Any = None,
    ):
        """
        Constructor.

        Args:
            performances (FiniteSetOfTwoClassClassificationPerformances): _description_
            score (Callable[ [ TwoClassClassificationPerformance  |  FiniteSetOfTwoClassClassificationPerformances ], np.ndarray, ]): _description_
            correlation_coefficient (Literal[ &quot;pearson_r&quot;, &quot;spearman_rho&quot;, &quot;kendall_tau&quot; ], optional): _description_. Defaults to "pearson_r".
            name (str, optional): _description_. Defaults to "Correlation Flavor".
            colormap (Any, optional): _description_. Defaults to None.
        """
        assert isinstance(performances, FiniteSetOfTwoClassClassificationPerformances)
        self._performances = performances

        assert callable(other_score)
        try:  # try if X is vectorized
            other_score_values: list | np.ndarray = other_score(self._performances)
        except Exception as e:  # else fallback to loop
            logging.warning(
                "Something went wrong when calling the score. Maybe the score given to the Correlation Flavor is not vectorized? "
                "Continuing with sequential loop.\n"
                f"Got : {e!r}.\n"
            )
            other_score_values = [other_score(p) for p in self._performances]
        self._other_score_values = other_score_values

        assert isinstance(correlation_coefficient_name, str)
        self._correlation_coefficient_name = correlation_coefficient_name
        match correlation_coefficient_name:
            case "pearson_r":
                self._correlation_coefficient = stats.pearsonr
            case "spearman_rho":
                self._correlation_coefficient = stats.spearmanr
            case "kendall_tau":
                self._correlation_coefficient = stats.kendalltau
            case _:
                raise ValueError(
                    f"Unknown correlation coefficient: {correlation_coefficient_name}. "
                    "Available options are 'pearson_r' and 'spearman_rho' and 'kendall_tau'."
                )

        super().__init__(name=name, colormap=colormap)

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performances

    # @property
    # def score(
    #     self,
    # ) -> Callable[
    #     [
    #         TwoClassClassificationPerformance
    #         | FiniteSetOfTwoClassClassificationPerformances
    #     ],
    #     np.ndarray,
    # ]:
    #     return self._other_score

    @property
    def correlation_coefficient(self) -> str:
        return self._correlation_coefficient_name

    def __call__(
        self,
        importance: Importance | np.ndarray,
    ):
        assert (
            isinstance(importance, Importance)
            or isinstance(importance, np.ndarray)
            and importance.shape[-1] == 4
        )  # TODO: RankingScore also supports list[Importance]. Why not here?

        value_scores = RankingScore._compute(
            importance=importance, performance=self._performances
        )

        correlation = np.empty((value_scores.shape[1], value_scores.shape[2]))

        for x in range(value_scores.shape[1]):
            for y in range(value_scores.shape[2]):
                correlation[x, y] = self._correlation_coefficient(
                    self._other_score_values, value_scores[:, x, y]
                ).correlation
        return correlation

    def getDefaultColormap(self):
        return "gist_rainbow"

    def getLowerBound(self) -> float:
        return -1.0

    def getUpperBound(self) -> float:
        return 1.0
