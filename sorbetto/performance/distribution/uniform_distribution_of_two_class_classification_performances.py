import itertools

from sorbetto.performance.distribution.abstract_distribution_of_two_class_classification_performances import (
    AbstractDistributionOfTwoClassClassificationPerformances,
)
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.performance.two_class_classification import (
    TwoClassClassificationPerformance,
)


class UniformDistributionOfTwoClassClassificationPerformances(
    AbstractDistributionOfTwoClassClassificationPerformances
):
    def __init__(self, name):
        super().__init__(name)

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

        # TODO: implement a warning if grid_size is too large.
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
