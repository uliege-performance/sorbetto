# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.ranking.entity import Entity


def test_properties():
    perf = TwoClassClassificationPerformance(ptn=0.45, pfp=0.05, pfn=0.025, ptp=0.475)

    entity = Entity(performance=perf, name="TestEntity", color="red")

    assert entity.name == "TestEntity"
    assert entity.color == "red"
    assert entity.performance == perf
