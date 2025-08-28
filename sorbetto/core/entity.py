from typing import Any

from sorbetto.performance.two_class_classification import (
    TwoClassClassificationPerformance,
)


class Entity:
    def __init__(
        self,
        performance: TwoClassClassificationPerformance,
        name: str = "ε",
        color: Any = "blue",
    ):
        """Entity class

        Args:
            performance (TwoClassClassificationPerformance): Performance score for the entity
            name (str): Name of the entity. Defaults to "ε"
            color (Any, optional): Color to use for the entity. Defaults to "blue".
        """

        self._name = name
        self._color = color
        self._performance = performance

    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> str | tuple[float] | list[float]:
        return self._color

    def evaluate(self) -> TwoClassClassificationPerformance:
        return self._performance

    def __str__(self):
        txt = f"Entity `{self._name}` with performance \n {self._performance.__str__()}"
        return txt


if __name__ == "__main__":

    class MockPerformance:
        def __str__(self):
            return "MockPerformance(tn=0.9, fp=0.1, fn=0.05, tp=0.95)"

    mock_perf = MockPerformance()

    # Test successful creation
    entity1 = Entity(performance=mock_perf, name="TestEntity1", color="red")
    print(f"Successfully created: {entity1}")
    assert entity1.name == "TestEntity1"
    assert entity1.color == "red"
    assert entity1.evaluate() == mock_perf

    # Test default creation
    entity2 = Entity(performance=mock_perf)
    print(f"Successfully created with defaults: {entity2}")
    assert entity2.name == "ε"
    assert entity2.color == "blue"

    # Test string representation
    expected_str = "Entity `TestEntity1` with performance \n MockPerformance(tn=0.9, fp=0.1, fn=0.05, tp=0.95)"
    assert str(entity1) == expected_str
    print("String representation test passed.")

    print("\nAll tests passed!")
