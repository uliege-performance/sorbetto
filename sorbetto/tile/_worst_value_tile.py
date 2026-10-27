# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import override

from sorbetto.flavor import WorstValueFlavor
from sorbetto.parameterization import (
    AbstractParameterization,
)
from sorbetto.performance import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking import ConstraintCanonical, RankingScore

from ._numeric_tile import NumericTile


class WorstValueTile(NumericTile):
    """
    Example of Worst Value Tile: the Baseline Tile.
    """

    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: WorstValueFlavor,
        name: str = "Worst Value Tile",
        resolution: int = 1001,
        colorbar_mode: str = "default",
    ):
        assert isinstance(parameterization, AbstractParameterization)
        assert isinstance(flavor, WorstValueFlavor)
        assert isinstance(name, str)
        assert isinstance(resolution, int)
        assert resolution > 0

        super().__init__(
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
            colorbar_mode=colorbar_mode,
            base_constraint_on_importances=ConstraintCanonical(),
        )

    @property
    def flavor(self) -> WorstValueFlavor:
        # We override the property's getter to ensure the right type of flavor.
        flavor = super().flavor
        assert isinstance(flavor, WorstValueFlavor)
        return flavor

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self.flavor.performances

    @override
    def minimize(self, precision: float = 1e-6) -> tuple[float, float, float]:
        assert isinstance(precision, float)
        assert precision >= 0.0

        parameterization = self.parameterization

        # With the default parameterization, it has been demonstrated in
        # :cite:t:`Pierard2024TheTile-arxiv` that the values taken by the
        # canonical ranking scores on horizontal and vertical lines
        # correspond to some f-means. So, at the extremities, on has the
        # minimal and maximal values. As a consequence, to find a point
        # of the Tile at which the value is minimal or maximal, it suffices
        # to look at the four corners. This can be generalized to all
        # parameterizations: the value taken by any canonical ranking score
        # is bounded by TNR, TPR, NPV, and PPV.

        # TODO: be sure that this is correct when the value is undefined at some corners!

        best_x = math.nan
        best_y = math.nan
        best_val = math.inf

        def update_for_min(ranking_score):
            nonlocal best_x
            nonlocal best_y
            nonlocal best_val

            for performance in self.flavor.performances:
                x = parameterization.getValueParameter1(ranking_score)
                y = parameterization.getValueParameter2(ranking_score)
                val = ranking_score(performance)
                if val < best_val:
                    best_x = x
                    best_y = y
                    best_val = val

        update_for_min(RankingScore.getTrueNegativeRate())
        update_for_min(RankingScore.getTruePositiveRate())
        update_for_min(RankingScore.getNegativePredictiveValue())
        update_for_min(RankingScore.getPositivePredictiveValue())

        return best_x, best_y, best_val

    def getExplanation(self) -> str:
        return "Explanation for this tile is not implemented yet"
