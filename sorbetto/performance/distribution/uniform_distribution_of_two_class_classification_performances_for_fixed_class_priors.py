import random

import numpy as np

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
    """
    The instances of this class represent a uniform distribution of two-class classification
    performances over the part of the performance space that corresponds to some given
    class priors. Geometricaly, this part is the intersection of the tetrahedron with a plane,
    and is a rectangle.

    It can be shown that the True Negative Rate (TNR), the False Positive Rate (FPR),
    the False Negative Rate (FNR), and True Positive Rate (TPR) are all uniformly distributed
    random variables over [0, 1]. Moreover, the TNR (or FPR) and FNR (or TPR) are
    independent. In fact, TNR (or FPR) and FNR (or TPR) are the two Cartesian
    coordinates of a performance within the rectangle of interest.
    """

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
            priorPos: :math:`\\pi_+ = P( \\{ fn, tp \\} )`
        """
        return self._priorPos

    @property
    def priorNeg(self) -> float:
        """
        The prior of the negative class.

        Returns:
            priorNeg: :math:`\\pi_- = P( \\{ tn, tp \\} )`
        """
        return 1.0 - self._priorPos

    def drawOneAtRandom(self) -> TwoClassClassificationPerformance:
        """
        Draw a two-class classification performances at random,
        uniformy, in the performances corresponding to fixed class prios.

        Returns:
            TwoClassClassificationPerformance: the performance.
        """
        priorNeg = self.priorNeg
        priorPos = self.priorPos

        name = "randomly chosen performance"

        tnr = random.random()  # true negative rate
        tpr = random.random()  # true positive rate
        fpr = 1.0 - tnr  # false positive rate
        fnr = 1.0 - tpr  # false negative rate

        ptn = tnr * priorNeg  # probability of a true negative
        pfp = fpr * priorNeg  # probability of a false positive
        pfn = fnr * priorPos  # probability of a false negative
        ptp = tpr * priorPos  # probability of a true positive

        p = TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name=name)
        return p

    def drawAtRandom(
        self, numPerformances: int
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        """
        Draw `numPerformances` two-class classification performances at random,
        uniformy, in the performances corresponding to fixed class prios.

        Args:
            numPerformances (int): the amount of performances to draw.

        Returns:
            FiniteSetOfTwoClassClassificationPerformances: the (multi)set.
        """
        assert isinstance(numPerformances, int)
        assert numPerformances >= 0

        priorNeg = self.priorNeg
        priorPos = self.priorPos

        name = "randomly chosen performance"

        performances = list()
        for _ in range(numPerformances):
            tnr = random.random()  # true negative rate
            tpr = random.random()  # true positive rate
            fpr = 1.0 - tnr  # false positive rate
            fnr = 1.0 - tpr  # false negative rate

            ptn = tnr * priorNeg  # probability of a true negative
            pfp = fpr * priorNeg  # probability of a false positive
            pfn = fnr * priorPos  # probability of a false negative
            ptp = tpr * priorPos  # probability of a true positive

            p = TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name=name)
            performances.append(p)

        return FiniteSetOfTwoClassClassificationPerformances(performances)

    def getMean(self) -> TwoClassClassificationPerformance:
        """
        Computes the mean of the distribution.
        """
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
        self, gridSize: int, open: bool = False
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        """
        Sample the rectangle of two-class classification performances corresponding
        to the fixed class priors on a regular grid of size `gridSize`.

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

        priorNeg = self.priorNeg
        priorPos = self.priorPos

        if open:
            min_tnr, max_tnr = 0.5 / n, 1.0 - 0.5 / n
            min_tpr, max_tpr = 0.5 / n, 1.0 - 0.5 / n
        else:
            min_tnr, max_tnr = 0.0, 1.0
            min_tpr, max_tpr = 0.0, 1.0

        performances = list()
        for tnr in np.linspace(min_tnr, max_tnr, n):
            fpr = 1.0 - tnr
            for tpr in np.linspace(min_tpr, max_tpr, n):
                fnr = 1.0 - tpr

                ptn = tnr * priorNeg
                pfp = fpr * priorNeg
                pfn = fnr * priorPos
                ptp = tpr * priorPos

                p = TwoClassClassificationPerformance(ptn, pfp, pfn, ptp)
                performances.append(p)

        return FiniteSetOfTwoClassClassificationPerformances(performances)

    def getConstraint(self) -> ConstraintFixedClassPriors:
        """
        Provide the constraint that corresponds to the fixed class priors.

        Returns:
            ConstraintFixedClassPriors: The constraint.
        """
        return ConstraintFixedClassPriors(priorPos=self._priorPos)
