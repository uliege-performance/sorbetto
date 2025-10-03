# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math

from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class ConstraintFixedClassPriors:
    def __init__(self, priorPos: float):
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0
        self._priorPos = priorPos

    def __call__(self, performance: TwoClassClassificationPerformance) -> bool:
        assert isinstance(performance, TwoClassClassificationPerformance)
        value = performance._prior_pos()
        return math.isclose(value, self._priorPos, abs_tol=1e-8)

    def getPriorNeg(self):
        return 1.0 - self._priorPos

    def getPriorPos(self):
        return self._priorPos

    def __str__(self):
        priorPos = self._priorPos
        priorNeg = 1.0 - priorPos
        return "constraint: fixed class priors for (neg,pos)=({:g},{:g})".format(
            priorNeg, priorPos
        )

    def __eq__(self, other):
        if not isinstance(other, ConstraintFixedClassPriors):
            return NotImplemented
        else:
            return math.isclose(self._priorPos, other._priorPos)
