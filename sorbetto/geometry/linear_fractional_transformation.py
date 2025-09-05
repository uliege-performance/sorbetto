from typing import Self


class LinearFractionalTransformation:
    """
    This class is used to represent linear fractional transformations.
    $x \\mapsto \\frac{ a x + b }{ c x + d }$
    https://en.wikipedia.org/wiki/Linear_fractional_transformation
    """

    def __init__(self, a: float, b: float, c: float, d: float):
        """
        Initializes a new LinearFractionalTransformation object.

        Args:
            a (float): the paramater $a$ of the linear fractional transformation
            b (float): the paramater $b$ of the linear fractional transformation
            c (float): the paramater $c$ of the linear fractional transformation
            d (float): the paramater $d$ of the linear fractional transformation
        """
        assert isinstance(a, float)
        assert isinstance(b, float)
        assert isinstance(c, float)
        assert isinstance(d, float)
        self._a = a
        self._b = b
        self._c = c
        self._d = d

    @property
    def a(self) -> float:
        """
        The coefficient $a$.

        Returns:
            float: The paramater $a$ of the linear fractional transformation.
        """
        return self._a

    @property
    def b(self) -> float:
        """
        The coefficient $b$.

        Returns:
            float: The paramater $b$ of the linear fractional transformation.
        """
        return self._b

    @property
    def c(self) -> float:
        """
        The coefficient $c$.

        Returns:
            float: The paramater $c$ of the linear fractional transformation.
        """
        return self._c

    @property
    def d(self) -> float:
        """
        The coefficient $d$.

        Returns:
            float: The paramater $d$ of the linear fractional transformation.
        """
        return self._d

    def __call__(self, x):
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        return (a * x + b) / (c * x + d)

    def getInverse(self) -> Self:
        """
        Computes the inverse of this linear fractional transformation.

        Returns:
            Self: the inverse linear fractional transformation
        """
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        return LinearFractionalTransformation(d, -b, c, -a)

    def __str__(self):
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        return "linear fractional transformation ( ({}) x + ({}) ) / ( ({}) x + ({}) )".format(
            a, b, c, d
        )
