# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import Self


# TODO: Should it be in module "geometry" or in a module "algebra"?
# TODO: We will need the particular case of one variable for the change of parameterization
# TODO: We will need the particular case of one variable for functions in ROC (e.g., ranking scores)
# TODO: So, do we code several classes, or only one?
class LinearFractionalTransformation:
    """
    This class is used to represent linear fractional transformations.

    .. math::
        f : \\mathbb{R} \\rightarrow \\mathbb{R} : x \\mapsto \\frac{ a x + b }{ c x + d }

    See https://en.wikipedia.org/wiki/Linear_fractional_transformation
    """

    def __init__(self, a: float, b: float, c: float, d: float):
        """
        Initializes a new LinearFractionalTransformation object.

        Args:
            a (float): the parameter :math:`a` of the linear fractional transformation
            b (float): the parameter :math:`b` of the linear fractional transformation
            c (float): the parameter :math:`c` of the linear fractional transformation
            d (float): the parameter :math:`d` of the linear fractional transformation
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
        The coefficient :math:`a`.

        Returns:
            float: The parameter :math:`a` of the linear fractional transformation.
        """
        return self._a

    @property
    def b(self) -> float:
        """
        The coefficient :math:`b`.

        Returns:
            float: The parameter :math:`b` of the linear fractional transformation.
        """
        return self._b

    @property
    def c(self) -> float:
        """
        The coefficient :math:`c`.

        Returns:
            float: The parameter :math:`c` of the linear fractional transformation.
        """
        return self._c

    @property
    def d(self) -> float:
        """
        The coefficient :math:`d`.

        Returns:
            float: The parameter :math:`d` of the linear fractional transformation.
        """
        return self._d

    def __call__(self, x: float):
        assert isinstance(x, float)

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
        if math.isclose(a * d, b * c):
            raise RuntimeError("The invertibility condition is not satisfied.")
        return LinearFractionalTransformation(d, -b, -c, a)

    def __str__(self) -> str:
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        return "linear fractional transformation ( ({}) x + ({}) ) / ( ({}) x + ({}) )".format(
            a, b, c, d
        )
