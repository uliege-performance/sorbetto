from sorbetto.performance.constraint_fixed_prediction_rates import (
    ConstraintFixedPredictionRates,
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


class UniformDistributionOfTwoClassClassificationPerformancesForFixedPredictionRates(
    AbstractDistributionOfTwoClassClassificationPerformances
):
    def __init__(self, ratePos: float, name: str | None = None):
        assert isinstance(ratePos, float)
        assert ratePos >= 0.0
        assert ratePos <= 1.0
        self._ratePos = ratePos
        super().__init__(name)

    @property
    def ratePos(self) -> float:
        """
        The rate of predictions for the positive class.

        Returns:
            ratePos: $\\tau_+ = P( \\{ fp, tp \\} )$
        """
        return self._ratePos

    @property
    def rateNeg(self) -> float:
        """
        The rate of predictions for the negative class.

        Returns:
            rateNeg: $\\tau_- = P( \\{ tn, fn \\} )$
        """
        return 1.0 - self._ratePos

    def drawAtRandom(
        self, numPerformances: int
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        assert isinstance(numPerformances, int)
        assert numPerformances >= 0
        raise NotImplementedError()  # TODO

    def getMean(self) -> TwoClassClassificationPerformance:
        mean_npv = 0.5  # negative predictive value (a.k.a. inverse precision)
        mean_fdr = 0.5  # false discovery rate
        mean_for = 0.5  # false omission rate
        mean_ppv = 0.5  # positive predictive value (a.k.a. precision)
        ptn = mean_npv * self.rateNeg
        pfp = mean_fdr * self.ratePos
        pfn = mean_for * self.rateNeg
        ptp = mean_ppv * self.ratePos
        name = 'mean of distribution "{}"'.format(self.name)
        return TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name=name)

    def sampleOnRegularGrid(
        self, grid_size
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        raise NotImplementedError()  # TODO

    def getConstraint(self) -> ConstraintFixedPredictionRates:
        return ConstraintFixedPredictionRates(ratePos=self._ratePos)
