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

        self._lambda_tn = lambda_tn
        self._lambda_fp = lambda_fp
        self._lambda_fn = lambda_fn
        self._lambda_tp = lambda_tp

    def isValid(self) -> bool:
        """
        A linear constraint is valid if and only if it corresponds to a
        quadrilateral in the tetrahedron (simples) of importances that does not
        have any intersection with the tn-tp and fp-fn edges. It is a plane that
        cuts the tetrahedron in two parts, one in which the edge tn-tp is, and
        the other one in which the edge fp-fn is. This plane cuts each of the
        tn-fp, tn-fn, fp-tp, and fn-tp edges in exactly one point. These points
        are the vertices of the quadrilateral. Expressed in terms of the
        coefficients, the constraint is valid if and only if

        .. math::
            max( \\lambda_{tn}, \\lambda_{tp} ) < 0 < min( \\lambda_{fp}, \\lambda_{fn} )

        or

        .. math::
            max( \\lambda_{fp}, \\lambda_{fn} ) < 0 < min( \\lambda_{tn}, \\lambda_{tp} )

        The vertex of the quadrilateral corresponding to the intersection between
        the plane and the edge tn-fp of the tetrahedron (simplex) of importances
        is given by

        .. math::
            \\left(
                I(tn),
                I(fp),
                I(fn),
                I(tp)
            \\right) = \\left(
                \\frac{\\lambda_{fp}}{\\lambda_{fp}-\\lambda_{tn}},
                \\frac{-\\lambda_{tn}}{\\lambda_{fp}-\\lambda_{tn}},
                0,
                0
            \\right)

        The vertex of the quadrilateral corresponding to the intersection between
        the plane and the edge tn-fn of the tetrahedron (simplex) of importances
        is given by

        .. math::
            \\left(
                I(tn),
                I(fp),
                I(fn),
                I(tp)
            \\right) = \\left(
                \\frac{\\lambda_{fn}}{\\lambda_{fn}-\\lambda_{tn}},
                0,
                \\frac{-\\lambda_{tn}}{\\lambda_{fn}-\\lambda_{tn}},
                0
            \\right)

        The vertex of the quadrilateral corresponding to the intersection between
        the plane and the edge fp-tp of the tetrahedron (simplex) of importances
        is given by

        .. math::
            \\left(
                I(tn),
                I(fp),
                I(fn),
                I(tp)
            \\right) = \\left(
                0
                \\frac{-\\lambda_{tp}}{\\lambda_{fp}-\\lambda_{tp}},
                0,
                \\frac{\\lambda_{fp}}{\\lambda_{fp}-\\lambda_{tp}}
            \\right)

        The vertex of the quadrilateral corresponding to the intersection between
        the plane and the edge fn-tp of the tetrahedron (simplex) of importances
        is given by

        .. math::
            \\left(
                I(tn),
                I(fp),
                I(fn),
                I(tp)
            \\right) = \\left(
                0
                0,
                \\frac{-\\lambda_{tp}}{\\lambda_{fn}-\\lambda_{tp}},
                \\frac{\\lambda_{fn}}{\\lambda_{fn}-\\lambda_{tp}}
            \\right)

        Returns:
            bool: True if and only if valid.
        """
        if (
            self._lambda_tn < 0.0
            and self._lambda_fp > 0.0
            and self._lambda_fn > 0.0
            and self._lambda_tp < 0.0
        ):
            return True
        if (
            self._lambda_tn > 0.0
            and self._lambda_fp < 0.0
            and self._lambda_fn < 0.0
            and self._lambda_tp > 0.0
        ):
            return True
        return False

    def samePerformanceOrdering(self, importance: "Importance") -> "Importance":
        """
        For a valid constraint, returns an importance that leads to the same
        performance ordering as the one given in input, that satisfies the
        constraint, and such that all importance values sum up to one.

        Args:
            importance (Importance): the importance for which we want to mimic the performance ordering.

        Raises:
            RuntimeError: if this is not a valid constraint.

        Returns:
            Importance: the computed importance.
        """
        from ._importance import Importance

        assert isinstance(importance, Importance)

        if not self.isValid():
            raise RuntimeError("Only for valid constraints.")

        tn = self._lambda_tn * importance.itn
        fp = self._lambda_fp * importance.ifp
        fn = self._lambda_fn * importance.ifn
        tp = self._lambda_tp * importance.itp

        a = tp / (tn + tp)
        assert 0.0 <= a and a <= 1.0
        b = fn / (fp + fn)
        assert 0.0 <= b and b <= 1.0

        itn = -(1.0 - a) / self._lambda_tn
        ifp = (1.0 - b) / self._lambda_fp
        ifn = b / self._lambda_fn
        itp = -a / self._lambda_tp

        tot = itn + ifp + ifn + itp
        itn /= tot
        ifp /= tot
        ifn /= tot
        itp /= tot

        # check that the importance values are valid.
        assert itn >= 0.0
        assert ifp >= 0.0
        assert ifn >= 0.0
        assert itp >= 0.0

        # check that we still have the same performance ordering (the same point on Tile).
        TOL = 1e-8
        assert math.isclose(
            importance.itp / (importance.itn + importance.itp),
            itp / (itn + itp),
            abs_tol=TOL,
        )
        assert math.isclose(
            importance.ifn / (importance.ifp + importance.ifn),
            ifn / (ifp + ifn),
            abs_tol=TOL,
        )

        # check that the constraint is satisfied.
        i = Importance(itn, ifp, ifn, itp)
        assert self(i)

        return i

    def __call__(self, importance: "Importance") -> bool:
        from ._importance import Importance

        assert isinstance(importance, Importance)
        sum = 0.0
        sum += self._lambda_tn * importance.itn
        sum += self._lambda_fp * importance.ifp
        sum += self._lambda_fn * importance.ifn
        sum += self._lambda_tp * importance.itp
        return math.fabs(sum) < 1e-6

    def __str__(self) -> str:
        substrings = []

        coefs = [self._lambda_tn, self._lambda_fp, self._lambda_fn, self._lambda_tp]
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
