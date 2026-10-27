# Copyright (c) 2025-2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

# from typing import TYPE_CHECKING

from ._constraint_relative_importance_satisfying_unsatisfying import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)

# if TYPE_CHECKING:
#    from ._importance import Importance


class ConstraintCanonical(ConstraintRelativeImportanceSatisfyingUnsatisfying):
    """
    This class represents the following homogeneous linear constraint on
    importance values:

    .. math::
        I(tn)+I(tp) = I(fp)+I(fn) \\Leftrightarrow I(tn)-I(fp)-I(fn)+I(tp)=0

    Ranking scores are said "canonical" when the importance satisfy this
    constraint. This is motivated by the fact that all ranking scores with
    the same values for

    .. math::
        a(I)=\\frac{ I(tp) }{ I(tn)+I(tp) }

    and

    .. math::
        b(I)=\\frac{ I(fn) }{ I(fp)+I(fn) }

    induce the same performance ordering. From a ranking point of view, it is
    thus not necessary to consider all of them. With the canonical importances,
    the accuracy (A), the true negative rate (TNR), the true positive rate (TPR),
    the negative predictive value (NPV), the positive predictive value (PPV),
    and the F-scores for both classes belong to the canonical ranking scores.
    """

    def __init__(self):
        ConstraintRelativeImportanceSatisfyingUnsatisfying.__init__(self, 0.5, 0.5)

    # def __call__(self, importance: "Importance") -> bool:
    #     from ._importance import Importance
    #
    #     assert isinstance(importance, Importance)
    #     return importance.isCanonical()

    def __str__(self) -> str:
        return "constraint: canonical importance"
