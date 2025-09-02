import numpy as np

from sorbetto.core.importance import Importance, _parse_importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
    _parse_performance,
)
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

    def __init__(
        self,
        performance: TwoClassClassificationPerformance,
        name: str = "Unnamed Value Flavor",
    ):
        super().__init__(name)
        self._performance = performance

    @staticmethod
    def _compute(
        importance: Importance | list[Importance] | np.ndarray | None = None,
        performance: TwoClassClassificationPerformance
        | FiniteSetOfTwoClassClassificationPerformances
        | np.ndarray
        | None = None,
        itn: float | np.ndarray | None = None,
        ifp: float | np.ndarray | None = None,
        ifn: float | np.ndarray | None = None,
        itp: float | np.ndarray | None = None,
        ptn: float | np.ndarray | None = None,
        pfp: float | np.ndarray | None = None,
        pfn: float | np.ndarray | None = None,
        ptp: float | np.ndarray | None = None,
    ):
        itn, ifp, ifn, itp = _parse_importance(
            importance=importance, itn=itn, ifp=ifp, ifn=ifn, itp=itp
        )
        ptn, pfp, pfn, ptp = _parse_performance(
            performance=performance, ptn=ptn, pfp=pfp, pfn=pfn, ptp=ptp
        )

        return RankingScore._compute(
            itn=itn,
            ifp=ifp,
            ifn=ifn,
            itp=itp,
            ptn=ptn,
            pfp=pfp,
            pfn=pfn,
            ptp=ptp,
        )

    def __call__(
        self,
        importance: Importance | np.ndarray,
    ) -> float | np.ndarray:
        return self._compute(
            importance=importance,
            performance=self._performance,
        )

    def getDefaultColormap(self):
        return "gray"

    def getLowerBound(self):
        return 0.0

    def getUpperBound(self):
        return 1.0
