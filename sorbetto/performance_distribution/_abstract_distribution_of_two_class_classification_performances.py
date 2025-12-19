# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod

from sorbetto.core import Named
from sorbetto.performance import (
    FiniteSetOfTwoClassClassificationPerformances,
    TwoClassClassificationPerformance,
)


class AbstractDistributionOfTwoClassClassificationPerformances(ABC, Named):
    """
    This is the base class for all distributions of two-class classification performances.
    """

    def __init__(self, name: str | None = None):
        ABC.__init__(self)
        default_name = "unnamed distribution of two-class classification performances"
        Named.__init__(self, default_name, name)

    @abstractmethod
    def drawOneAtRandom(self) -> TwoClassClassificationPerformance: ...

    @abstractmethod
    def drawAtRandom(
        self, numPerformances: int
    ) -> FiniteSetOfTwoClassClassificationPerformances: ...

    @abstractmethod
    def getMean(self) -> TwoClassClassificationPerformance: ...

    def __str__(self):
        txt = f"{self.name}: Distribution of two-class classification performances"
        return txt
