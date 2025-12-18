# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import TYPE_CHECKING

from sorbetto.ranking.constraint_relative_importance_satisfying_unsatisfying import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)

if TYPE_CHECKING:
    from sorbetto.ranking import Importance


class ConstraintCanonical(ConstraintRelativeImportanceSatisfyingUnsatisfying):
    def __init__(self):
        ConstraintRelativeImportanceSatisfyingUnsatisfying.__init__(self, 0.5, 0.5)

    def __call__(self, importance: "Importance") -> bool:
        from sorbetto.ranking import Importance

        assert isinstance(importance, Importance)
        return importance.isCanonical()

    def __str__(self):
        return "constraint: canonical importance"
