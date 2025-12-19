# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._importance import Importance


class ConstraintRelativeImportanceSatisfyingUnsatisfying:
    def __init__(
        self, relativeImportanceSatisfying: float, relativeImportanceUnsatisfying: float
    ):
        assert isinstance(relativeImportanceSatisfying, float)
        assert math.isfinite(relativeImportanceSatisfying)
        assert relativeImportanceSatisfying >= 0.0

        assert isinstance(relativeImportanceUnsatisfying, float)
        assert math.isfinite(relativeImportanceUnsatisfying)
        assert relativeImportanceUnsatisfying >= 0.0

        sum = relativeImportanceSatisfying + relativeImportanceUnsatisfying
        self._relativeImportanceSatisfying = relativeImportanceSatisfying / sum
        self._relativeImportanceUnsatisfying = relativeImportanceUnsatisfying / sum

    def __call__(self, importance: "Importance") -> bool:
        from ._importance import Importance

        assert isinstance(importance, Importance)
        importanceSatisfying = importance.itn + importance.itp
        importanceUnsatisfying = importance.ifp + importance.ifn
        sum = importanceSatisfying + importanceUnsatisfying
        relativeImportanceSatisfying = importanceSatisfying / sum
        if not math.isclose(
            relativeImportanceSatisfying,
            self._relativeImportanceSatisfying,
            abs_tol=1e-6,
        ):
            return False
        relativeImportanceUnsatisfying = importanceUnsatisfying / sum
        if not math.isclose(
            relativeImportanceUnsatisfying,
            self._relativeImportanceUnsatisfying,
            abs_tol=1e-6,
        ):
            return False
        return True

    def __str__(self):
        return "constraint: relative importance of satisfying vs. unsatisfying"

    def __eq__(self, other):
        if not isinstance(other, ConstraintRelativeImportanceSatisfyingUnsatisfying):
            return NotImplemented
        else:
            return math.isclose(
                self._relativeImportanceSatisfying, other._relativeImportanceSatisfying
            )
