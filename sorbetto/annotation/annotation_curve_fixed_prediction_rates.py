import math

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.performance.constraint_fixed_prediction_rates import (
    ConstraintFixedPredictionRates,
)
from sorbetto.tile.tile import Tile


class AnnotationCurveFixedPredictionRates(AbstractAnnotation):
    def __init__(
        self,
        ratePos: float | ConstraintFixedPredictionRates,
        name: str | None = None,
        **plt_kwargs,
    ):
        if isinstance(ratePos, ConstraintFixedPredictionRates):
            ratePos = ratePos.getRatePos()
        assert isinstance(ratePos, float)
        assert ratePos > 0.0
        assert ratePos < 1.0
        self._ratePos = ratePos

        if name is None:
            name = "locus of performance orderings putting all no-skill performances with the prediction rates ({:g}, {:g}) on an equal footing".format(
                1.0 - ratePos, ratePos
            )
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: Tile, fig: Figure, ax: Axes) -> None:
        assert isinstance(tile, Tile)

        flavor = tile.flavor
        if isinstance(flavor, ValueFlavor):
            performance = flavor.performance
            ratePos = performance.pfp + performance.ptp
            if not math.isclose(ratePos, self._ratePos, abs_tol=1e-6):
                raise RuntimeError("wrong prediction rates")

        parameterization = tile.parameterization
        min1, max1 = parameterization.getBoundsParameter1()
        min2, max2 = parameterization.getBoundsParameter2()
        extent = [min1, max1, min2, max2]

        curve = parameterization.locateOrderingsPuttingNoSkillPerformancesOnAnEqualFootingForFixedPredictionRates(
            self._ratePos
        )

        curve.draw(fig, ax, extent, **self._plt_kwargs)
