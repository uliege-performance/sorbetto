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
        itn: float,
        ifp: float,
        ifn: float,
        itp: float,
        name: str = "I",
    ):
        assert isinstance(itn, (int, float))
        assert isinstance(ifp, (int, float))
        assert isinstance(ifn, (int, float))
        assert isinstance(itp, (int, float))

        if itn < 0 or ifp < 0 or ifn < 0 or itp < 0:
            raise ValueError(
                f"Importance values must be non-negative. Received [TN:{itn}, FP:{ifp}, FN:{ifn}, TP:{itp}]"
            )

        if itn == 0 and ifp == 0 and ifn == 0 and itp == 0:
            raise ValueError(
                f"At least one importance value must be positive. Received [TN:{itn}, FP:{ifp}, FN:{ifn}, TP:{itp}]"
            )

        self._itn = itn
        self._ifp = ifp
        self._ifn = ifn
        self._itp = itp
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

        return (
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
    itn: float | np.ndarray | None = None,
    ifp: float | np.ndarray | None = None,
    ifn: float | np.ndarray | None = None,
    itp: float | np.ndarray | None = None,
) -> tuple[
    float | np.ndarray,
    float | np.ndarray,
    float | np.ndarray,
    float | np.ndarray,
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
