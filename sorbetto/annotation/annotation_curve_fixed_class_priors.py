from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)
from sorbetto.tile.tile import Tile


class AnnotationCurveFixedClassPriors(AbstractAnnotation):
    def __init__(
        self,
        priorPos: float | ConstraintFixedClassPriors,
        name: str | None = None,
        **plt_kwargs,
    ):
        if isinstance(priorPos, ConstraintFixedClassPriors):
            priorPos = priorPos.getPriorPos()
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        self._priorPos = priorPos

        if name is None:
            name = "locus of performance orderings putting all no-skill performances with the class priors ({:g}, {:g}) on an equal footing".format(
                1.0 - priorPos, priorPos
            )
        else:
            if not isinstance(name, str):
                name = str(name)

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    def draw(self, tile: Tile, fig: Figure, ax: Axes) -> None:
        assert isinstance(tile, Tile)

        parameterization = tile.parameterization
        min1, max1 = parameterization.getBoundsParameter1()
        min2, max2 = parameterization.getBoundsParameter2()
        extent = [min1, max1, min2, max2]

        curve = parameterization.locateOrderingsPuttingNoSkillPerformancesOnAnEqualFootingForFixedClassPriors(
            self._priorPos
        )

        curve.draw(fig, ax, extent, **self._plt_kwargs)
