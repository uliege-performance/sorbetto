import numpy as np

from sorbetto.core.entity import Entity
from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore


class RankingFlavor(AbstractNumericFlavor):
    """
    For a given rank $r$, the *Entity Flavor* is the mathematical function that
    gives, to any Importance $I$  (that is, some application-specific preferences), the
    entity ranked $r$-th according to the ordering of performances induced by the
    Ranking Score $R_I$ corresponding to the importance $I$.
    """

    def __init__(
        self,
        entity: Entity,
        entity_list: list[Entity],
        name: str = "Unnamed Ranking Flavor",
    ):
        super().__init__(name)
        self._entity = entity
        self._entity_list = entity_list
        self._nb_entities = len(entity_list)
        self._performances = FiniteSetOfTwoClassClassificationPerformances(
            [e.performance for e in entity_list]
        )
        for i, e in enumerate(self._entity_list):
            if e is entity:
                self._id_entity = i
                break
        else:
            raise ValueError("The given entity was not found in the given entity list.")

    @property
    def entity(self) -> Entity:
        return self._entity

    @property
    def entity_list(self) -> list[Entity]:
        return self._entity_list

    @property
    def nb_entities(self) -> int:
        return self._nb_entities

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performances

    @property
    def id_entity(self) -> int:
        return self._id_entity

    def __call__(
        self,
        importance: Importance | np.ndarray,
    ) -> float | np.ndarray:
        values = RankingScore._compute(
            importance=importance, performance=self._performances
        )

        # TODO check behaviour of argsort(argsort()) with multiple identical values
        # and allow user to choose between 'min', 'max', 'mean', ...
        ranks = np.argsort(-values, axis=0)
        rank_entities = np.argsort(ranks, axis=0)
        return rank_entities[self._id_entity]

    def getDefaultColormap(self):
        # FIXME discrete colormap
        return "rainbow"

    def getLowerBound(self):
        return 0.0

    def getUpperBound(self):
        return self._nb_entities - 1
