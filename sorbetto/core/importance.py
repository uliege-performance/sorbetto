import math

import numpy as np


class Importance:
    """This class encodes some application-specific preferences.
    Currently, it is a random variable, called importance,
    that gives a positive value to each element of the sample space: tn (for true negative), fp (for false positive), fn (for false negative), and tp (for true positive).

    See :cite:t:`Pierard2025Foundations` for more information on this topic.
    """

    tol = 1e-10

    def __init__(
        self,
        itn: float | int,
        ifp: float | int,
        ifn: float | int,
        itp: float | int,
        name: str = "I",
    ):
        assert isinstance(itn, (float, int))
        assert isinstance(ifp, (float, int))
        assert isinstance(ifn, (float, int))
        assert isinstance(itp, (float, int))

        if itn < 0.0 or ifp < 0.0 or ifn < 0.0 or itp < 0.0:
            raise ValueError(
                f"Importance values must be non-negative. Received [TN:{itn}, FP:{ifp}, FN:{ifn}, TP:{itp}]"
            )

        if math.isclose(itn + ifp + ifn + itp, 0.0, abs_tol=self.tol):
            raise ValueError(
                f"At least one importance value must be positive. Received [TN:{itn}, FP:{ifp}, FN:{ifn}, TP:{itp}]"
            )

        self._itn = float(itn)
        self._ifp = float(ifp)
        self._ifn = float(ifn)
        self._itp = float(itp)
        self._name = name

    @property
    def itn(self) -> float:
        return self._itn

    @property
    def ifp(self) -> float:
        return self._ifp

    @property
    def ifn(self) -> float:
        return self._ifn

    @property
    def itp(self) -> float:
        return self._itp

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other):
        if not isinstance(other, Importance):
            return False

        return (  # TODO: would math.fabs be better than abs?
            abs(self.itn - other.itn) <= self.tol
            and abs(self.ifp - other.ifp) <= self.tol
            and abs(self.ifn - other.ifn) <= self.tol
            and abs(self.itp - other.itp) <= self.tol
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
