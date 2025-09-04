from abc import ABC, abstractmethod
from collections.abc import Iterable as iterable

import numpy as np

from sorbetto.core.entity import Entity


class AbstractRanking(ABC):
    """
    See Axiom 1 in :cite:t:`Pierard2025Foundations`.
    """

    def __init__(self, entities, performance_ordering, name=None):
        assert isinstance(entities, iterable)
        for entity in entities:
            assert isinstance(entity, Entity)

        self._entities = entities
        self._performance_ordering = performance_ordering
        self._name = name

        # TODO: help Sebastien
        # assert isinstance(performance_ordering, PerformanceOrderingInducedByOneScore)
        self._performance_ordering = performance_ordering

        if name is None:
            name = f"ranking of {len(entities)} entities induced by the ordering {performance_ordering.getName()}"
        self._name = name

        ABC.__init__(self)

    @property
    def entities(self) -> iterable:
        return self._entities

    @property
    def performance_ordering(self):
        return self._performance_ordering

    @property
    def name(self):
        return self._name

    @property
    @abstractmethod
    def values(self) -> np.ndarray: ...

    @abstractmethod
    def getAllStableRanks(self) -> np.ndarray: ...

    @abstractmethod
    def getStableRank(self, entity) -> int: ...

    @abstractmethod
    def getAllMinRanks(self) -> np.ndarray: ...

    @abstractmethod
    def getMinRank(self, entity) -> int: ...

    @abstractmethod
    def getAllMaxRanks(self) -> np.ndarray: ...

    @abstractmethod
    def getMaxRank(self, entity) -> int: ...

    @abstractmethod
    def getEntitiesAtRank(self, rank: int) -> list: ...

    def getAllAvgRanks(self) -> np.ndarray:
        min_ranks = self.getAllMinRanks()
        max_ranks = self.getAllMaxRanks()
        ranks = (min_ranks + max_ranks) * 0.5
        return ranks

    def getAvgRank(self, entity) -> float:
        min_ranks = self.getMinRank(entity)
        max_ranks = self.getMaxRank(entity)
        ranks = (min_ranks + max_ranks) * 0.5
        return ranks

    def __str__(self):
        return self.name
