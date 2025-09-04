from typing import Any

import numpy as np

from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class Entity:
    def __init__(
        self,
        performance: TwoClassClassificationPerformance,
        name: str = "ε",
        color: Any = None,
    ):
        """Entity class

        Args:
            performance (TwoClassClassificationPerformance): Performance score for the entity
            name (str): Name of the entity. Defaults to "ε"
            color (Any, optional): Color to use for the entity. Defaults to a random list of floats.
        """

        self._name = name
        if color is None:
            color = list(np.random.random(3))
        self._color = color
        self._performance = performance

    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> str | tuple[float] | list[float]:
        return self._color

    @property
    def performance(self) -> TwoClassClassificationPerformance:
        """
        The result of the evaluation of the entity, that is its performance.

        Returns:
            TwoClassClassificationPerformance: The entity's performance
        """
        return self._performance

    def __str__(self):
        txt = f"Entity `{self._name}` with performance \n {self._performance.__str__()}"
        return txt
