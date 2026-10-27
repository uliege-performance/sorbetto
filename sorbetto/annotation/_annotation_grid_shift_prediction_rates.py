# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import TYPE_CHECKING

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.flavor import ValueFlavor
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


class AnnotationGridShiftPredictionRates(AbstractAnnotation):
    r"""
    This type of annotation can be used to place a grid on the Tile to show the
    effect of a target shift on the prediction rates :math:`P(\hat{Y})`.

    A target shift transforming the prediction rates
    from :math:`(\tau_-, \tau_+)` to :math:`(\tau_-', \tau_+')`, when applied
    to a performance :math:`P`, leads to a performance `P'` such that:

    - :math:`P'(\{tn\}) \propto P(\{tn\}) \frac{ \tau_-' }{ \tau_- }`
    - :math:`P'(\{fp\}) \propto P(\{fp\}) \frac{ \tau_+' }{ \tau_+ }`
    - :math:`P'(\{fn\}) \propto P(\{fn\}) \frac{ \tau_-' }{ \tau_- }`
    - :math:`P'(\{tp\}) \propto P(\{tp\}) \frac{ \tau_+' }{ \tau_+ }`

    In the particular case in which :math:`(P(\hat{Y}=c_-), P(\hat{Y}=c_+))=(\tau_-, \tau_+)`,
    we obtain :math:`(P'(\hat{Y}=c_-), P'(\hat{Y}=c_+))=(\tau_-', \tau_+')`.

    Tiles are distorted by such a shift: the information placed on it moves.
    The grid is intended to show the resulting displacements on the Tile.
    It turns out that, from the point of view of ranking scores values, the shift
    is perfectly compensated by the inverse operation applied to importance values as
    :math:`R_{I'}(P')=R_I(P)` with:

    - :math:`I'(tn) = I(tn) \frac{ \tau_- }{ \tau_-' }`
    - :math:`I'(fp) = I(fp) \frac{ \tau_+ }{ \tau_+' }`
    - :math:`I'(fn) = I(fn) \frac{ \tau_- }{ \tau_-' }`
    - :math:`I'(tp) = I(tp) \frac{ \tau_+ }{ \tau_+' }`

    For more information, see :cite:t:`Pierard2024TheTile-arxiv`, Section A.2.2.
    """

    # TODO: It should be possible to automatically retrieve the prediction rates
    # from the flavor of the tile on which this annotation should be placed.
    def __init__(
        self,
        rate_pos_old: float | ConstraintFixedPredictionRates,
        rate_pos_new: float | ConstraintFixedPredictionRates,
        name: str | None = None,
        **plt_kwargs,
    ):
        if isinstance(rate_pos_new, ConstraintFixedPredictionRates):
            rate_pos_new = rate_pos_new.getRatePos()
        assert isinstance(rate_pos_new, float)
        assert rate_pos_new > 0.0
        assert rate_pos_new < 1.0
        self._rate_pos_new = rate_pos_new

        if isinstance(rate_pos_old, ConstraintFixedPredictionRates):
            rate_pos_old = rate_pos_old.getRatePos()
        assert isinstance(rate_pos_old, float)
        assert rate_pos_old > 0.0
        assert rate_pos_old < 1.0
        self._rate_pos_old = rate_pos_old

        if name is None:
            name = "grid for the prediction rates ({:g}, {:g})".format(
                1.0 - rate_pos_new, rate_pos_new
            )
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile import Tile

        assert isinstance(tile, Tile)

        flavor = tile.flavor
        if isinstance(flavor, ValueFlavor):
            flavor_rate_pos = flavor.performance._rate_pos
            if not math.isclose(flavor_rate_pos, self._rate_pos_new, abs_tol=1e-6):
                message = "wrong prediction rates: the value flavor is for ({}, {}) while the curve is for ({}, {})"
                message = message.format(
                    1.0 - flavor_rate_pos,
                    flavor_rate_pos,
                    1.0 - self._rate_pos_new,
                    self._rate_pos_new,
                )
                raise RuntimeError(message)

        parameterization = tile.parameterization
        extent = parameterization.getExtent()

        rate_pos_new = self._rate_pos_new
        rate_neg_new = 1.0 - self._rate_pos_new
        rate_pos_old = self._rate_pos_old
        rate_neg_old = 1.0 - self._rate_pos_old

        plt_kwargs = self._plt_kwargs.copy()
        if "color" not in plt_kwargs.keys():
            plt_kwargs["color"] = "lightgrey"
        if "linestyle" not in plt_kwargs.keys():
            plt_kwargs["linestyle"] = ":"

        for v in np.linspace(0.0, 1.0, 11):
            # relative importance of true negatives (up to a positive scale factor)
            itn = v
            # relative importance of true positives (up to a positive scale factor)
            itp = 1.0 - v
            # adaptation: we need to compensate for a target shift from
            # (rate_neg_old, rate_pos_old) to (rate_neg_new, rate_pos_new): by doing
            # the opposite of what would be done on probabilities, the value taken
            # by a ranking score does not change.
            itn *= rate_neg_old / rate_neg_new
            itp *= rate_pos_old / rate_pos_new
            # plot
            line = parameterization.locateRelativeImportanceSatisfying(itn, itp)
            line.draw(fig, ax, extent, **plt_kwargs)

        for v in np.linspace(0.0, 1.0, 11):
            # relative importance of false positives (up to a positive scale factor)
            ifp = v
            # relative importance of false negatives (up to a positive scale factor)
            ifn = 1.0 - v
            # adaptation: we need to compensate for a target shift from
            # (rate_neg_old, rate_pos_old) to (rate_neg_new, rate_pos_new): by doing
            # the opposite of what would be done on probabilities, the value taken
            # by a ranking score does not change.
            ifp *= rate_pos_old / rate_pos_new
            ifn *= rate_neg_old / rate_neg_new
            line = parameterization.locateRelativeImportanceUnsatisfying(ifp, ifn)
            line.draw(fig, ax, extent, **plt_kwargs)

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
