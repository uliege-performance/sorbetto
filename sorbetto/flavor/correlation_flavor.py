import logging
from typing import Callable, Literal

from scipy import stats

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class CorrelationFlavor(AbstractNumericFlavor):
    """
    For a given performance, the *Correlation Flavor* is the mathematical function
    that gives, to any importance $I$  (that is, some application-specific preferences),
    the correlation, using a defined correlation coefficient (e.g., Pearson's r),
    between a score $X$ and the Ranking Score $R_I$ corresponding to this
    importance.
    """

    def __init__(self, name: str = "Correlation Flavor"):
        super().__init__(name)

    def __call__(
        self,
        importance: Importance,
        performances: list[TwoClassClassificationPerformance],
        X: Callable[
            [
                list[TwoClassClassificationPerformance]
                | TwoClassClassificationPerformance
            ],
            float,
        ],
        correlation_coefficient: Literal["pearsonr", "spearmanr"],
    ):
        try:  # try if X is vectorized
            x_scores = X(performances)
        except Exception as e:  # else fallback to loop
            logging.warning(
                "The score given to the Correlation Flavor is not vectorized. "
                "Continuing with sequential loop.\n"
                f"Got : {e!r}.\n"
            )
            x_scores = [X(p) for p in performances]

        value_flavor = ValueFlavor()
        value_scores = [value_flavor(importance, p) for p in performances]

        if correlation_coefficient == "pearsonr":
            return stats.pearsonr(x_scores, value_scores)

        elif correlation_coefficient == "spearmanr":
            return stats.spearmanr(x_scores, value_scores)
        else:
            raise ValueError(
                f"Unknown correlation coefficient: {correlation_coefficient}. "
                "Available options are 'pearsonr' and 'spearmanr'."
            )

        # TODO how do we select the coefficient ? add more options ?

    def getDefaultColormap(self):
        return "gray"

    def getLowerBound(self):
        return -1.0

    def getUpperBound(self):
        return 1.0
