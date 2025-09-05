import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.geometry.conic import Conic


class BilinearCurve(Conic):
    """
    This class is used to represent bilinear curves:
    :math:`K_{xy} x y + K_x x + K_y y + K = 0`.
    These are particular cases of conic sections.
    :math:`a x^2 + b x y + c y^2 + d x + e y + f = 0`
    where :math:`a=0`, :math:`b=K_{xy}`, :math:`c=0`, :math:`d=K_x`, :math:`e=K_y`, and :math:`f=K`.
    """

    def __init__(self, Kxy, Kx, Ky, K, name: str | None = None):
        a = 0.0
        b = Kxy
        c = 0.0
        d = Kx
        e = Ky
        f = K
        Conic.__init__(self, a, b, c, d, e, f, name)

    def getY(self, x):
        """
        Computes the value of :math:`y`, for any given :math:`x`.

        Args:
            x (_type_): :math:`x`

        Returns:
            _type_: the value of :math:`y`, for the given :math:`x`.
        """
        assert self._a == 0.0
        Kxy = self._b
        assert self._c == 0.0
        Kx = self._d
        Ky = self._e
        K = self._f

        #     Kxy x y + Kx x + Ky y + K = 0
        # <=> y ( Kxy x + Ky ) + ( Kx x + K ) = 0
        # <=> y = - ( Kx x + K ) / ( Kxy x + Ky )

        return -(Kx * x + K) / (Kxy * x + Ky)
        # TODO: This equation is a linear fractional transformation. We have a class to represent it.
        #       It could be useful to have a method returning it.

    def getX(self, y):
        """
        Computes the value of :math:`x`, for any given :math:`y`.

        Args:
            y (_type_): :math:`y`

        Returns:
            _type_: the value of :math:`x`, for the given :math:`y`.
        """
        assert self._a == 0.0
        Kxy = self._b
        assert self._c == 0.0
        Kx = self._d
        Ky = self._e
        K = self._f

        #     Kxy x y + Kx x + Ky y + K = 0
        # <=> x ( Kxy y + Kx ) + ( Ky y + K ) = 0
        # <=> x = - ( Ky y + K ) / ( Kxy y + Kx )

        return -(Ky * y + K) / (Kxy * y + Kx)
        # TODO: This equation is a linear fractional transformation. We have a class to represent it.
        #       It could be useful to have a method returning it.

    def draw(self, fig: Figure, ax: Axes, extent, **plt_kwargs):
        """
        Draws the part of the bilinear curve that is within some axis-aligned box in some given Pyplot axes.

        Args:
            fig (_type_): a Pyplot Figure object
            ax (_type_): a Pyplot Axes object
            extent (_type_): the axis-aligned box :math:`(x_{min}, x_{max}, y_{min}, y_{max})`
            plt_kwargs: options for Pyplot's plot command.
        """

        assert self._a == 0.0
        Kxy = self._b
        assert self._c == 0.0
        Kx = self._d
        Ky = self._e
        K = self._f

        x_min, x_max, y_min, y_max = extent
        assert x_max > x_min
        assert y_max > y_min

        if Kx != 0.0 or Kxy != 0.0:
            # Let's plot x = - ( Ky y + K ) / ( Kxy y + Kx )
            # where -1 <= dx/dy <= 1
            y = np.linspace(y_min, y_max, 1000)
            num = Ky * y + K
            den = Kxy * y + Kx
            x = -num / den
            out_of_bounds = np.logical_or(x < x_min, x > x_max)
            d_num_d_y = Ky
            d_den_d_y = Kxy
            d_x_d_y = -(d_num_d_y * den - d_den_d_y * num) / (den * den)
            bad = np.logical_or(np.abs(d_x_d_y) >= 1.0 + 1e-8, out_of_bounds)
            x[bad] = np.nan  # slope is too high
            y[bad] = np.nan  # slope is too high
            ax.plot(x, y, "-", **plt_kwargs)

        if Ky != 0.0 or Kxy != 0.0:
            # Let's plot y = - ( Kx x + K ) / ( Kxy x + Ky )
            # where -1 <= dy/dx <= 1
            x = np.linspace(x_min, x_max, 1000)
            num = Kx * x + K
            den = Kxy * x + Ky
            y = -num / den
            out_of_bounds = np.logical_or(y < y_min, y > y_max)
            d_num_d_x = Kx
            d_den_d_x = Kxy
            d_y_d_x = -(d_num_d_x * den - d_den_d_x * num) / (den * den)
            bad = np.logical_or(np.abs(d_y_d_x) >= 1.0 + 1e-8, out_of_bounds)
            x[bad] = np.nan  # slope is too high
            y[bad] = np.nan  # slope is too high
            ax.plot(x, y, "-", **plt_kwargs)

    def __str__(self) -> str:
        assert self._a == 0.0
        Kxy = self._b
        assert self._c == 0.0
        Kx = self._d
        Ky = self._e
        K = self._f

        return ("{} ({:g}) x y + ({:g}) x + ({:g}) y + ({:g}) = 0").format(
            "bilinear curve", Kxy, Kx, Ky, K
        )
