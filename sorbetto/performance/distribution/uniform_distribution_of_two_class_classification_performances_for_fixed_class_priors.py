from sorbetto.performance.distribution.abstract_distribution_of_two_class_classification_performances import (
    AbstractDistributionOfTwoClassClassificationPerformances,
)
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)


class UniformDistributionOfTwoClassClassificationPerformancesForFixedClassPriors(
    AbstractDistributionOfTwoClassClassificationPerformances
):
    def __init__(self, name):
        super().__init__(name)

    def sampleOnRegularGrid(
        self, grid_size
    ) -> FiniteSetOfTwoClassClassificationPerformances: ...  # TODO
