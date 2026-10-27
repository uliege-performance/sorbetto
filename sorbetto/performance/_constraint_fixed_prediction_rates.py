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
    def __init__(self, ratePos: float):
        assert isinstance(ratePos, float)
        assert ratePos >= 0.0
        assert ratePos <= 1.0
        self._ratePos = ratePos
        ConstraintLinearOnTwoClassClassificationPerformance.__init__(
            0.0, 1.0, 0.0, 1.0, ratePos
        )

    def __call__(self, performance: TwoClassClassificationPerformance) -> bool:
        # Override the parents' implementation for speed optimization.
        assert isinstance(performance, TwoClassClassificationPerformance)
        value = performance._rate_pos()
        return math.isclose(value, self._ratePos, abs_tol=1e-8)

    def getRateNeg(self):
        return 1.0 - self._ratePos

    def getRatePos(self):
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
