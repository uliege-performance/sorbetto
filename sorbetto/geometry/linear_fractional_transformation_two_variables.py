from sorbetto.geometry.line import Line
from sorbetto.geometry.pencil_of_lines import PencilOfLines
from sorbetto.geometry.ruler import Ruler


# TODO: Should it be in module "geometry" or in a module "algebra"?
# TODO: We will need the particular case of one variable for the change of parameterization
# TODO: We will need the particular case of one variable for functions in ROC (e.g., ranking scores)
# TODO: So, do we code several classes, or only one?
class LinearFractionalTransformationTwoVariables:
    """
    This class is used to represent linear fractional transformations of two variables.

    .. math::
        f: \\mathbb{R}^2 \\rightarrow \\mathbb{R} : (x,y) \\mapsto f(x,y) = \\frac{ a x + b y + c }{ d x + e y + f }

    See https://en.wikipedia.org/wiki/Linear_fractional_transformation
    """

    def __init__(self, a: float, b: float, c: float, d: float, e: float, f: float):
        """
        Initializes a new LinearFractionalTransformation object.

        Args:
            a (float): the parameter :math:`a` of the linear fractional transformation
            b (float): the parameter :math:`b` of the linear fractional transformation
            c (float): the parameter :math:`c` of the linear fractional transformation
            d (float): the parameter :math:`d` of the linear fractional transformation
            e (float): the parameter :math:`e` of the linear fractional transformation
            f (float): the parameter :math:`f` of the linear fractional transformation
        """
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

    @property
    def e(self) -> float:
        """
        The coefficient :math:`e`.

        Returns:
            float: The parameter :math:`e` of the linear fractional transformation.
        """
        return self._e

    @property
    def f(self) -> float:
        """
        The coefficient :math:`f`.

        Returns:
            float: The parameter :math:`f` of the linear fractional transformation.
        """
        return self._f

    def __call__(self, x: float, y: float):
        assert isinstance(x, float)
        assert isinstance(y, float)

        a = self._a
        b = self._b
        c = self._c
        d = self._d
        e = self._e
        f = self._f
        return (a * x + b * y + c) / (d * x + e * y + f)

    def getPencil(self) -> PencilOfLines:
        """
        Returns the pencil of lines corresponding to the various values taken
        by this function.

        The locus of points where the function takes a given value is a line,
        and all these lines form the pencil

        .. math::
            \\lambda_0 ( a_0 x + b_0 y + c_0 ) + \\lambda_1 ( a_1 x + b_1 y + c_1 ) = 0

        The line :math:`a_0 x + b_0 y + c_0 = 0` is the locus of points for which the
        function takes the value :math:`0`. The coefficients are given by

        * :math:`a_0 = a`
        * :math:`b_0 = b`
        * :math:`c_0 = c`

        The line :math:`a_1 x + b_1 y + c_1 = 0` is the locus of point for which the
        function takes the value :math:`1`. The coefficients are given by

        * :math:`a_1 = a - d`
        * :math:`b_1 = b - e`
        * :math:`c_1 = c - f`

        By choosing :math:`(\\lambda_0, \\lambda_1) = (1-v, v)`, one obtains a line that is the
        locus of points for which the function takes the value :math:`v`.

        Returns:
            PencilOfLines: The pencil of lines.

        """
        #     f(x,y) = v
        # <=> [ a x + b y + c ] / [ d x + e y + f ] = v
        # <=> ( a - v d ) x + ( b - v e ) y + ( c - v f ) = 0
        # <=> (1-v) [ a x + b y + c ] + v [ ( a - d ) x + ( b - e ) y + ( c - f ) ]
        # <=> (1-v) line_0 + v line_1 = 0

        # When the function takes the value v=0, we have:
        # line_0 :: a x + b y + c = 0.
        a = self._a
        b = self._b
        c = self._c
        line_0 = Line(a, b, c, "line for value 0")

        # When the score takes the value v=1, we have:
        # line_1 :: ( a - d ) x + ( b - e ) y + ( c - f ) = 0
        a = self._a - self._d
        b = self._b - self._e
        c = self._c - self._f
        line_1 = Line(a, b, c, "line for value 1")

        # name = "pencil for {}".format(self.name)
        return PencilOfLines(line_0, line_1)

    def getRuler(self, x: float, y: float, vmin: float, vmax: float, ticks) -> Ruler:
        """
        On any line with a vector direction :math:`(e, -d)`, the values taken
        by this function are linearly spread. This method returns a ruler placed
        on the line with the vector direction :math:`(e, -d)` and passing through
        the point :math:`(x, y)`.

        Args:
            x (float): The first coordinate of the point where to place the ruler, :math:`x`.
            y (float): The second coordinate of the point where to place the ruler, :math:`y`.
            vmin (float): The minimal value to show on the ruler.
            vmax (float): The maximal value to show on the ruler.
            ticks (_type_): The ticks to show on the ruler, or None if they should be determined automatically.

        Returns:
            Ruler: The ruler.
        """
        # We can read values linearly if we are on a line where the
        # denominator of f(x,y) is constant (and not zero):
        # d x + e y = cte

        d = self._d
        e = self._e

        v = self(x, y)

        dx = e
        dy = -d
        dv = self(x + dx, y + dy) - v

        # name = "ruler for {}".format(self.name)
        return Ruler(x, y, v, dx, dy, dv, vmin, vmax, ticks)

    def __str__(self) -> str:
        a = self._a
        b = self._b
        c = self._c
        d = self._d
        e = self._e
        f = self._f
        return "linear fractional transformation ( ({}) x + ({}) y + ({}) ) / ( ({}) x + ({}) y + ({}) )".format(
            a, b, c, d, e, f
        )
