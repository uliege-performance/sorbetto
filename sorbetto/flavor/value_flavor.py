import numpy as np

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.flavor.ranking_flavor import FiniteSetOfTwoClassClassificationPerformances
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
        self,
        importance: Importance | np.ndarray,
        performance: TwoClassClassificationPerformance
        | FiniteSetOfTwoClassClassificationPerformances
        | np.ndarray,
    ) -> float | np.ndarray:
        if isinstance(importance, Importance):
            itn = importance.itn
            ifp = importance.ifp
            ifn = importance.ifn
            itp = importance.itp
        elif isinstance(importance, np.ndarray):
            assert importance.shape[-1] == 4
            itn = importance[..., 0]
            ifp = importance[..., 1]
            ifn = importance[..., 2]
            itp = importance[..., 3]

        if isinstance(
            performance,
            (
                TwoClassClassificationPerformance,
                FiniteSetOfTwoClassClassificationPerformances,
            ),
        ):
            ptn = performance.ptn
            pfp = performance.pfp
            pfn = performance.pfn
            ptp = performance.ptp
        elif isinstance(performance, np.ndarray):
            assert performance.shape[-1] == 4
            ptn = performance[..., 0]
            pfp = performance[..., 1]
            pfn = performance[..., 2]
            ptp = performance[..., 3]

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

    def getDefaultColormap(self):
        return "gray"

    def getLowerBound(self):
        return 0.0

    def getUpperBound(self):
        return 1.0
