from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D
import numpy as np
import jax


class Conic(AbstractGeometricObject2D):
    """
    This class is used to represent conic sections.
    $a x^2 + b x y + c y^2 + d x + e y + f = 0$
    See https://en.wikipedia.org/wiki/Conic_section
    """

    def __init__(self, a, b, c, d, e, f, name: str | None = None):
        assert isinstance(a, float)
        assert isinstance(b, float)
        assert isinstance(c, float)
        assert isinstance(d, float)
        assert isinstance(e, float)
        assert isinstance(f, float)
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
        The coefficient $a$ that multiplies $x^2 y^0$ in the equation of the conic section.

        Returns:
            float: The paramater $a$ of the conic section.
        """
        return self._a

    @property
    def b(self) -> float:
        """
        The coefficient $b$ that multiplies $x^1 y^1$ in the equation of the conic section.

        Returns:
            float: The paramater $b$ of the conic section.
        """
        return self._b

    @property
    def c(self) -> float:
        """
        The coefficient $c$ that multiplies $x^0 y^2$ in the equation of the conic section.

        Returns:
            float: The paramater $c$ of the conic section.
        """
        return self._c

    @property
    def d(self) -> float:
        """
        The coefficient $d$ that multiplies $x^1 y^0$ in the equation of the conic section.

        Returns:
            float: The paramater $d$ of the conic section.
        """
        return self._d

    @property
    def e(self) -> float:
        """
        The coefficient $e$ that multiplies $x^0 y^1$ in the equation of the conic section.

        Returns:
            float: The paramater $e$ of the conic section.
        """
        return self._e

    @property
    def f(self) -> float:
        """
        The coefficient $a$ that multiplies $x^0 y^0$ in the equation of the conic section.

        Returns:
            float: The paramater $f$ of the conic section.
        """
        return self._f

    @staticmethod
    def _solve_quadratic_equation_min(a, b, c):
        """
        Computes the lowest solution of the quadratic equation
        $a x^2 + b x^1 + c x^0 = 0$.

        Args:
            a (_type_): paramater $a$
            b (_type_): paramater $b$
            c (_type_): paramater $c$

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
        $a x^2 + b x^1 + c x^0 = 0$.

        Args:
            a (_type_): paramater $a$
            b (_type_): paramater $b$
            c (_type_): paramater $c$

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
        Computes the smallest value of $y$, for any given $x$.

        Args:
            x (_type_): $x$

        Returns:
            _type_: the smallest value of $y$, for the given $x$.
        """
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f

        #     a x^2 + b x y + c y^2 + d x + e y + f = 0 = 0
        # <=> y^2 ( c ) + y^1 ( b x + e ) + y^0 ( a x^2 + d x + f ) = 0

        A = c
        B = b * x + e
        C = a * x * x + d * x + f

        return self._solve_quadratic_equation_min(A, B, C)

    def getLargestY(self, x):
        """
        Computes the largest value of $y$, for any given $x$.

        Args:
            x (_type_): $x$

        Returns:
            _type_: the largest value of $y$, for the given $x$.
        """
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f

        #     a x^2 + b x y + c y^2 + d x + e y + f = 0
        # <=> y^2 ( c ) + y^1 ( b x + e ) + y^0 ( a x^2 + d x + f ) = 0

        A = c
        B = b * x + e
        C = (a * x + d) * x + f

        return self._solve_quadratic_equation_max(A, B, C)

    def getSmallestX(self, y):
        """
        Computes the smallest value of $x$, for any given $y$.

        Args:
            y (_type_): $y$

        Returns:
            _type_: the smallest value of $x$, for the given $y$.
        """
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f

        #     a x^2 + b x y + c y^2 + d x + e y + f = 0
        # <=> x^2 ( a ) + x^1 ( b y + d ) + x^0 ( c y^2 + e y + f ) = 0

        A = a
        B = b * y + d
        C = (c * y + e) * y + f

        return Conic._solve_quadratic_equation_min(A, B, C)

    def getLargestX(self, y):
        """
        Computes the largest value of $x$, for any given $y$.

        Args:
            y (_type_): $y$

        Returns:
            _type_: the largest value of $x$, for the given $y$.
        """
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f

        #     a x^2 + b x y + c y^2 + d x + e y + f = 0
        # <=> x^2 ( a ) + x^1 ( b y + d ) + x^0 ( c y^2 + e y + f ) = 0

        A = a
        B = b * y + d
        C = (c * y + e) * y + f

        return self._solve_quadratic_equation_max(A, B, C)

    def draw(self, fig, ax, extent, **plt_kwargs):
        """
        Draws the part of the conic section that is within some axis-aligned box in some given Pyplot axes.

        Args:
            fig (_type_): a Pyplot Figure object
            ax (_type_): a Pyplot Axes object
            extent (_type_): the axis-aligned box $(x_{min}, x_{max}, y_{min}, y_{max})$
            plt_kwargs: options for Pyplot's plot command.
        """

        x_min = extent[0]
        x_max = extent[1]
        assert x_max > x_min
        x = np.linspace(x_min, x_max, 1000)

        def draw_y_fct_of_x(f):
            y = f(x)
            grad = jax.grad(f)
            g = grad(x)
            ok = np.logical_and(np.isfinite(y), -1.0 <= g, g <= 1.0)
            ko = np.logical_not(ok)
            y[ko] = np.nan
            y[y < y_min] = np.nan
            y[y > y_max] = np.nan
            ax.plot(x, y, "-", plt_kwargs)

        draw_y_fct_of_x(self.getSmallestY)
        draw_y_fct_of_x(self.getLargestY)

        y_min = extent[2]
        y_max = extent[3]
        assert y_max > y_min
        y = x  # = np.linspace(y_min, y_max, 1000)

        def draw_x_fct_of_y(f):
            x = f(y)
            grad = jax.grad(f)
            g = grad(y)
            ok = np.logical_and(np.isfinite(x), -1.0 <= g, g <= 1.0)
            ko = np.logical_not(ok)
            x[ko] = np.nan
            x[x < x_min] = np.nan
            x[x > x_max] = np.nan
            ax.plot(x, y, "-", plt_kwargs)

        draw_x_fct_of_y(self.getSmallestX)
        draw_x_fct_of_y(self.getLargestX)

    def __str__(self) -> str:
        return "({:g}) x^2 + ({:g}) x y + ({:g}) y^2 + ({:g}) x + ({:g}) y + ({:g}) = 0".fomat(
            self.a, self.b, self.c, self.d, self.e, self.f
        )
