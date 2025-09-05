from sorbetto.core.entity import Entity
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


def test_properties():
    perf = TwoClassClassificationPerformance(ptn=0.9, pfp=0.1, pfn=0.05, ptp=0.95)

    entity = Entity(performance=perf, name="TestEntity", color="red")

    assert entity.name == "TestEntity"
    assert entity.color == "red"
    assert entity.performance == perf
