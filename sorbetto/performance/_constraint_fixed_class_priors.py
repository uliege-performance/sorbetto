# Copyright (c) 2025-2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math

from sorbetto.performance._constraint_linear_on_two_class_classification_performance import (
    ConstraintLinearOnTwoClassClassificationPerformance,
)

from ._two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class ConstraintFixedClassPriors(ConstraintLinearOnTwoClassClassificationPerformance):
    """
    This class represents constraints on two-class classification performances
    corresponding to fixed class priors: :math:`\\pi_-` for the negative class,
    :math:`\\pi_+` for the positive class, with :math:`\\pi_- \\ge 0`,
    :math:`\\pi_+ \\ge 0`, and :math:`\\pi_- + \\pi_+ = 1`. A performance
    :math:`P` satisfies such a constraint if and only if

    .. math::
        P(\\{tn,fp\\}) = \\pi_- \\Leftrightarrow P(\\{fn,tp\\}) = \\pi_+

    or, equivalently,

    .. math::
        \\pi_+ P(\\{tn\\}) + \\pi_+ P(\\{fp\\}) - \\pi_- P(\\{fn\\}) - \\pi_- P(\\{tp\\}) = 0

    """

    def __init__(self, priorPos: float):
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0
        self._priorPos = priorPos
        ConstraintLinearOnTwoClassClassificationPerformance.__init__(
            self, 0.0, 0.0, 1.0, 1.0, priorPos
        )

    def __call__(self, performance: TwoClassClassificationPerformance) -> bool:
        # Override the parents' implementation for speed optimization.
        assert isinstance(performance, TwoClassClassificationPerformance)
        value = performance._prior_pos()
        return math.isclose(value, self._priorPos, abs_tol=1e-8)

    def getPriorNeg(self):
        """
        Returns the fixed prior for the negative class, :math:`\\pi_-`.
        """
        return 1.0 - self._priorPos

    def getPriorPos(self):
        """
        Returns the fixed prior for the positive class, :math:`\\pi_+`.
        """
        return self._priorPos

    def __str__(self):
        priorPos = self._priorPos
        priorNeg = 1.0 - priorPos
        return "constraint: fixed class priors for (neg,pos)=({:g},{:g})".format(
            priorNeg, priorPos
        )

    def __eq__(self, other):
        # Override the parents' implementation for speed optimization.
        if not isinstance(other, ConstraintFixedClassPriors):
            return super().__eq__(other)
        else:
            return math.isclose(self._priorPos, other._priorPos)
