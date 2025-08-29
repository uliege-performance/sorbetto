from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.two_class_classification import (
    TwoClassClassificationPerformance,
)
from sorbetto.ranking.ranking_score import RankingScore


class ValueFlavor(AbstractNumericFlavor):
    """
    For a given performance, the *Value Flavor* is the mathematical function that
    gives, to any importance $I$  (that is, some application-specific preferences), the
    value taken by the Ranking Score $R_I$ corresponding to this importance.
    """

    def __init__(self, name: str = "Value Flavor"):
        super().__init__(name)

    def __call__(
        self, importance: Importance, performance: TwoClassClassificationPerformance
    ):
        rs = RankingScore(importance, constraint=None, name=None)

        return rs(performance)

    def getDefaultColormap(self):
        return "gray"

    def getLowerBound(self):
        return 0.0

    def getUpperBound(self):
        return 1.0
