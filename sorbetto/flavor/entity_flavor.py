import numpy as np

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.performance.two_class_classification import (
    TwoClassClassificationPerformance,
)
from sorbetto.ranking.ranking_score import RankingScore


class EntityFlavor(AbstractSymbolicFlavor):
    """
    For a given rank $r$, the *Entity Flavor* is the mathematical function that
    gives, to any Importance $I$  (that is, some application-specific preferences), the
    entity ranked $r$-th according to the ordering of performances induced by the
    Ranking Score $R_I$ corresponding to the importance $I$.
    """

    def __init__(self, name: str = "Entity Flavor"):
        super().__init__(name)

    def __call__(
        self,
        importance: Importance,
        performances: list[TwoClassClassificationPerformance],
        rank: int,
    ):
        values = [
            RankingScore(importance, constraint=None, name=None)(p)
            for p in performances
        ]  # this is also computed in ranking flavor -> factored out and cached?
        rank_indices = np.argsort(values)  # this as well, but it is pretty cheap

        # FIXME do we return the performance or its index ?
        return performances[rank_indices[rank]]

    def getDefaultColormap(self):
        # FIXME discrete colormap
        return "rainbow"
