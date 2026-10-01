# Copyright (c) 2025-2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
import math
from typing import Any, Callable, Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import (
    LinearSegmentedColormap,
)
from scipy import stats
from tqdm import tqdm

from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
    FiniteSetOfTwoClassClassificationPerformances,
    TwoClassClassificationPerformance,
)
from sorbetto.ranking import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
    Importance,
    RankingScore,
)

from ._abstract_numeric_flavor import AbstractNumericFlavor


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
            other_score (Callable[ [ TwoClassClassificationPerformance  |  FiniteSetOfTwoClassClassificationPerformances ], np.ndarray, ]): _description_
            correlation_coefficient_name (Literal[ &quot;pearson_r&quot;, &quot;spearman_rho&quot;, &quot;kendall_tau&quot; ], optional): _description_. Defaults to "pearson_r".
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

        num_correlation_values_to_compute = correlation.size
        for x in (
            # We use tqdm only when there are a lot of values to compute.
            # So, each time this method is called on a single Importance
            # when minimizing or maximizing, tqdm is not used.
            range(value_scores.shape[1])
            if num_correlation_values_to_compute < 100
            else tqdm(range(value_scores.shape[1]))
        ):
            for y in range(value_scores.shape[2]):
                correlation[x, y] = self._correlation_coefficient(
                    self._other_score_values, value_scores[:, x, y]
                ).correlation
        return correlation

    def getDefaultColormap(self):
        N = 2048
        colors1 = plt.get_cmap("gist_rainbow_r", N)
        colors1 = colors1(np.linspace(0, 1, N))
        colors1 = 0.5 + colors1 * 0.5  # whiter
        colors2 = plt.get_cmap("gist_rainbow", N)
        colors2 = colors2(np.linspace(0, 1, N))
        colors = np.vstack((colors1, colors2))
        cmap = LinearSegmentedColormap.from_list("correlation", colors, N=2 * N)
        cmap.set_under("white")
        cmap.set_over("white")
        cmap.set_bad("black")
        return cmap

    def getLowerBound(self) -> float:
        return -1.0

    def getUpperBound(self) -> float:
        return 1.0

    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintRelativeImportanceSatisfyingUnsatisfying): a constraint on importances.

        Returns:
            bool: True
        """
        assert isinstance(
            constraint, ConstraintRelativeImportanceSatisfyingUnsatisfying
        )
        return True

    def isCompatibleWithConstraintOnClassPriors(
        self, constraint: ConstraintFixedClassPriors
    ) -> bool:
        """
        Checks if all performances used in the Flavor's definition satisfy the
        given constraint on performances.

        Args:
            constraint (ConstraintFixedClassPriors): a constraint on performances.

        Returns:
            bool: True if the constraint is satisfied, and False otherwise.
        """
        assert isinstance(constraint, ConstraintFixedClassPriors)
        prior_pos = constraint.getPriorPos()

        min_prior_pos = self._performances.getMinPriorPos()
        if not math.isclose(min_prior_pos, prior_pos):
            return False

        max_prior_pos = self._performances.getMaxPriorPos()
        if not math.isclose(max_prior_pos, prior_pos):
            return False

        return True

    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        """
        Checks if all performances used in the Flavor's definition satisfy the
        given constraint on performances.

        Args:
            constraint (ConstraintFixedPredictionRates): a constraint on performances.

        Returns:
            bool: True if the constraint is satisfied, and False otherwise.
        """
        assert isinstance(constraint, ConstraintFixedPredictionRates)
        rate_pos = constraint.getRatePos()

        min_rate_pos = self._performances.getMinRatePos()
        if not math.isclose(min_rate_pos, rate_pos):
            return False

        max_rate_pos = self._performances.getMaxRatePos()
        if not math.isclose(max_rate_pos, rate_pos):
            return False

        return True
