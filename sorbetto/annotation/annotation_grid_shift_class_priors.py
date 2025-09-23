import math
from typing import TYPE_CHECKING

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationGridShiftClassPriors(AbstractAnnotation):
    """
    This type of annotation can be used to place a grid on the Tile to show the
    effect of a target shift on the class priors :math:`P(Y)`.

    A target shift transforming the class priors :math:`(P(Y=c_-), P(Y=c_+))`
    from :math:`(\\pi_-, \\pi_+)` to :math:`(\\pi_-', \\pi_+')`, when applied
    to a performance :math:`P`, leads to a performance `P'` such that:

    - :math:`P'(\\{tn\\}) = P(\\{tn\\}) \\frac{ \\pi_-' }{ \\pi_- }`
    - :math:`P'(\\{fp\\}) = P(\\{fp\\}) \\frac{ \\pi_-' }{ \\pi_- }`
    - :math:`P'(\\{fn\\}) = P(\\{fn\\}) \\frac{ \\pi_+' }{ \\pi_+ }`
    - :math:`P'(\\{tp\\}) = P(\\{tp\\}) \\frac{ \\pi_+' }{ \\pi_+ }`

    Tiles are distorted by such a shift: the information placed on it moves.
    The grid is intended to show the resulting displacements on the Tile.
    It turns out that, from the point of view of ranking scores values, the shift
    is perfectly compensated by the inverse operation applied to importance values as
    :math:`R_{I'}(P')=R_I(P)` with:

    - :math:`I'(tn) = I(tn) \\frac{ \\pi_- }{ \\pi_-' }`
    - :math:`I'(fp) = I(fp) \\frac{ \\pi_- }{ \\pi_-' }`
    - :math:`I'(fn) = I(fn) \\frac{ \\pi_+ }{ \\pi_+' }`
    - :math:`I'(tp) = I(tp) \\frac{ \\pi_+ }{ \\pi_+' }`

    For more information, see :cite:t:`Pierard2024TheTile-arxiv`, Section A.2.2.
    """

    def __init__(
        self,
        prior_pos_old: float | ConstraintFixedClassPriors,
        prior_pos_new: float | ConstraintFixedClassPriors,
        name: str | None = None,
        **plt_kwargs,
    ):
        if isinstance(prior_pos_new, ConstraintFixedClassPriors):
            prior_pos_new = prior_pos_new.getPriorPos()
        assert isinstance(prior_pos_new, float)
        assert prior_pos_new > 0.0
        assert prior_pos_new < 1.0
        self._prior_pos_new = prior_pos_new

        if isinstance(prior_pos_old, ConstraintFixedClassPriors):
            prior_pos_old = prior_pos_old.getPriorPos()
        assert isinstance(prior_pos_old, float)
        assert prior_pos_old > 0.0
        assert prior_pos_old < 1.0
        self._prior_pos_old = prior_pos_old

        if name is None:
            name = "grid for the class priors ({:g}, {:g})".format(
                1.0 - prior_pos_new, prior_pos_new
            )
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)

        flavor = tile.flavor
        if isinstance(flavor, ValueFlavor):
            flavor_prior_pos = flavor.performance._prior_pos
            if not math.isclose(flavor_prior_pos, self._prior_pos_new, abs_tol=1e-6):
                message = "wrong class priors: the value flavor is for ({}, {}) while the curve is for ({}, {})"
                message = message.format(
                    1.0 - flavor_prior_pos,
                    flavor_prior_pos,
                    1.0 - self._prior_pos_new,
                    self._prior_pos_new,
                )
                raise RuntimeError(message)

        parameterization = tile.parameterization
        extent = parameterization.getExtent()

        prior_pos_new = self._prior_pos_new
        prior_neg_new = 1.0 - self._prior_pos_new
        prior_pos_old = self._prior_pos_old
        prior_neg_old = 1.0 - self._prior_pos_old

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
            # (prior_neg_old, prior_pos_old) to (prior_neg_new, prior_pos_new): by doing
            # the opposite of what would be done on probabilities, the value taken
            # by a ranking score does not change.
            itn *= prior_neg_old / prior_neg_new
            itp *= prior_pos_old / prior_pos_new
            # plot
            line = parameterization.locateRelativeImportanceSatisfying(itn, itp)
            line.draw(fig, ax, extent, **plt_kwargs)

        for v in np.linspace(0.0, 1.0, 11):
            # relative importance of false positives (up to a positive scale factor)
            ifp = v
            # relative importance of false negatives (up to a positive scale factor)
            ifn = 1.0 - v
            # adaptation: we need to compensate for a target shift from
            # (prior_neg_old, prior_pos_old) to (prior_neg_new, prior_pos_new): by doing
            # the opposite of what would be done on probabilities, the value taken
            # by a ranking score does not change.
            ifp *= prior_neg_old / prior_neg_new
            ifn *= prior_pos_old / prior_pos_new
            line = parameterization.locateRelativeImportanceUnsatisfying(ifp, ifn)
            line.draw(fig, ax, extent, **plt_kwargs)
