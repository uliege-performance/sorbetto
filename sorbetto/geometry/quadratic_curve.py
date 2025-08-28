from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D
import numpy as np
import jax


class QuadraticCurve(AbstractGeometricObject2D):
    """
    $a x^2 + b y^2 + c x y + d x + e y + f = 0$
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
        return self._a

    @property
    def b(self) -> float:
        return self._b

    @property
    def c(self) -> float:
        return self._c

    @property
    def d(self) -> float:
        return self._d

    @property
    def e(self) -> float:
        return self._e

    @property
    def f(self) -> float:
        return self._f

    @staticmethod
    def _solve_quadratic_equation(A, B, C):
        if A == 0.0:
            return -C / B
        else:
            D = B * B - 4.0 * A * C
            return (-B - np.sqrt(D)) / (2 * A)

    def y_min_fct_of_x(self, x):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f

        #     a x^2 + b y^2 + c x y + d x + e y + f = 0
        # <=> y^2 ( b ) + y^1 ( c x + e ) + y^0 ( a x^2 + d x + f ) = 0

        A = b
        B = c * x + e
        C = a * x * x + d * x + f

        return self._solve_quadratic_equation(A, B, C)

    def y_max_fct_of_x(self, x):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f

        #     a x^2 + b y^2 + c x y + d x + e y + f = 0
        # <=> y^2 ( b ) + y^1 ( c x + e ) + y^0 ( a x^2 + d x + f ) = 0

        A = b
        B = c * x + e
        C = (a * x + d) * x + f

        return self._solve_quadratic_equation(A, B, C)

    def x_min_fct_of_y(self, y):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f

        #     a x^2 + b y^2 + c x y + d x + e y + f = 0
        # <=> x^2 ( a ) + x^1 ( c y + d ) + x^0 ( b y^2 + e y + f ) = 0

        A = a
        B = c * y + d
        C = (b * y + e) * y + f

        return QuadraticCurve._solve_quadratic_equation(A, B, C)

    def x_max_fct_of_y(self, y):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f

        #     a x^2 + b y^2 + c x y + d x + e y + f = 0
        # <=> x^2 ( a ) + x^1 ( c y + d ) + x^0 ( b y^2 + e y + f ) = 0

        A = a
        B = c * y + d
        C = (b * y + e) * y + f

        return self._solve_quadratic_equation(A, B, C)

    def draw(self, fig, ax, extent, **plt_kwargs):
        """_summary_

        Args:
            fig (_type_): _description_
            ax (_type_): _description_
            extent (_type_): (x_min, x_max, y_min, y_max)
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

        draw_y_fct_of_x(self.y_min_fct_of_x)
        draw_y_fct_of_x(self.y_max_fct_of_x)

        y_min = extent[2]
        y_max = extent[3]
        assert y_max > y_min
        y = np.linspace(y_min, y_max, 1000)

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

        draw_x_fct_of_y(self.x_min_fct_of_y)
        draw_x_fct_of_y(self.x_max_fct_of_y)
