import itertools
import logging

import numpy as np

from sorbetto.performance.distribution.abstract_distribution_of_two_class_classification_performances import (
    AbstractDistributionOfTwoClassClassificationPerformances,
)
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class UniformDistributionOfTwoClassClassificationPerformances(
    AbstractDistributionOfTwoClassClassificationPerformances
):
    """
    All instances of this class represent the uniform distribution of two-class classification performances,
    over the whole performance space. This is equivalent to a Dirichlet distribution with all concentration
    parameters set to one.

    See https://en.wikipedia.org/wiki/Continuous_uniform_distribution
    See https://en.wikipedia.org/wiki/Dirichlet_distribution
    """

    def __init__(self, name):
        super().__init__(name)

    def drawOneAtRandom(self) -> TwoClassClassificationPerformance:
        """
        Draw a two-class classification performances at random,
        uniformy, in the set of all performances.

        Returns:
            TwoClassClassificationPerformance: the performance.
        """

        name = "randomly chosen performance"

        concentration_parameters = [1, 1, 1, 1]  # for uniform
        numPerformances = 1
        mat = np.random.dirichlet(concentration_parameters, size=numPerformances)
        ptn = mat[0, 0]
        pfp = mat[0, 1]
        pfn = mat[0, 2]
        ptp = mat[0, 3]

        p = TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name=name)
        return p

    def drawAtRandom(
        self, numPerformances
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        concentration_parameters = [1, 1, 1, 1]  # for uniform
        mat = np.random.dirichlet(concentration_parameters, size=numPerformances)
        # ptn = mat [ :, 0 ]
        # pfp = mat [ :, 1 ]
        # pfn = mat [ :, 2 ]
        # ptp = mat [ :, 3 ]
        return FiniteSetOfTwoClassClassificationPerformances(
            mat, name="random performances"
        )

    def getMean(self) -> TwoClassClassificationPerformance:
        """
        Computes the mean of the distribution.
        """
        ptn = 0.25
        pfp = 0.25
        pfn = 0.25
        ptp = 0.25
        name = 'mean of distribution "{}"'.format(self.name)
        return TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name=name)

    def sampleOnRegularGrid(
        self, grid_size: int
    ) -> FiniteSetOfTwoClassClassificationPerformances:
        """_summary_

        Args:
            grid_size (int): _description_

        Returns:
            FiniteSetOfTwoClassClassificationPerformances: _description_

        Yields:
            Iterator[FiniteSetOfTwoClassClassificationPerformances]: _description_
        """

        assert isinstance(grid_size, int)
        assert grid_size > 0
        if grid_size >= 300:
            raise RuntimeError(
                "You are asking for too many performances. Use a grid size smaller than 300."
            )
        elif grid_size >= 180:
            logging.warning(
                "You are asking for a huge amount of performances. With a grid size larger than 180, "
                "you are going to obtain more than one million performances."
            )

        def gen():
            ss = [0, 1, 2, 3]
            for seq in itertools.combinations_with_replacement(ss, grid_size):
                ptn = seq.count(0) / grid_size
                pfp = seq.count(1) / grid_size
                pfn = seq.count(2) / grid_size
                ptp = seq.count(3) / grid_size
                yield TwoClassClassificationPerformance(ptn, pfp, pfn, ptp)

        performance_list = list(gen())
        return FiniteSetOfTwoClassClassificationPerformances(
            performance_list, "uniform grid of performances"
        )
