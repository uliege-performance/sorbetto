import logging

from sorbetto.performance.two_class_classification import (
    TwoClassClassificationPerformance,
)


def getTpr(tp, fn):
    return tp / (tp + fn)


def getFpr(fp, tn):
    return fp / (fp + tn)


class FiniteSetOfTwoClassClassificationPerformances:
    # TODO: list or dict ?
    # TODO: FiniteSet or Multiset ?

    def __init__(
        self,
        performance_list: list[TwoClassClassificationPerformance],
        name: str = "finite set",
    ):
        self._performance_list = performance_list
        self._name = name

    @property
    def performance_list(self) -> list[TwoClassClassificationPerformance]:
        return self._performance_list

    @property
    def name(self) -> str:
        return self._name

    def getMean(self) -> TwoClassClassificationPerformance:
        """
        The mean is know as the summarized performance as well as Fawcett's interpolated performance.

        """

        ...  # TODO

    def getRange(self, score) -> tuple[float, float]:
        try:
            score_vals = score(
                [perf.getMassFunction() for perf in self._performance_list]
            )
        except Exception as e:
            logging.warning(
                f"Warning: issue encountered with vectorized score function: {e}"
            )

            score_vals = [
                score(perf.getMassFunction()) for perf in self._performance_list
            ]

        min_val = min(score_vals)
        max_val = max(score_vals)

        return (min_val, max_val)

    def drawInROC(self, fig, ax):  # and options ?
        for perf in self._performance_list:
            perf.drawInROC(fig, ax)

    def getWorstValueTile(self, parameterization):  # and options ?
        ...  # TODO

    def getBestValueTile(self, parameterization):  # and options ?
        ...  # TODO

    def __str__(self):
        txt = f"FiniteSetOfTwoClassClassificationPerformances(name={self._name}, performances={self._performance_list})"

        return txt
