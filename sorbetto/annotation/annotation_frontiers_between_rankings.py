import logging

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.parameterization.parameterization_default import ParameterizationDefault
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore
from sorbetto.tile.abstract_tile import AbstractTile


class FrontiersBetweenRankings(AbstractAnnotation):
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

    def draw(self, tile: AbstractTile, fig, ax) -> None:
        performances = self._performances
        for i, p1 in enumerate(performances):
            for j, p2 in enumerate(performances):
                if i < j:
                    if isinstance(tile.parameterization, ParameterizationDefault):
                        # TDOO: RankingScore.equivalent is only for the default parameterization
                        curve = RankingScore.equivalent(p1, p1)
                        extent = tile.parameterization.getExtent()
                        plt_kwargs = dict()
                        plt_kwargs["color"] = [0.7, 0.7, 0.7]
                        curve.draw(fig, ax, extent, **plt_kwargs)
