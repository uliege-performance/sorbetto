# Copyright (c) 2025-2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import TYPE_CHECKING

import matplotlib.ticker as ticker
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)

from ._abstract_annotation import AbstractAnnotation

if TYPE_CHECKING:
    from sorbetto.tile import Tile


class AnnotationIsovalueCurves(AbstractAnnotation):
    """
    This type of annotation can be used to draw isovalue curves with value labels
    on numeric tile.
    """

    def __init__(
        self, levels: list | str | None = None, name: str | None = None, **plt_kwargs
    ):
        """_summary_

        Args:
            levels(list | str | None): a list of floating point values,
                "auto-values", "auto-areas", or None. Defaults to None,
                the default behavior, which is currently the same as "auto-values".
                With "auto-values", the levels are "pretty" values linearly spread
                approximately between the minimum and maximum values of the Tile.
                With "auto-areas", the levels are chosen in such a way that the
                area on the Tile between consecutive levels is approximately constant.
            name (str | None, optional): the annotation's name. Defaults to None.
            plt_kwargs: options to pass to matplotlib.pyplot.
        """

        if levels is None:
            levels = "auto-values"
        else:
            if isinstance(levels, list):
                assert all(isinstance(x, float) for x in levels)
            elif isinstance(levels, str):
                assert levels in ["auto-values", "auto-areas"]
            else:
                assert False
        self._levels = levels

        if name is None:
            name = "isovalue curves"
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def _get_levels(self, mat_values: np.ndarray) -> np.ndarray:
        levels = self._levels
        if isinstance(levels, list):
            return levels
        if levels == "auto-values":
            max_val = np.nanmax(mat_values)
            min_val = np.nanmin(mat_values)

            if np.abs(max_val - min_val) < 1e-6:
                return np.empty(0)

            locator = ticker.MaxNLocator(nbins=20)
            levels = locator.tick_values(min_val, max_val)
            return levels
        if levels == "auto-areas":
            qs = np.linspace(0, 100, 11)
            levels = [np.nanpercentile(mat_values, q) for q in qs]
            return levels
        assert False

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile import NumericTile

        if not isinstance(tile, NumericTile):
            message = "It makes no sense to draw isovalue curves on a Tile that is not numeric."
            logging.warning(message)
            return

        mat_values = tile.mat_value
        if mat_values is None:
            message = "It seems that there is no background image in this Tile."
            logging.warning(message)
            return
        assert isinstance(mat_values, np.ndarray)

        levels = self._get_levels(mat_values)

        vec_x = tile._vec_x
        assert isinstance(vec_x, np.ndarray)
        vec_y = tile._vec_y
        assert isinstance(vec_y, np.ndarray)

        cs = ax.contour(
            vec_x,
            vec_y,
            mat_values,
            levels=levels,
            colors="cornflowerblue",
            **self._plt_kwargs,  # TODO: filter these properties with a function in sorbetto.core.matplotlib_utils
        )
        tiny = 6
        ax.clabel(
            cs, inline=True, fontsize=tiny, **self._plt_kwargs
        )  # TODO: filter these properties with a function in sorbetto.core.matplotlib_utils

    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintRelativeImportanceSatisfyingUnsatisfying): a constraint on importances.

        Returns:
            bool: True
        """
        assert isinstance(
            constraint, ConstraintRelativeImportanceSatisfyingUnsatisfying
        )
        return True

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
        return None

    def getConstraintOnClassPriors(self) -> ConstraintFixedClassPriors | None:
        return None

    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        return None
