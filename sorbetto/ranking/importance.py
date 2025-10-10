# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math

import numpy as np

from sorbetto.core.named import Named


class Importance(Named):
    """This class encodes some application-specific preferences.
    Currently, it is a random variable, called importance,
    that gives a positive value to each element of the sample space: tn (for true negative), fp (for false positive), fn (for false negative), and tp (for true positive).

    See :cite:t:`Pierard2025Foundations` for more information on this topic.
    """

    TOL: float = 1e-10
    """Tolerance used for floating  comparisons."""

    def __init__(
        self,
        itn: float | int,
        ifp: float | int,
        ifn: float | int,
        itp: float | int,
        name: str | None = None,
    ):
        """
        Args:
            itn (float | int): importance of the true negatives
            ifp (float | int): importance of the false positives
            ifn (float | int): importance of the false negatives
            itp (float | int): importance of the true positives
            name (str | None, optional): name of this Importance. Defaults to None.

        Raises:
            ValueError: if one of the importance values is negative, or if all
                importance values are zero.
        """
        assert isinstance(itn, (float, int))
        assert isinstance(ifp, (float, int))
        assert isinstance(ifn, (float, int))
        assert isinstance(itp, (float, int))

        if itn < 0.0 or ifp < 0.0 or ifn < 0.0 or itp < 0.0:
            raise ValueError(
                f"Importance values must be non-negative. Received [TN:{itn}, FP:{ifp}, FN:{ifn}, TP:{itp}]"
            )

        if math.isclose(itn + ifp + ifn + itp, 0.0, abs_tol=self.TOL):
            raise ValueError(
                f"At least one importance value must be positive. Received [TN:{itn}, FP:{ifp}, FN:{ifn}, TP:{itp}]"
            )

        self._itn = float(itn)
        self._ifp = float(ifp)
        self._ifn = float(ifn)
        self._itp = float(itp)

        Named.__init__(self, "I", name)

    @property
    def itn(self) -> float:
        """
        The importance of true negatives.
        """
        return self._itn

    @property
    def ifp(self) -> float:
        """
        The importance of false positives.
        """
        return self._ifp

    @property
    def ifn(self) -> float:
        """
        The importance of false negatives.
        """
        return self._ifn

    @property
    def itp(self) -> float:
        """
        The importance of true positives.
        """
        return self._itp

    def isCanonical(self, abs_tol: float = 1e-8) -> bool:
        """
        Tests if

        .. math::
            I(tn)+I(tp) = I(fp)+I(fn)

        Args:
            abs_tol (float, optional): The absolute tolerance to use for the comparison of :math:`I(tn)+I(tp)` with :math:`I(fp)+I(fn)`. Defaults to 1e-8.

        Returns:
            bool: True if the Importance is canonical, False otherwise.
        """
        itn = self._itn
        ifp = self._ifp
        ifn = self._ifn
        itp = self._itp

        return math.isclose(itn + itp, ifp + ifn, abs_tol=abs_tol)

    def __eq__(self, other):
        if not isinstance(other, Importance):
            return False

        return (  # TODO: would math.fabs be better than abs?
            abs(self.itn - other.itn) <= self.TOL
            and abs(self.ifp - other.ifp) <= self.TOL
            and abs(self.ifn - other.ifn) <= self.TOL
            and abs(self.itp - other.itp) <= self.TOL
        )

    def __str__(self):
        txt = f"[Importance] containing [TN:{self.itn}, FP:{self.ifp}, FN:{self.ifn}, TP:{self.itp}]"
        return txt


# TODO get even better typing there (output as tuple of single type, based on inputs)
def _parse_importance(
    importance: Importance | list[Importance] | np.ndarray | None = None,
    itn: float | int | np.ndarray | None = None,
    ifp: float | int | np.ndarray | None = None,
    ifn: float | int | np.ndarray | None = None,
    itp: float | int | np.ndarray | None = None,
) -> tuple[
    float | int | np.ndarray,
    float | int | np.ndarray,
    float | int | np.ndarray,
    float | int | np.ndarray,
]:
    if isinstance(importance, Importance):
        itn_ = importance.itn
        ifp_ = importance.ifp
        ifn_ = importance.ifn
        itp_ = importance.itp
    elif isinstance(importance, np.ndarray):
        assert importance.shape[-1] == 4
        itn_ = importance[..., 0]
        ifp_ = importance[..., 1]
        ifn_ = importance[..., 2]
        itp_ = importance[..., 3]
    elif isinstance(importance, list):
        itn_ = np.array([imp.itn for imp in importance])
        ifp_ = np.array([imp.ifp for imp in importance])
        ifn_ = np.array([imp.ifn for imp in importance])
        itp_ = np.array([imp.itp for imp in importance])
    else:
        if (itn is None) or (ifp is None) or (ifn is None) or (itp is None):
            raise ValueError(
                "Either importance or all itn, ifp, ifn, itp must be provided."
            )
        itn_, ifp_, ifn_, itp_ = itn, ifp, ifn, itp

    return itn_, ifp_, ifn_, itp_
