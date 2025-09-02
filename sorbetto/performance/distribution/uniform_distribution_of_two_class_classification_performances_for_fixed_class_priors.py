from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)
from sorbetto.performance.distribution.abstract_distribution_of_two_class_classification_performances import (
    AbstractDistributionOfTwoClassClassificationPerformances,
)
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class UniformDistributionOfTwoClassClassificationPerformancesForFixedClassPriors(
    AbstractDistributionOfTwoClassClassificationPerformances
):
    def __init__(self, priorPos: float, name: str | None = None):
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0
        self._priorPos = priorPos
        super().__init__(name)

    @property
    def priorPos(self) -> float:
        """
        The prior of the positive class.

        Returns:
            priorPos: $\\pi_+ = P( \\{ fn, tp \\} )$
        """
        return self._priorPos

    @property
    def priorNeg(self) -> float:
        """
        The prior of the negative class.

        Returns:
            priorNeg: $\\pi_- = P( \\{ tn, tp \\} )$
        """
        return 1.0 - self._priorPos

    def drawAtRandom(
        self, numPerformances: int
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        assert isinstance(numPerformances, int)
        assert numPerformances >= 0
        raise NotImplementedError()  # TODO

    def getMean(self) -> TwoClassClassificationPerformance:
        mean_tnr = 0.5
        mean_fpr = 0.5
        mean_fnr = 0.5
        mean_tpr = 0.5
        ptn = mean_tnr * self.priorNeg
        pfp = mean_fpr * self.priorNeg
        pfn = mean_fnr * self.priorPos
        ptp = mean_tpr * self.priorPos
        name = 'mean of distribution "{}"'.format(self.name)
        return TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name=name)

    def sampleOnRegularGrid(
        self, grid_size
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        raise NotImplementedError()  # TODO

    def getConstraint(self) -> ConstraintFixedClassPriors:
        return ConstraintFixedClassPriors(priorPos=self._priorPos)
