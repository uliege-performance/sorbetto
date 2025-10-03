# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.core.matplotlib_utils import (
    filter_properties_for_plot,
    filter_properties_for_text,
)
from sorbetto.geometry.point import Point
from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)
from sorbetto.performance.constraint_fixed_prediction_rates import (
    ConstraintFixedPredictionRates,
)
from sorbetto.performance.performance_ordering_induced_by_one_score import (
    PerformanceOrderingInducedByOneScore,
)
from sorbetto.ranking.constraint_relative_importance_satisfying_unsatisfying import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)
from sorbetto.ranking.importance import Importance
from sorbetto.ranking.ranking_score import RankingScore

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationText(AbstractAnnotation):
    """
    This type of annotation can be used to place a text on the Tile, next to the point
    corresponding to given importance values.
    """

    def __init__(
        self,
        location: Importance
        | RankingScore
        | PerformanceOrderingInducedByOneScore
        | Point,
        label: str | None = None,
        **plt_kwargs,
    ):
        """
        Initializes a new annotation for a text object.

        Args:
            location (Importance | RankingScore | PerformanceOrderingInducedByOneScore | Point): where to write the label
            label (str | None, optional): what text to write (if None, will
                attempt to use the shortName of the location). Defaults to None.

        Tip: 'color' affects both the text color and the marker color. You can
        override the marker color using 'markerfacecolor' and 'markeredgecolor'.
        """

        assert isinstance(
            location,
            (Importance, RankingScore, PerformanceOrderingInducedByOneScore, Point),
        )
        if isinstance(location, PerformanceOrderingInducedByOneScore):
            assert isinstance(location.score, RankingScore)
        self._location = location

        if label is not None:
            if not isinstance(label, str):
                label = str(label)
        elif isinstance(location, Importance):
            importance = location
            label = importance.name
        elif isinstance(location, RankingScore):
            rankingScore = location
            label = rankingScore.shortLabel
        elif isinstance(location, PerformanceOrderingInducedByOneScore):
            ordering = location
            score = ordering.score
            label = "≲ with " + score.shortLabel

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, label)

    def _whatShouldWeDraw(self, tile: "Tile") -> tuple[float, float, str]:
        from sorbetto.tile.value_tile import ValueTile

        parameterization = tile.parameterization
        location = self._location

        if isinstance(location, PerformanceOrderingInducedByOneScore):
            location = location.score

        if isinstance(location, Importance):
            importance = location
            rankingScore = RankingScore(importance)
            x = parameterization.getValueParameter1(rankingScore)
            y = parameterization.getValueParameter2(rankingScore)
        elif isinstance(location, RankingScore):
            rankingScore = location
            constraint = rankingScore.constraint
            # TODO: implement something more generic than this.
            if constraint is not None and isinstance(tile, ValueTile):
                if not constraint(tile.performance):
                    raise RuntimeError(
                        f"Trying to place a marker for the Ranking Score {rankingScore} with the constraint {constraint} on a Value Tile corresponding to the Performance {tile.performance} incompatible with the constraint."
                    )
            x = parameterization.getValueParameter1(rankingScore)
            y = parameterization.getValueParameter2(rankingScore)
        elif isinstance(location, Point):
            point = location
            x = point.x
            y = point.y
        else:
            assert False  # This should never happen

        return x, y, self.name

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)

        options_for_text = filter_properties_for_text(self._plt_kwargs)
        options_for_plot = filter_properties_for_plot(self._plt_kwargs)

        x, y, label = self._whatShouldWeDraw(tile)

        parameterization = tile.parameterization
        min_x, max_x = parameterization.getBoundsParameter1()
        min_y, max_y = parameterization.getBoundsParameter2()
        try:
            assert x >= min_x and x <= max_x
            assert y >= min_y and y <= max_y
        except AssertionError:
            raise RuntimeError(
                "Trying to place a marker on the Tile outside the parameterization limits."
            )

        ax.plot(x, y, "o", **options_for_plot)

        if x < (2.0 * min_x + 1.0 * max_x) / 3.0:
            dx, ha = 1.0, "left"
        elif x <= (1.0 * min_x + 2.0 * max_x) / 3.0:
            dx, ha = 0.0, "center"
        else:
            dx, ha = -1.0, "right"
        dx *= 0.025 * (max_x - min_x)

        if y < (2.0 * min_y + 1.0 * max_y) / 3.0:
            dy, va = 1.0, "baseline"
        elif y <= (1.0 * min_y + 2.0 * max_y) / 3.0:
            if dx == 0.0:
                dy, va = -1.0, "top"
            else:
                dy, va = 0.0, "center_baseline"
        else:
            dy, va = -1.0, "top"
        dy *= 0.025 * (max_y - min_y)

        ax.text(x + dx, y + dy, label, ha=ha, va=va, **options_for_text)

    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool:
        """
        Checks if this Annotation is compatible with the given constraint on importances. There
        are compatibility issues to be checked when the annotation is placed at a location that
        is either an Importance object or a RankingScore object. Note, however, that there is
        no compatibility issue when the location is PerformanceOrderingInducedByOneScore object,
        as the ordering is the same for a whole bunch of importances.

        Args:
            constraint (ConstraintRelativeImportanceSatisfyingUnsatisfying): a constraint on importances.

        Returns:
            bool: True if this Annotation is compatible with the given constraint, False otherwise.
        """
        assert isinstance(
            constraint, ConstraintRelativeImportanceSatisfyingUnsatisfying
        )
        location = self._location
        if isinstance(location, Importance):
            importance = location
            return constraint(importance)
        elif isinstance(location, RankingScore):
            rankingScore = location
            importance = rankingScore.importance
            return constraint(importance)
        elif isinstance(location, PerformanceOrderingInducedByOneScore):
            return True
        elif isinstance(location, Point):
            return True
        else:
            assert False  # This should never happen

    def isCompatibleWithConstraintOnClassPriors(
        self, constraint: ConstraintFixedClassPriors
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintFixedClassPriors): a constraint on performances.

        Returns:
            bool: True
        """
        assert isinstance(constraint, ConstraintFixedClassPriors)
        return True

    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintFixedPredictionRates): a constraint on performances.

        Returns:
            bool: True
        """
        assert isinstance(constraint, ConstraintFixedPredictionRates)
        return True

    def getConstraintOnImportances(
        self,
    ) -> ConstraintRelativeImportanceSatisfyingUnsatisfying | None:
        if isinstance(self._location, Point):
            # TODO: take a look at the assumptions linked to the geometric object
            raise NotImplementedError()
        else:
            return None

    def getConstraintOnClassPriors(self) -> ConstraintFixedClassPriors | None:
        if isinstance(self._location, Point):
            # TODO: take a look at the assumptions linked to the geometric object
            raise NotImplementedError()
        else:
            return None

    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        if isinstance(self._location, Point):
            # TODO: take a look at the assumptions linked to the geometric object
            raise NotImplementedError()
        else:
            return None
