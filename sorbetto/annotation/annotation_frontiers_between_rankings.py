import logging
from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.parameterization.parameterization_default import ParameterizationDefault
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationFrontiersBetweenRankings(AbstractAnnotation):
    def __init__(
        self, performnances: FiniteSetOfTwoClassClassificationPerformances, name=None
    ):
        assert isinstance(performnances, FiniteSetOfTwoClassClassificationPerformances)
        self._performances = performnances
        if len(performnances) >= 15:
            message = "{} froentiers are going to be computed. That's a lot!".format(
                len(performnances)
            )
            logging.warning(message)
        super().__init__(name)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)

        plt_kwargs = dict()
        plt_kwargs["color"] = [0.7, 0.7, 0.7]

        if isinstance(tile.parameterization, ParameterizationDefault):
            # TDOO: RankingScore.equivalent is only for the default parameterization
            extent = tile.parameterization.getExtent()
            performances = self._performances
            for i, p1 in enumerate(performances):
                for j, p2 in enumerate(performances):
                    if i < j:
                        curve = RankingScore.equivalent(p1, p2)
                        curve.draw(fig, ax, extent, **plt_kwargs)
        else:
            message = (
                "AnnotationFrontiersBetweenRankings only works for ParameterizationDefault in this version.\n"
                "See RankingScore.equivalent for more information about this limitation."
            )
            logging.warning(message)
