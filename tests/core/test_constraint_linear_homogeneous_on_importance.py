# Copyright (c) 2025-2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import random

from sorbetto.ranking import (
    ConstraintCanonical,
    ConstraintImportanceAdaptedToClassPriors,
    ConstraintImportanceAdaptedToPredictionRates,
    Importance,
    RankingScore,
)


def test_method_samePerformanceOrdering():
    NUM_TRIALS = 100
    for _ in range(NUM_TRIALS):
        itn = random.random()
        ifp = random.random()
        ifn = random.random()
        itp = random.random()
        i = Importance(itn, ifp, ifn, itp)

        c = ConstraintCanonical()
        c.samePerformanceOrdering(i)

        for priorPos in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99]:
            c = ConstraintImportanceAdaptedToClassPriors(priorPos)
            c.samePerformanceOrdering(i)

        for ratePos in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99]:
            c = ConstraintImportanceAdaptedToPredictionRates(ratePos)
            c.samePerformanceOrdering(i)


def test_known_canonicals():
    c = ConstraintCanonical()

    score = RankingScore.getTrueNegativeRate()
    assert c(score.importance)

    score = RankingScore.getSpecificity()
    assert c(score.importance)

    score = RankingScore.getSelectivity()
    assert c(score.importance)

    score = RankingScore.getInverseRecall()
    assert c(score.importance)

    score = RankingScore.getTruePositiveRate()
    assert c(score.importance)

    score = RankingScore.getSensitivity()
    assert c(score.importance)

    score = RankingScore.getRecall()
    assert c(score.importance)

    score = RankingScore.getNegativePredictiveValue()
    assert c(score.importance)

    score = RankingScore.getInversePrecision()
    assert c(score.importance)

    score = RankingScore.getPositivePredictiveValue()
    assert c(score.importance)

    score = RankingScore.getPrecision()
    assert c(score.importance)

    score = RankingScore.getF(beta=1.0)
    assert c(score.importance)

    score = RankingScore.getDiceSorensenCoefficient()
    assert c(score.importance)

    score = RankingScore.getDiceSimilarityCoefficient()
    assert c(score.importance)

    score = RankingScore.getZijdenbosSimilarityIndex()
    assert c(score.importance)

    score = RankingScore.getCzekanowskiBinaryIndex()
    assert c(score.importance)

    score = RankingScore.getInverseF(beta=1.0)
    assert c(score.importance)

    score = RankingScore.getAccuracy()
    assert c(score.importance)

    for priorPos in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99]:
        score = RankingScore.getMacroAveragedRecall(priorPos)
        assert c(score.importance)

        score = RankingScore.getBalancedAccuracy(priorPos)
        assert c(score.importance)

    for ratePos in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99]:
        score = RankingScore.getMacroAveragedPrecision(ratePos)
        assert c(score.importance)


def test_known_adapted_to_class_priors():
    for priorPos in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99]:
        c = ConstraintImportanceAdaptedToClassPriors(priorPos)

        score = RankingScore.getTrueNegativeRate()
        assert c(score.importance)

        score = RankingScore.getSpecificity()
        assert c(score.importance)

        score = RankingScore.getSelectivity()
        assert c(score.importance)

        score = RankingScore.getInverseRecall()
        assert c(score.importance)

        score = RankingScore.getTruePositiveRate()
        assert c(score.importance)

        score = RankingScore.getSensitivity()
        assert c(score.importance)

        score = RankingScore.getRecall()
        assert c(score.importance)

        score = RankingScore.getStandardizedNegativePredictiveValue(priorPos)
        assert c(score.importance)

        score = RankingScore.getStandardizedPositivePredictiveValue(priorPos)
        assert c(score.importance)

        score = RankingScore.getSkewInsensitiveVersionOfF1(priorPos)
        assert c(score.importance)

        score = RankingScore.getAccuracy()
        assert c(score.importance)

        score = RankingScore.getMacroAveragedRecall(priorPos)
        assert c(score.importance)

        score = RankingScore.getBalancedAccuracy(priorPos)
        assert c(score.importance)


def test_known_adapted_to_prediction_rates():
    for ratePos in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99]:
        c = ConstraintImportanceAdaptedToPredictionRates(ratePos)

        score = RankingScore.getNegativePredictiveValue()
        assert c(score.importance)

        score = RankingScore.getInversePrecision()
        assert c(score.importance)

        score = RankingScore.getPositivePredictiveValue()
        assert c(score.importance)

        score = RankingScore.getPrecision()
        assert c(score.importance)

        score = RankingScore.getAccuracy()
        assert c(score.importance)

        score = RankingScore.getMacroAveragedPrecision(ratePos)
        assert c(score.importance)
