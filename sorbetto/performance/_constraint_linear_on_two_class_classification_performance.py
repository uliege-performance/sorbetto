# Copyright (c) 2025-2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._two_class_classification_performance import TwoClassClassificationPerformance


class ConstraintLinearOnTwoClassClassificationPerformance:
    """
    This class represents linear constraints on two-class classification performances:

    .. math::
        \\lambda_{tn} P({tn}) + \\lambda_{fp} P({fp}) + \\lambda_{fn} P({fn}) + \\lambda_{tp} P({tp}) = \\lambda_0

    Note that, as :math:`P({tn}) + P({fp}) + P({fn}) + P({tp}) = 1`, this is equivalent to

    .. math::
        (\\lambda_{tn}-\\lambda_0) P({tn}) + (\\lambda_{fp}-\\lambda_0) P({fp}) + (\\lambda_{fn}-\\lambda_0) P({fn}) + (\\lambda_{tp}-\\lambda_0) P({tp}) = 0

    So, all linear constraints can be converted into homogeneous linear constraints.
    """

    def __init__(
        self,
        lambda_tn: float,
        lambda_fp: float,
        lambda_fn: float,
        lambda_tp: float,
        lambda_0: float = 0.0,
    ):
        assert isinstance(lambda_tn, float) and math.isfinite(lambda_tn)
        assert isinstance(lambda_fp, float) and math.isfinite(lambda_fp)
        assert isinstance(lambda_fn, float) and math.isfinite(lambda_fn)
        assert isinstance(lambda_tp, float) and math.isfinite(lambda_tp)
        assert isinstance(lambda_0, float) and math.isfinite(lambda_0)

        self._lambda_tn = lambda_tn - lambda_0
        self._lambda_fp = lambda_fp - lambda_0
        self._lambda_fn = lambda_fn - lambda_0
        self._lambda_tp = lambda_tp - lambda_0

        # TODO: Do we want to normalize the coefficients? The sum of the coefficients
        # can be zero. So, do not divide them by the sum. Instead, divide by a norm.
        # Is the Euclidean norm the best choice?

    def __call__(self, performance: "TwoClassClassificationPerformance") -> bool:
        from ._TwoClassClassificationPerformance import (
            TwoClassClassificationPerformance,
        )

        assert isinstance(performance, TwoClassClassificationPerformance)
        sum = 0.0
        sum += self._lambda_tn * performance.ptn
        sum += self._lambda_fp * performance.pfp
        sum += self._lambda_fn * performance.pfn
        sum += self._lambda_tp * performance.ptp
        return math.fabs(sum) < 1e-6

    def __str__(self) -> str:
        substrings = []

        coefs = [self._lambda_tn, self._lambda_fp, self._lambda_fn, self._lambda_tp]
        vars = ["P({tn})", "P({fp})", "P({fn})", "P({tp})"]
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
        if not isinstance(other, ConstraintLinearOnTwoClassClassificationPerformance):
            return NotImplemented
        else:
            coefs_self = [
                self._lambda_tn,
                self._lambda_fp,
                self._lambda_fn,
                self._lambda_tp,
            ]
            coefs_other = [
                other._lambda_tn,
                other._lambda_fp,
                other._lambda_fn,
                other._lambda_tp,
            ]

            sum_self = sum(coefs_self)
            sum_other = sum(coefs_other)

            for coef_self, coef_other in zip(coefs_self, coefs_other):
                if math.fabs(coef_self * sum_other - coef_other * sum_self) > 1e-6:
                    return False
            return True
