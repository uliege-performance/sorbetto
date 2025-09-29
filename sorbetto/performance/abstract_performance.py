# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod

import numpy as np

from sorbetto.core.named import Named


class AbstractPerformance(ABC, Named):
    def __init__(self, name: str | None = None):
        ABC.__init__(self)
        default_name = "unnamed performance"
        Named.__init__(self, default_name, name)

    @abstractmethod
    def getMassFunction(self) -> np.ndarray: ...
