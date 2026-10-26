# Copyright (c) 2025-2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._importance import Importance


class ConstraintLinearHomogeneousOnImportance:
    """
    This class represents homogeneous linear constraints on importance values:

    .. math::
        \\lambda_{tn} I(tn) + \\lambda_{fp} I(fp) + \\lambda_{fn} I(fn) + \\lambda_{tp} I(tp) = 0

    The motivation to restrict the linear constraints to homogeneous ones
    comes from the fact that ranking scores are insensitive to the scaling of
    the importance values. The homogeneous linear constraints are also
    insensitive to the scaling of the importance values.
    """

    def __init__(
        self, lambda_tn: float, lambda_fp: float, lambda_fn: float, lambda_tp: float
    ):
        assert isinstance(lambda_tn, float) and math.isfinite(lambda_tn)
        assert isinstance(lambda_fp, float) and math.isfinite(lambda_fp)
        assert isinstance(lambda_fn, float) and math.isfinite(lambda_fn)
        assert isinstance(lambda_tp, float) and math.isfinite(lambda_tp)

        self.lambda_tn = lambda_tn
        self.lambda_fp = lambda_fp
        self.lambda_fn = lambda_fn
        self.lambda_tp = lambda_tp

    def __call__(self, importance: "Importance") -> bool:
        from ._importance import Importance

        assert isinstance(importance, Importance)
        sum = 0.0
        sum += self.lambda_tn * importance.itn
        sum += self.lambda_fp * importance.ifp
        sum += self.lambda_fn * importance.ifn
        sum += self.lambda_tp * importance.itp
        return math.fabs(sum) < 1e-6

    def __str__(self) -> str:
        substrings = []

        coefs = [self.lambda_tn, self.lambda_fp, self.lambda_fn, self.lambda_tp]
        vars = ["I(tn)", "I(fp)", "I(fn)", "I(tp)"]
        for coef, var in zip(coefs, vars):
            if coef == 0.0:
                continue
            sign = "-" if coef < 0 else "+"
            val = math.fabs(coef)
            substring = var if val == 1.0 else "{:g} {}".format(val, var)
            if not substrings:
                if coef < 0.0:
                    substrings.append("-")
                substrings.append(substring)
            else:
                substrings.append(" {} {}".format(sign, substring))

        if not substrings:
            return "constraint: 0 = 0"

        return "constraint: " + " ".join(substrings) + " = 0"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ConstraintLinearHomogeneousOnImportance):
            return NotImplemented
        else:
            coefs_self = [
                self.lambda_tn,
                self.lambda_fp,
                self.lambda_fn,
                self.lambda_tp,
            ]
            coefs_other = [
                other.lambda_tn,
                other.lambda_fp,
                other.lambda_fn,
                other.lambda_tp,
            ]

            sum_self = sum(coefs_self)
            sum_other = sum(coefs_other)

            for coef_self, coef_other in zip(coefs_self, coefs_other):
                if math.fabs(coef_self * sum_other - coef_other * sum_self) > 1e-6:
                    return False
            return True
