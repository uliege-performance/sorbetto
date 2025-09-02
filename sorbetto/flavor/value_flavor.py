import numpy as np

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
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
        elif isinstance(importance, list):
            itn = np.array([imp.itn for imp in importance])
            ifp = np.array([imp.ifp for imp in importance])
            ifn = np.array([imp.ifn for imp in importance])
            itp = np.array([imp.itp for imp in importance])
        else:
            if (itn is None) or (ifp is None) or (ifn is None) or (itp is None):
                raise ValueError(
                    "Either importance or all itn, ifp, ifn, itp must be provided."
                )

        if isinstance(performance, TwoClassClassificationPerformance):
            ptn = performance.ptn
            pfp = performance.pfp
            pfn = performance.pfn
            ptp = performance.ptp
        elif isinstance(performance, (FiniteSetOfTwoClassClassificationPerformances)):
            ptn = performance.ptn[:, np.newaxis, np.newaxis]
            pfp = performance.pfp[:, np.newaxis, np.newaxis]
            pfn = performance.pfn[:, np.newaxis, np.newaxis]
            ptp = performance.ptp[:, np.newaxis, np.newaxis]
        elif isinstance(performance, np.ndarray):
            assert performance.shape[-1] == 4
            ptn = performance[..., 0][:, np.newaxis, np.newaxis]
            pfp = performance[..., 1][:, np.newaxis, np.newaxis]
            pfn = performance[..., 2][:, np.newaxis, np.newaxis]
            ptp = performance[..., 3][:, np.newaxis, np.newaxis]
        else:
            if (ptn is None) or (pfp is None) or (pfn is None) or (ptp is None):
                raise ValueError(
                    "Either performance or all ptn, pfp, pfn, ptp must be provided."
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
