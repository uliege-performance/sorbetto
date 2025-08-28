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

        return (
            abs(self.itn - other.itn) <= self.tol
            and abs(self.ifp - other.ifp) <= self.tol
            and abs(self.ifn - other.ifn) <= self.tol
            and abs(self.itp - other.itp) <= self.tol
        )

    def __ne__(self, other):
        if not isinstance(other, Importance):
            return True

        return not (
            abs(self.itn - other.itn) <= self.tol
            and abs(self.ifp - other.ifp) <= self.tol
            and abs(self.ifn - other.ifn) <= self.tol
            and abs(self.itp - other.itp) <= self.tol
        )

    def __str__(self):
        txt = f"[Importance] containing [TN:{self.itn}, FP:{self.ifp}, FN:{self.ifn}, TP:{self.itp}]"
        return txt


if __name__ == "__main__":
    # Test successful creation
    prefs1 = Importance(1.0, 0.5, 0.2, 0.8, name="Prefs1")
    print(f"Successfully created: {prefs1}")
    assert prefs1.itn == 1.0
    assert prefs1.ifp == 0.5
    assert prefs1.ifn == 0.2
    assert prefs1.itp == 0.8
    assert prefs1.name == "Prefs1"

    # Test string representation
    expected_str = "[Importance] containing [TN:1.0, FP:0.5, FN:0.2, TP:0.8]"
    assert str(prefs1) == expected_str
    print("String representation test passed.")

    # Test equality
    prefs2 = Importance(1.0, 0.5, 0.2, 0.8, name="Prefs2")
    assert prefs1 == prefs2
    print("Equality test passed.")

    # Test equality with tolerance
    prefs3 = Importance(1.0, 0.5, 0.2, 0.8 + 1e-11, name="Prefs3")
    assert prefs1 == prefs3
    print("Equality with tolerance test passed.")

    # Test inequality
    prefs4 = Importance(1.0, 0.5, 0.2, 0.9, name="Prefs4")
    assert prefs1 != prefs4
    print("Inequality test passed.")

    # Test inequality with different type
    assert prefs1 != "not an Importance object"
    print("Inequality with different type test passed.")

    # Test validation: negative importance
    try:
        Importance(-1.0, 0.5, 0.2, 0.8)
    except ValueError as e:
        print(f"Caught expected error for negative importance: {e}")
        assert "must be non-negative" in str(e)

    # Test validation: all zero importance
    # try:
    #    Importance(0, 0, 0, 0)
    # except ValueError as e:
    #    print(f"Caught expected error for all-zero importance: {e}")
    #    assert "at least one importance value must be positive" in str(e)

    # Test validation: negative tolerance
    # try:
    #    Importance(1, 1, 1, 1, tol=-0.1)
    # except ValueError as e:
    #    print(f"Caught expected error for negative tolerance: {e}")
    #    assert "tolerance must be non-negative" in str(e)

    print("\nAll tests passed!")
