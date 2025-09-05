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

    def __call__(self, performance):
        assert isinstance(performance, TwoClassClassificationPerformance)
        value = performance.pfn + performance.ptp
        return math.isclose(value, self._priorPos, abs_tol=1e-8)

    def getPriorNeg(self):
        return 1 - self._priorPos

    def getPriorPos(self):
        return self._priorPos

    def __str__(self):
        priorPos = self._priorPos
        priorNeg = 1.0 - priorPos
        return "constraint: fixed class priors for (neg,pos)=({:g},{:g})".format(
            priorNeg, priorPos
        )
