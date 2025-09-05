import math

from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class ConstraintFixedPredictionRates:
    def __init__(self, ratePos: float):
        assert isinstance(ratePos, float)
        assert ratePos >= 0.0
        assert ratePos <= 1.0
        self._ratePos = ratePos

    def __call__(self, performance):
        assert isinstance(performance, TwoClassClassificationPerformance)
        value = performance.pfp + performance.ptp
        return math.isclose(value, self._ratePos, abs_tol=1e-8)

    def getRateNeg(self):
        return 1 - self._ratePos

    def getRatePos(self):
        return self._ratePos

    def __str__(self):
        ratePos = self._ratePos
        rateNeg = 1.0 - ratePos
        return "constraint: fixed prediction rates for (neg,pos)=({:g},{:g})".format(
            rateNeg, ratePos
        )
