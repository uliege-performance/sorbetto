from ..core.entity import Entity
from abc import abstractmethod
from collections.abc import Iterable as iterable
import numpy as np


class AbstractRanking:
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

    def getEntities(self) -> iterable:
        return self._entities

    def getPerformanceOrdering(self):
        return self._performance_ordering
    
    def getName(self):
        return self._name

    @abstractmethod
    def getAllValues(self) -> np.ndarray:
        raise NotImplementedError()

    @abstractmethod
    def getValue(self, entity) -> float:
        raise NotImplementedError()

    @abstractmethod
    def getAllMinRanks(self) -> np.ndarray:
        raise NotImplementedError()

    @abstractmethod
    def getMinRank(self, entity) -> int:
        raise NotImplementedError()

    @abstractmethod
    def getAllMaxRanks(self) -> np.ndarray:
        raise NotImplementedError()

    @abstractmethod
    def getMaxRank(self, entity) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def getEntitiesAtRank(self, rank: int) -> list:
        raise NotImplementedError()

    def getAllAvgRanks(self) -> np.ndarray:
        min_ranks = self.getAllMinRanks()
        max_ranks = self.getAllMaxRanks()
        ranks = (min_ranks + max_ranks) * 0.5
        return ranks

    def getAvgRank(self, entity) -> float:
        min_ranks = self.getMinRanks(entity)
        max_ranks = self.getMaxRanks(entity)
        ranks = (min_ranks + max_ranks) * 0.5
        return ranks

    def __str__(self):
        return self.getName()