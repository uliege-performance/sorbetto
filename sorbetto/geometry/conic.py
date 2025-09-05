import logging
import math

import jax
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D


class Conic(AbstractGeometricObject2D):
    """
    This class is used to represent conic sections.
    :math:`a x^2 + b x y + c y^2 + d x + e y + f = 0`
    See https://en.wikipedia.org/wiki/Conic_section
    """

    def __init__(self, a, b, c, d, e, f, name: str | None = None):
        assert isinstance(a, float)
        assert isinstance(b, float)
        assert isinstance(c, float)
        assert isinstance(d, float)
        assert isinstance(e, float)
        assert isinstance(f, float)
        if a == 0.0 and b == 0:
            # FIXME: what happens if we initialize a BilinearCurve object, which in its __init__ calls
            # the __init__ of its parent class Conic? In this case, I think that we will print the
            # warning while we should not.
            logging.warning(
                "Using conic sections where the more efficient bilinear curves could be used."
            )
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        self._e = e
        self._f = f
        AbstractGeometricObject2D.__init__(self, name)

    @property
    def a(self) -> float:
        """
        The coefficient :math:`a` that multiplies :math:`x^2 y^0` in the equation of the conic section.

        Returns:
            float: The paramater :math:`a` of the conic section.
        """
        return self._a

    @property
    def b(self) -> float:
        """
        The coefficient :math:`b` that multiplies :math:`x^1 y^1` in the equation of the conic section.

        Returns:
            float: The paramater :math:`b` of the conic section.
        """
        return self._b

    @property
    def c(self) -> float:
        """
        The coefficient :math:`c` that multiplies :math:`x^0 y^2` in the equation of the conic section.

        Returns:
            float: The paramater :math:`c` of the conic section.
        """
        return self._c

    @property
    def d(self) -> float:
        """
        The coefficient :math:`d` that multiplies :math:`x^1 y^0` in the equation of the conic section.

        Returns:
            float: The paramater :math:`d` of the conic section.
        """
        return self._d

    @property
    def e(self) -> float:
        """
        The coefficient :math:`e` that multiplies :math:`x^0 y^1` in the equation of the conic section.

        Returns:
            float: The paramater :math:`e` of the conic section.
        """
        return self._e

    @property
    def f(self) -> float:
        """
        The coefficient :math:`a` that multiplies :math:`x^0 y^0` in the equation of the conic section.

        Returns:
            float: The paramater :math:`f` of the conic section.
        """
        return self._f

    def getMatrixRepresentation(self) -> np.ndarray:
        """
        Computes the 3 by 3 matrix representation of the conic section.
        See https://en.wikipedia.org/wiki/Matrix_representation_of_conic_sections

        Returns:
            np.nparray: the matrix representation
        """
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        e = self._e
        f = self._f

        return np.array(
            [[a, 0.5 * b, 0.5 * d], [0.5 * b, c, 0.5 * e], [0.5 * d, 0.5 * e, f]]
        )

    def isDegenerate(self, tol: float = 1e-8) -> bool:
        """
        See https://en.wikipedia.org/wiki/Degenerate_conic

        Args:
            tol (float, optional): the numerical tolerance, positive. Defaults to 1e-8.

        Returns:
            bool: True if the conic section is degenerate; False otherwise
        """
        det = np.linalg.det(self.getMatrixRepresentation())

        return math.isclose(det, 0.0, abs_tol=tol)

    def isEllipse(self, tol: float = 1e-8) -> bool:
        """
        Test if the conic section is an ellipse.

        Args:
            tol (float, optional): the numerical tolerance, positive. Defaults to 1e-8.

        Returns:
            bool: True if the conic section is an ellipse; False otherwise
        """
        a = self._a
        b = self._b
        c = self._c

        test_1 = b * b - 4.0 * a * c < 0.0
        test_2 = not self.isParabola(tol)
        return test_1 and test_2

    def isCircle(self, tol: float = 1e-8) -> bool:
        """
        Test if the conic section is a circle.

        Args:
            tol (float, optional): the numerical tolerance, positive. Defaults to 1e-8.

        Returns:
            bool: True if the conic section is a circle; False otherwise
        """
        a = self._a
        b = self._b
        c = self._c

        return (
            self.isEllipse()
            and math.isclose(a, c, abs_tol=tol)
            and math.isclose(b, 0.0, abs_tol=tol)
        )

    def isParabola(self, tol: float = 1e-8) -> bool:
        """
        Test if the conic section is a parabola.

        Args:
            tol (float, optional): the numerical tolerance, positive. Defaults to 1e-8.

        Returns:
            bool: True if the conic section is a parabola; False otherwise
        """
        a = self._a
        b = self._b
        c = self._c

        return math.isclose(b * b - 4.0 * a * c, 0.0, abs_tol=tol)

    def isHyperbola(self, tol: float = 1e-8) -> bool:
        """
        Test if the conic section is a hyperbola.

        Args:
            tol (float, optional): the numerical tolerance, positive. Defaults to 1e-8.

        Returns:
            bool: True if the conic section is a hyperbola; False otherwise
        """
        a = self._a
        b = self._b
        c = self._c

        test_1 = b * b - 4.0 * a * c > 0.0
        test_2 = not self.isParabola(tol)
        return test_1 and test_2

    def isRectangularHyperbola(self, tol: float = 1e-8) -> bool:
        """
        Test if the conic section is a rectangular hyperbola.

        Args:
            tol (float, optional): the numerical tolerance, positive. Defaults to 1e-8.

        Returns:
            bool: True if the conic section is a rectangular hyperbola; False otherwise
        """
        a = self._a
        c = self._c

        return self.isParabola(tol) and a + c == 0.0

    def classify(self, tol: float = 1e-8) -> str:
        """
        Classify the conic section.

        Args:
            tol (float, optional): the numerical tolerance, positive. Defaults to 1e-8.

        Returns:
            str: a name, in english, for the conic section type
        """
        # TODO: should we have some numerical tolerance in this test?
        if self.isParabola(tol):
            return "degenerate parabola" if self.isDegenerate(tol) else "parabola"
        if self.isCircle(tol):
            return "degenerate circle" if self.isDegenerate(tol) else "circle"
        if self.isEllipse(tol):
            return "degenerate ellipse" if self.isDegenerate(tol) else "ellipse"
        if self.isRectangularHyperbola(tol):
            return (
                "degenerate rectangular hyperbola"
                if self.isDegenerate(tol)
                else "rectangular hyperbola"
            )
        if self.isHyperbola(tol):
            return "degenerate hyperbola" if self.isDegenerate(tol) else "hyperbola"
        return "unknown type of conic section"  # this should never happen

    @staticmethod
    def _solve_quadratic_equation_min(a, b, c):
        """
        Computes the lowest solution of the quadratic equation
        :math:`a x^2 + b x^1 + c x^0 = 0`.

        Args:
            a (_type_): paramater :math:`a`
            b (_type_): paramater :math:`b`
            c (_type_): paramater :math:`c`

        Returns:
            _type_: The lowest solution.
        """
        if a == 0.0:
            return -c / b
        else:
            d = b * b - 4.0 * a * c
            return (-b - np.sqrt(d)) / (2.0 * a)

    @staticmethod
    def _solve_quadratic_equation_max(a, b, c):
        """
        Computes the highest solution of the quadratic equation
        :math:`a x^2 + b x^1 + c x^0 = 0`.

        Args:
            a (_type_): paramater :math:`a`
            b (_type_): paramater :math:`b`
            c (_type_): paramater :math:`c`

        Returns:
            _type_: The highest solution.
        """
        if a == 0.0:
            return -c / b
        else:
            d = b * b - 4.0 * a * c
            return (-b + np.sqrt(d)) / (2.0 * a)

    def getSmallestY(self, x):
        """
        Computes the smallest value of :math:`y`, for any given :math:`x`.

        Args:
            x (_type_): :math:`x`

        Returns:
            _type_: the smallest value of :math:`y`, for the given :math:`x`.
        """
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        e = self._e
        f = self._f

        #     a x^2 + b x y + c y^2 + d x + e y + f = 0
        # <=> y^2 ( c ) + y^1 ( b x + e ) + y^0 ( a x^2 + d x + f ) = 0

        A = c
        B = b * x + e
        C = a * x * x + d * x + f

        return self._solve_quadratic_equation_min(A, B, C)

    def getLargestY(self, x):
        """
        Computes the largest value of :math:`y`, for any given :math:`x`.

        Args:
            x (_type_): :math:`x`

        Returns:
            _type_: the largest value of :math:`y`, for the given :math:`x`.
        """
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        e = self._e
        f = self._f

        #     a x^2 + b x y + c y^2 + d x + e y + f = 0
        # <=> y^2 ( c ) + y^1 ( b x + e ) + y^0 ( a x^2 + d x + f ) = 0

        A = c
        B = b * x + e
        C = (a * x + d) * x + f

        return self._solve_quadratic_equation_max(A, B, C)

    def getSmallestX(self, y):
        """
        Computes the smallest value of :math:`x`, for any given :math:`y`.

        Args:
            y (_type_): :math:`y`

        Returns:
            _type_: the smallest value of :math:`x`, for the given :math:`y`.
        """
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        e = self._e
        f = self._f

        #     a x^2 + b x y + c y^2 + d x + e y + f = 0
        # <=> x^2 ( a ) + x^1 ( b y + d ) + x^0 ( c y^2 + e y + f ) = 0

        A = a
        B = b * y + d
        C = (c * y + e) * y + f

        return Conic._solve_quadratic_equation_min(A, B, C)

    def getLargestX(self, y):
        """
        Computes the largest value of :math:`x`, for any given :math:`y`.

        Args:
            y (_type_): :math:`y`

        Returns:
            _type_: the largest value of :math:`x`, for the given :math:`y`.
        """
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        e = self._e
        f = self._f

        #     a x^2 + b x y + c y^2 + d x + e y + f = 0
        # <=> x^2 ( a ) + x^1 ( b y + d ) + x^0 ( c y^2 + e y + f ) = 0

        A = a
        B = b * y + d
        C = (c * y + e) * y + f

        return self._solve_quadratic_equation_max(A, B, C)

    def draw(self, fig: Figure, ax: Axes, extent, **plt_kwargs):
        """
        Draws the part of the conic section that is within some axis-aligned box in some given Pyplot axes.

        Args:
            fig (_type_): a Pyplot Figure object
            ax (_type_): a Pyplot Axes object
            extent (_type_): the axis-aligned box :math:`(x_{min}, x_{max}, y_{min}, y_{max})`
            plt_kwargs: options for Pyplot's plot command.
        """

        x_min, x_max, y_min, y_max = extent
        assert x_max > x_min
        assert y_max > y_min

        x = np.linspace(x_min, x_max, 1000)

        def draw_y_fct_of_x(f):
            y = f(x)
            y[y < y_min] = np.nan
            y[y > y_max] = np.nan
            grad = jax.grad(f)
            g = np.empty(x.shape)
            for i in range(x.size):
                if np.isfinite(y[i]):
                    g[i] = grad(x[i])
                else:
                    g[i] = np.nan
            ok = np.logical_and(np.isfinite(y), -1.0 <= g, g <= 1.0)
            ko = np.logical_not(ok)
            y[ko] = np.nan
            ax.plot(x, y, "-", **plt_kwargs)

        draw_y_fct_of_x(self.getSmallestY)
        draw_y_fct_of_x(self.getLargestY)

        y = x  # = np.linspace(y_min, y_max, 1000)

        def draw_x_fct_of_y(f):
            x = f(y)
            x[x < x_min] = np.nan
            x[x > x_max] = np.nan
            grad = jax.grad(f)
            g = np.empty(y.shape)
            for i in range(y.size):
                if np.isfinite(x[i]):
                    g[i] = grad(y[i])
                else:
                    g[i] = np.nan
            ok = np.logical_and(np.isfinite(x), -1.0 <= g, g <= 1.0)
            ko = np.logical_not(ok)
            x[ko] = np.nan
            ax.plot(x, y, "-", **plt_kwargs)

        draw_x_fct_of_y(self.getSmallestX)
        draw_x_fct_of_y(self.getLargestX)

    def __str__(self) -> str:
        return (
            "{} ({:g}) x^2 + ({:g}) x y + ({:g}) y^2 + ({:g}) x + ({:g}) y + ({:g}) = 0"
        ).format(self.classify(), self.a, self.b, self.c, self.d, self.e, self.f)
