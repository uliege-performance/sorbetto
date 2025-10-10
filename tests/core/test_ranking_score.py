import math

from sorbetto.performance import TwoClassClassificationPerformance
from sorbetto.performance.distribution import (
    UniformDistributionOfTwoClassClassificationPerformances,
)
from sorbetto.ranking import Importance, RankingScore


def test_equality():
    importance_a = Importance(1.0, 2.0, 3.0, 4.0)
    importance_b = Importance(2, 4, 6, 8)
    importance_c = Importance(1.0, 2.0, 3.0, 5.0)
    score_a = RankingScore(importance_a)
    score_b = RankingScore(importance_b)
    score_c = RankingScore(importance_c)

    assert score_a == score_b
    assert not (score_a == score_c)


def test_SkewInsensitiveVersionOfF1():
    def _classical_formula(performance):
        assert isinstance(performance, TwoClassClassificationPerformance)
        tpr = performance._tpr()
        fpr = performance._fpr()
        # Formula given in cite:t:`Flach2003TheGeometry`, at the top-right of the fifth page.
        return 2 * tpr / (tpr + fpr + 1)

    distri = UniformDistributionOfTwoClassClassificationPerformances()
    performances = distri.sampleOnRegularGrid(grid_size=6)
    for performance in performances:
        priorPos = performance._prior_pos()
        score_1 = _classical_formula
        # FIXME adapt this test when we decide what to do with zero priors
        if priorPos == 0.0 or priorPos == 1.0:
            continue
        score_2 = RankingScore.getSkewInsensitiveVersionOfF1(priorPos)
        value_1 = score_1(performance)
        value_2 = score_2(performance)
        assert math.isclose(value_1, value_2, abs_tol=1e-8)
