import numpy as np

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore


class BaselineFlavor(AbstractNumericFlavor):
    """
    For a given rank $r$, the *Entity Flavor* is the mathematical function that
    gives, to any Importance $I$  (that is, some application-specific preferences), the
    entity ranked $r$-th according to the ordering of performances induced by the
    Ranking Score $R_I$ corresponding to the importance $I$.
    """

    def __init__(self, name: str = "Entity Flavor"):
        super().__init__(name)

        self.nb_entities = 0

    def __call__(
        self,
        importance: Importance | np.ndarray,
        performance: FiniteSetOfTwoClassClassificationPerformances,
    ) -> float | np.ndarray:
        self.nb_entities = len(performance)
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
            (FiniteSetOfTwoClassClassificationPerformances,),
        ):
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

        values = RankingScore._compute(
            itn=itn,
            ifp=ifp,
            ifn=ifn,
            itp=itp,
            ptn=ptn,
            pfp=pfp,
            pfn=pfn,
            ptp=ptp,
        )

        return np.min(values, axis=0)

    def getDefaultColormap(self):
        # FIXME discrete colormap
        return "gray"

    def getCoDomain(self):
        """Returns the co-domain of the flavor.
        In Entity flavor, the co-domain is the set of all possible ranks.
        """
        return np.arange(0, len(self.performances))

    def getLowerBound(self):
        return 0.0

    def getUpperBound(self):
        return self.nb_entities - 1
