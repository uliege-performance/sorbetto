# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import numpy as np

from sorbetto.core import Named
from sorbetto.performance import (
    TwoClassClassificationPerformance,
)


class Entity(Named):
    # TODO: In the future, we could add properties to the entities. For example,
    # one could add the "cost" of using this entity. This information could be
    # propagated on Tiles through specific flavors. For example, one could observe
    # the "cost" of using a state-of-the-art method. This is an idea from Jérôme Pierre.
    """
    An entity is an object that has a performance and a name associated to it.
    """

    def __init__(
        self,
        performance: TwoClassClassificationPerformance,
        name: str = "ε",
        color: Any = None,
    ):
        """
        Args:
            performance (TwoClassClassificationPerformance): Performance score for the entity
            name (str, optional): Name of the entity. Defaults to "ε"
            color (Any, optional): Color to use for the entity. Defaults to a random list of floats.
        """

        if color is None:
            color = list(np.random.random(3))
        self._color = color
        self._performance = performance
        default_name = "Entity for performance {}".format(performance.name)
        Named.__init__(self, default_name, name)

    @property
    def color(self) -> str | tuple[float] | list[float]:
        """The color associated to the entity."""
        return self._color

    @property
    def performance(self) -> TwoClassClassificationPerformance:
        """
        The result of the evaluation of the entity, that is its performance.
        """
        return self._performance

    def __str__(self):
        txt = f"Entity `{self.name}` with performance \n {self._performance.__str__()}"
        return txt
