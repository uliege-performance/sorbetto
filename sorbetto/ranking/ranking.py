import numpy as np
from .base import AbstractRanking
from ..core.performance_orderingInduced_by_one_score import PerformanceOrderingInducedByOneScore
        


class RankingInducedByScore ( AbstractRanking ):
    """
    See Axiom 1 in :cite:t:`Pierard2025Foundations`.
    """

    def __init__(self, entities, score, name=None):

        # Precompute a few things.
        vals = [score(entity.evaluate()) for entity in entities]
        vals = np.asarray(vals)
        self._vals = vals

        idxs = np.argsort(vals)

        # keep the ordering in cache and create a link from entities to the sorted idxs
        self.sorted_idx = idxs
        self.dico_entities = {entity: idx for idx, entity in zip(idxs, entities)}

        N = len(self._entities)

        # num_lt = [ sum([v < val for v in vals]) for val in vals ]
        num_lt = np.searchsorted(vals, vals, side='left', sorter=idxs)
        self._num_ge = N - num_lt

        # num_le = [ sum([v <= val for v in vals]) for val in vals ]
        num_le = np.searchsorted(vals, vals, side='right', sorter=idxs)
        self._num_gt = N - num_le

        performance_ordering = PerformanceOrderingInducedByOneScore ( score )

        if name is None:
            name = "ranking of {} entities induced by the score {}".format(len(entities), score.getName())

        super().__init__ (entities, performance_ordering, name)

    def getAllValues(self) -> np.ndarray:
        return self._vals

    def getValue(self, entity) -> float:
        
        id_entity = self.dico_entities[entity]
        return self._vals[id_entity]

    def getAllMinRanks(self) -> np.ndarray:
        return 1 + self._num_gt

    def getMinRank(self, entity) -> int:
        id_entity = self.dico_entities[entity]
        return 1 + self._num_gt[id_entity]

    def getAllMaxRanks(self) -> np.ndarray:
        return self._num_ge

    def getMaxRank(self, entity) -> int:
        id_entity = self.dico_entities[entity]
        return self._num_ge[id_entity]

    def getEntitiesAtRank(self, rank: int) -> list:
        """

        :param rank: an integer between 1 and the number of entities.
        :return: The list of all entities e such that min_rank(e) <= rank <= max_rank(e)
        """

        min_ranks_all = self.getAllMinRanks()
        max_ranks_all = self.getAllMaxRanks()

        return [entity for idx, entity in enumerate(self._entities) if min_ranks_all[idx] <= rank <= max_ranks_all[idx]]
