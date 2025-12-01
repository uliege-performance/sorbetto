from typing import TYPE_CHECKING

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)
from sorbetto.performance.constraint_fixed_prediction_rates import (
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking.constraint_relative_importance_satisfying_unsatisfying import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)
from sorbetto.ranking.ranking_score import RankingScore

if TYPE_CHECKING:
    from sorbetto.tile.symbolic_tile import SymbolicTile
    from sorbetto.tile.tile import Tile


class AnnotationContour(AbstractAnnotation):
    """
    This type of annotation can be used to trace the contours found in
    a symbolic tile on any other tile.
    """

    def __init__(self, src_tile: "SymbolicTile", name: str | None = None, **plt_kwargs):
        from sorbetto.tile.symbolic_tile import SymbolicTile

        assert isinstance(src_tile, SymbolicTile)
        self._src_tile = src_tile

        if name is None:
            name = "contours found in {}".format(src_tile.name)
        else:
            if not isinstance(name, str):
                name = str(name)

        canonical_importance_contours = list()
        for symbol in src_tile.flavor.getCodomain():
            for c in src_tile.getCanonicalImportancesForContours(symbol):
                canonical_importance_contours.append(c)
        self._canonical_importance_contours = canonical_importance_contours

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)
        parameterization = tile.parameterization

        for canonical_importance_contour in self._canonical_importance_contours:
            n = len(canonical_importance_contour)
            xs = np.empty(n)
            ys = np.empty(n)
            for idx in range(n):
                canonical_importance = canonical_importance_contour[idx]
                score = RankingScore(canonical_importance)
                xs[idx] = parameterization.getValueParameter1(score)
                ys[idx] = parameterization.getValueParameter2(score)
            ax.plot(xs, ys, **self._plt_kwargs)

    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool:
        return self._src_tile.isCompatibleWithConstraintOnImportances(constraint)

    def isCompatibleWithConstraintOnClassPriors(
        self, constraint: ConstraintFixedClassPriors
    ) -> bool:
        return self._src_tile.isCompatibleWithConstraintOnClassPriors(constraint)

    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        return self._src_tile.isCompatibleWithConstraintOnPredictionRates(constraint)

    def getConstraintOnImportances(
        self,
    ) -> ConstraintRelativeImportanceSatisfyingUnsatisfying | None:
        return None
        # return self._src_tile.getConstraintOnImportances()

    def getConstraintOnClassPriors(self) -> ConstraintFixedClassPriors | None:
        return None
        # return self._src_tile.getConstraintOnClassPriors()

    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        return None
        # return self._src_tile.getConstraintOnPredictionRates()
