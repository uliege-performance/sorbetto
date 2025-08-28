import numpy as np

from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.two_class_classification import (
    TwoClassClassificationPerformance,
    # FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore

FiniteSetOfTwoClassClassificationPerformances = list[TwoClassClassificationPerformance]


class RankingFlavor(AbstractNumericFlavor):
    """
    For a given entity in a finite set of entities, the *Ranking Flavor* is the
    mathematical function that gives, to any importance $I$  (that is, some application-
    specific preferences), the rank of that entity.
    For a given set of entities, the ranking is based on the ordering of performances
    induced by the Ranking Score $R_I$ corresponding to the importance $I$.
    """

    def __init__(
        self,
        entities: FiniteSetOfTwoClassClassificationPerformances,
        name: str = "Ranking Flavor",
    ):
        super().__init__(name)
        self.entities = entities

    @property
    def entities(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._entities

    @entities.setter
    def entities(self, value: FiniteSetOfTwoClassClassificationPerformances):
        self._entities = value

    def __call__(
        self,
        importances: Importance,
        evaluated_entity_id: int,
    ):
        values = [
            RankingScore(importances, constraint=None, name=None)(entity)
            for entity in self.entities
        ]
        # FIXME how to get the entities's performance ?

        ranks = np.argsort(np.argsort(values))
        return ranks[evaluated_entity_id]

    def getDefaultColormap(self):
        return "rainbow"
