import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.core.performance_ordering_induced_by_one_score import (
    PerformanceOrderingInducedByOneScore,
)
from sorbetto.ranking.abstract_ranking import AbstractRanking


class RankingInducedByScore(AbstractRanking):
    """
    See Axiom 1 in :cite:t:`Pierard2025Foundations`.
    """

    def __init__(self, entities, score, name=None):
        # Precompute a few things.
        vals = [score(entity.performance) for entity in entities]
        vals = np.asarray(vals)
        self._vals = vals

        idxs = np.argsort(vals, kind="stable")

        # keep the ordering in cache and create a link from entities to the sorted idxs
        self._sorted_idx = idxs
        self._dico_entities = {entity: idx for idx, entity in zip(idxs, entities)}

        N = len(entities)

        # num_lt = [ sum([v < val for v in vals]) for val in vals ]
        num_lt = np.searchsorted(vals, vals, side="left", sorter=idxs)
        self._num_ge = N - num_lt

        # num_le = [ sum([v <= val for v in vals]) for val in vals ]
        num_le = np.searchsorted(vals, vals, side="right", sorter=idxs)
        self._num_gt = N - num_le

        performance_ordering = PerformanceOrderingInducedByOneScore(score)

        if name is None:
            name = "ranking of {} entities induced by the score {}".format(
                len(entities), score.name
            )

        super().__init__(entities, performance_ordering, name)

    @property
    def values(self) -> np.ndarray:
        return self._vals

    def getAllStableRanks(self) -> np.ndarray:
        # In case of equivalence (equal values), the returned rank decreases with the
        # position in the list of entities.
        # TODO: Change this implementation to mimic what we did in RankingFlavor for consistency (only).
        # (or vice-versa?)
        sorted_idx = self._sorted_idx
        N = sorted_idx.size
        tmp = np.empty(N, dtype=int)
        tmp[sorted_idx] = np.arange(N)
        return N - tmp

    def getStableRank(self, entity) -> int:
        id_entity = self._dico_entities[entity]
        # TODO: optimize this.
        all_stable_ranks = self.getAllStableRanks()
        return all_stable_ranks[id_entity]

    def getAllMinRanks(self) -> np.ndarray:
        return 1 + self._num_gt

    def getMinRank(self, entity) -> int:
        id_entity = self._dico_entities[entity]
        return 1 + self._num_gt[id_entity]

    def getAllMaxRanks(self) -> np.ndarray:
        return self._num_ge

    def getMaxRank(self, entity) -> int:
        id_entity = self._dico_entities[entity]
        return self._num_ge[id_entity]

    def getEntitiesAtRank(self, rank: int) -> list:
        """

        :param rank: an integer between 1 and the number of entities.
        :return: The list of all entities e such that min_rank(e) <= rank <= max_rank(e)
        """

        min_ranks_all = self.getAllMinRanks()
        max_ranks_all = self.getAllMaxRanks()

        return [
            entity
            for idx, entity in enumerate(self._entities)
            if min_ranks_all[idx] <= rank <= max_ranks_all[idx]
        ]

    def draw(
        self,
        fig: Figure | None = None,
        ax: Axes | None = None,
        value_axis_label: str = "",
    ) -> tuple[Figure, Axes]:
        if value_axis_label == "":
            score = self.performance_ordering.score
            value_axis_label = 'Value taken by the score\n"{}"'.format(score.name)
        return AbstractRanking.draw(self, fig, ax, value_axis_label)
