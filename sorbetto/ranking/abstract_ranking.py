from abc import ABC, abstractmethod
from collections.abc import Iterable as iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

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

    def draw(
        self,
        fig: Figure | None = None,
        ax: Axes | None = None,
        value_axis_label: str = "",
    ) -> tuple[Figure, Axes]:
        if fig is None:
            fig = plt.figure()
            ax = fig.gca()
        elif ax is None:
            ax = fig.gca()

        u = 0.03

        # value axis
        ax.plot([0, 0], [0, 1.1], "k-")
        ax.plot([-u, 0, u], [1.1 - u, 1.1, 1.1 - u], "k-")
        ax.plot([-u, u], [0, 0], "k-")
        ax.text(-2 * u, 0, "0", ha="right", va="center")
        ax.plot([-u, u], [1, 1], "k-")
        ax.text(-2 * u, 1, "1", ha="right", va="center")
        ax.text(
            0,
            1.1 + u,
            value_axis_label,
            ha="left",
            va="bottom",
        )

        n = len(self.entities)
        values = self.values

        if n == 1:
            e = self.entities[0]

            value = values[0]
            ax.plot([-u, u], [value, value], "-", c=e.color)

            y = 0.5
            ax.plot([u, 0.5 - u], [value, y], ":", c=e.color)

            y = 0.5
            ax.plot([0.5 - u, 0.5 + u], [y, y], "-", c=e.color)
            label = "{} ({:g})".format(e.name, value)
            ax.text(0.5 + 2 * u, y, label, ha="left", va="center", c=e.color)

        else:
            min_ranks = self.getAllMinRanks()
            max_ranks = self.getAllMaxRanks()
            stable_ranks = self.getAllStableRanks()

            for i, e in enumerate(self.entities):
                value = values[i]

                min_rank = min_ranks[i]
                max_rank = max_ranks[i]
                if min_rank != max_rank:
                    ax.plot([-u, u], [value, value], "k-")

                    min_y = (n - min_rank) / (n - 1)
                    max_y = (n - max_rank) / (n - 1)
                    ax.plot([0.5 - u, 0.5 - u], [min_y, max_y], "k-")

                    mean_rank = (min_rank + max_rank) / 2
                    y = (n - mean_rank) / (n - 1)
                    ax.plot([u, 0.5 - u], [value, y], "k:")

                else:
                    ax.plot([-u, u], [value, value], "-", c=e.color)

                    mean_rank = (min_rank + max_rank) / 2
                    y = (n - mean_rank) / (n - 1)
                    ax.plot([u, 0.5 - u], [value, y], ":", c=e.color)

                stable_rank = stable_ranks[i]
                y = (n - stable_rank) / (n - 1)
                ax.plot([0.5 - u, 0.5 + u], [y, y], "-", c=e.color)
                label = "{} ({:.3f})".format(e.name, value)
                ax.text(0.5 + 2 * u, y, label, ha="left", va="center", c=e.color)

        ax.set_xlim([-0.2, 1.2])
        ax.set_ylim([-0.1, 1.3])
        ax.axis("off")

        return fig, ax

    def __str__(self):
        return self.name
