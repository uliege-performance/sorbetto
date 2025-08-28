class Importance:
    """This class encodes some application-specific preferences.
    Currently, it is a random variable, called importance,
    that gives a positive value to each element of the sample space: tn (for true negative), fp (for false positive), fn (for false negative), and tp (for true positive).

    See :cite:t:`Pierard2025Foundations` for more information on this topic.
    """

    def __init__(
        self,
        itn: float,
        ifp: float,
        ifn: float,
        itp: float,
        name: str = "I",
        tol: float = 1e-10,
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

        if tol < 0:
            raise ValueError(
                f"Tolerance must be non-negative. Received [Tolerance:{tol}]"
            )

        self._itn = itn
        self._ifp = ifp
        self._ifn = ifn
        self._itp = itp
        self._name = name
        self._tol = tol

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
    def tol(self) -> float:
        return self._tol

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other):
        if not isinstance(other, Importance):
            return False

        # TODO should there be a close function with the tolerance, and equality be exact?
        # If not, which tolerance to use? self.tol, other.tol, max(self.tol, other.tol), min(self.tol, other.tol)?

        return (
            abs(self.itn - other.itn) <= self.tol
            and abs(self.ifp - other.ifp) <= self.tol
            and abs(self.ifn - other.ifn) <= self.tol
            and abs(self.itp - other.itp) <= self.tol
        )

    def __str__(self):
        txt = f"[Importance] containing [TN:{self.itn}, FP:{self.ifp}, FN:{self.ifn}, TP:{self.itp}]"
        return txt
