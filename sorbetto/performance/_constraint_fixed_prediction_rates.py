# Copyright (c) 2025-2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math

from sorbetto.performance._constraint_linear_on_two_class_classification_performance import (
    ConstraintLinearOnTwoClassClassificationPerformance,
)

from ._two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class ConstraintFixedPredictionRates(
    ConstraintLinearOnTwoClassClassificationPerformance
):
    """
    This class represents constraints on two-class classification performances
    corresponding to fixed prediction rates: :math:`\\tau_-` for the negative class,
    :math:`\\tau_+` for the positive class, with :math:`\\tau_- \\ge 0`,
    :math:`\\tau_+ \\ge 0`, and :math:`\\tau_- + \\tau_+ = 1`. A performance
    :math:`P` satisfies such a constraint if and only if

    .. math::
        P(\\{tn,fn\\}) = \\tau_- \\Leftrightarrow P(\\{fp,tp\\}) = \\tau_+

    or, equivalently,

    .. math::
        \\tau_+ P(\\{tn\\}) - \\tau_- P(\\{fp\\}) + \\tau_+ P(\\{fn\\}) - \\tau_- P(\\{tp\\}) = 0

    """

    def __init__(self, ratePos: float):
        """Instantiate a constraint object based on the prediction rate for the positive class.

        Args:
            ratePos (float): The prediction rate for the positive class, :math:`\\tau_+ \\in [0,1]`.
        """
        assert isinstance(ratePos, float)
        assert ratePos >= 0.0
        assert ratePos <= 1.0
        self._ratePos = ratePos
        ConstraintLinearOnTwoClassClassificationPerformance.__init__(
            self, 0.0, 1.0, 0.0, 1.0, ratePos
        )

    def __call__(self, performance: TwoClassClassificationPerformance) -> bool:
        # Override the parents' implementation for speed optimization.
        assert isinstance(performance, TwoClassClassificationPerformance)
        value = performance._rate_pos()
        return math.isclose(value, self._ratePos, abs_tol=1e-8)

    def getRateNeg(self):
        """
        Returns the fixed prediction rate for the negative class, :math:`\\tau_-`.
        """
        return 1.0 - self._ratePos

    def getRatePos(self):
        """
        Returns the fixed prediction rate for the positive class, :math:`\\tau_+`.
        """
        return self._ratePos

    def __str__(self):
        ratePos = self._ratePos
        rateNeg = 1.0 - ratePos
        return "constraint: fixed prediction rates for (neg,pos)=({:g},{:g})".format(
            rateNeg, ratePos
        )

    def __eq__(self, other):
        # Override the parents' implementation for speed optimization.
        if not isinstance(other, ConstraintFixedPredictionRates):
            return super().__eq__(other)
        else:
            return math.isclose(self._ratePos, other._ratePos)
