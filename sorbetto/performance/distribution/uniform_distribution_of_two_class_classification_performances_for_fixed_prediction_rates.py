import random

import numpy as np

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
    """
    The instances of this class represent a uniform distribution of two-class classification
    performances over the part of the performance space that corresponds to some given
    prediction rates. Geometricaly, this part is the intersection of the tetrahedron with a plane,
    and is a rectangle.

    It can be shown that the Negative Predictive Value (NPV), the False Discovery Rate (FDR),
    the False Omission Rate (FOR), and Posiitive Predictive Value (PPV) are all uniformly distributed
    random variables over [0, 1]. Moreover, the NPV (or FOR) and PPV (or FDR) are
    independent. In fact, NPV (or FOR) and PPV (or FDR) are the two Cartesian
    coordinates of a performance within the rectangle of interest.
    """

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
            ratePos: :math:`\\tau_+ = P( \\{ fp, tp \\} )`
        """
        return self._ratePos

    @property
    def rateNeg(self) -> float:
        """
        The rate of predictions for the negative class.

        Returns:
            rateNeg: :math:`\\tau_- = P( \\{ tn, fn \\} )`
        """
        return 1.0 - self._ratePos

    def drawOneAtRandom(self) -> TwoClassClassificationPerformance:
        """
        Draw a two-class classification performances at random,
        uniformy, in the performances corresponding to fixed prediction rates.

        Returns:
            TwoClassClassificationPerformance: the performance.
        """
        rateNeg = self.rateNeg
        ratePos = self.ratePos

        name = "randomly chosen performance"

        val_npv = random.random()  # negative predictive value
        val_ppv = random.random()  # positive predictive value
        val_for = 1.0 - val_npv  # false omission rate
        val_fdr = 1.0 - val_ppv  # false discovery rate

        ptn = val_npv * rateNeg  # probability of a true negative
        pfp = val_fdr * ratePos  # probability of a false positive
        pfn = val_for * rateNeg  # probability of a false negative
        ptp = val_ppv * ratePos  # probability of a true positive

        p = TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name=name)
        return p

    def drawAtRandom(
        self, numPerformances: int
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        """
        Draw `numPerformances` two-class classification performances at random,
        uniformy, in the performances corresponding to fixed prediction rates.

        Args:
            numPerformances (int): the amount of performances to draw.

        Returns:
            FiniteSetOfTwoClassClassificationPerformances: the (multi)set.
        """
        assert isinstance(numPerformances, int)
        assert numPerformances >= 0

        rateNeg = self.rateNeg
        ratePos = self.ratePos

        name = "randomly chosen performance"

        performances = list()
        for _ in range(numPerformances):
            val_npv = random.random()  # negative predictive value
            val_ppv = random.random()  # positive predictive value
            val_for = 1.0 - val_npv  # false omission rate
            val_fdr = 1.0 - val_ppv  # false discovery rate

            ptn = val_npv * rateNeg  # probability of a true negative
            pfp = val_fdr * ratePos  # probability of a false positive
            pfn = val_for * rateNeg  # probability of a false negative
            ptp = val_ppv * ratePos  # probability of a true positive

            p = TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name=name)
            performances.append(p)

        return FiniteSetOfTwoClassClassificationPerformances(performances)

    def getMean(self) -> TwoClassClassificationPerformance:
        """
        Computes the mean of the distribution.
        """
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
        self, gridSize: int, open: bool = False
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        """
        Sample the rectangle of two-class classification performances corresponding
        to the fixed prediction rates on a regular grid of size `gridSize`.

        Args:
            gridSize (_type_): The size of the grid.
            open (bool, optional): Whether the borders are excluded. Defaults to False.

        Returns:
            FiniteSetOfTwoClassClassificationPerformances: The `gridSize` times `gridSize` performances.
        """

        assert isinstance(gridSize, int)
        assert gridSize >= 0
        n = gridSize

        assert isinstance(open, bool)

        if n == 0:
            performances = list()
            return FiniteSetOfTwoClassClassificationPerformances(performances)

        rateNeg = self.rateNeg
        ratePos = self.ratePos

        if open:
            min_npv, max_npv = 0.5 / n, 1.0 - 0.5 / n
            min_ppv, max_ppv = 0.5 / n, 1.0 - 0.5 / n
        else:
            min_npv, max_npv = 0.0, 1.0
            min_ppv, max_ppv = 0.0, 1.0

        performances = list()
        for val_npv in np.linspace(min_npv, max_npv, n):
            val_for = 1.0 - val_npv
            for val_ppv in np.linspace(min_ppv, max_ppv, n):
                val_fdr = 1.0 - val_ppv

                ptn = val_npv * rateNeg  # probability of a true negative
                pfp = val_fdr * ratePos  # probability of a false positive
                pfn = val_for * rateNeg  # probability of a false negative
                ptp = val_ppv * ratePos  # probability of a true positive

                p = TwoClassClassificationPerformance(ptn, pfp, pfn, ptp)
                performances.append(p)

        return FiniteSetOfTwoClassClassificationPerformances(performances)

    def getConstraint(self) -> ConstraintFixedPredictionRates:
        """
        Provide the constraint that corresponds to the fixed prediction rates.

        Returns:
            ConstraintFixedClassPriors: The constraint.
        """
        return ConstraintFixedPredictionRates(ratePos=self._ratePos)
