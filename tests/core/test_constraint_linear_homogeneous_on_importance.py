# Copyright (c) 2025-2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import random

from sorbetto.ranking import (
    ConstraintCanonical,
    ConstraintImportanceAdaptedToClassPriors,
    ConstraintImportanceAdaptedToPredictionRates,
    Importance,
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
