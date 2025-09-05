import logging

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


def _getTpr(tp, fn):  # TODO: remove this
    return tp / (tp + fn)


def _getFpr(fp, tn):  # TODO: remove this
    return fp / (fp + tn)


class FiniteSetOfTwoClassClassificationPerformances:
    # TODO: list or dict ?
    # TODO: FiniteSet or Multiset ?

    def __init__(
        self,
        performance_list: list[TwoClassClassificationPerformance] | np.ndarray,
        name: str = "finite set",
    ):
        if isinstance(performance_list, np.ndarray):
            self._performance_list = (
                FiniteSetOfTwoClassClassificationPerformances.from_array(
                    performance_list
                ).performance_list
            )
        elif isinstance(performance_list, list):
            if len(performance_list) > 0:
                if isinstance(performance_list[0], TwoClassClassificationPerformance):
                    self._performance_list = performance_list
                else:
                    raise ValueError(
                        "The performance list must contain TwoClassClassificationPerformance instances"
                    )
            else:
                raise ValueError("The performance list cannot be empty")

        else:
            raise ValueError(
                "The performance_list must be a list of TwoClassClassificationPerformance instances or a numpy array"
            )

        self._name = name
        self._ptn = np.array([perf.ptn for perf in self._performance_list])
        self._pfp = np.array([perf.pfp for perf in self._performance_list])
        self._pfn = np.array([perf.pfn for perf in self._performance_list])
        self._ptp = np.array([perf.ptp for perf in self._performance_list])

    @staticmethod
    def from_array(array_tn_fp_fn_tp):
        performance_list = []
        for tn, fp, fn, tp in array_tn_fp_fn_tp:
            performance = TwoClassClassificationPerformance(
                ptn=tn, pfp=fp, pfn=fn, ptp=tp
            )
            performance_list.append(performance)
        return FiniteSetOfTwoClassClassificationPerformances(performance_list)

    @property
    def ptn(self) -> np.ndarray:
        return self._ptn

    @property
    def pfp(self) -> np.ndarray:
        return self._pfp

    @property
    def pfn(self) -> np.ndarray:
        return self._pfn

    @property
    def ptp(self) -> np.ndarray:
        return self._ptp

    # NOTE: if we add or remove a performance, we must call this method
    def update_probabilities(self):
        self._ptn = np.array([perf.ptn for perf in self._performance_list])
        self._pfp = np.array([perf.pfp for perf in self._performance_list])
        self._pfn = np.array([perf.pfn for perf in self._performance_list])
        self._ptp = np.array([perf.ptp for perf in self._performance_list])

    @property
    def performance_list(self) -> list[TwoClassClassificationPerformance]:
        return self._performance_list

    @property
    def name(self) -> str:
        return self._name

    def getMean(self) -> TwoClassClassificationPerformance:
        """
        The mean is know as the summarized performance :cite:t:`Pierard2020Summarizing`
        as well as Fawcett's interpolated performance :cite:t:`Fawcett2006AnIntroduction`.
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

    def drawInROC(self, fig: Figure, ax: Axes):  # and options ?
        for perf in self._performance_list:
            perf.drawInROC(fig, ax)

    def __str__(self):
        txt = (
            f"FiniteSetOfTwoClassClassificationPerformances(name={self._name} and "
            f"performances=\n{'\n'.join(str(self._performance_list[i]) for i in range(len(self._performance_list)))})"
        )

        return txt

    def __iter__(self):
        return iter(self._performance_list)

    def __getitem__(self, index: int) -> TwoClassClassificationPerformance:
        if index < 0 or index >= len(self._performance_list):
            raise IndexError("Index out of range")
        return self._performance_list[index]

    def __len__(self):
        return len(self._performance_list)


def _parse_performance(
    performance: TwoClassClassificationPerformance
    | FiniteSetOfTwoClassClassificationPerformances
    | np.ndarray
    | None = None,
    ptn: float | np.ndarray | None = None,
    pfp: float | np.ndarray | None = None,
    pfn: float | np.ndarray | None = None,
    ptp: float | np.ndarray | None = None,
) -> tuple[
    float | np.ndarray,
    float | np.ndarray,
    float | np.ndarray,
    float | np.ndarray,
]:
    if isinstance(performance, TwoClassClassificationPerformance):
        ptn_: float | np.ndarray = performance.ptn
        pfp_: float | np.ndarray = performance.pfp
        pfn_: float | np.ndarray = performance.pfn
        ptp_: float | np.ndarray = performance.ptp
    elif isinstance(performance, (FiniteSetOfTwoClassClassificationPerformances)):
        ptn_ = performance.ptn[:, np.newaxis, np.newaxis]
        pfp_ = performance.pfp[:, np.newaxis, np.newaxis]
        pfn_ = performance.pfn[:, np.newaxis, np.newaxis]
        ptp_ = performance.ptp[:, np.newaxis, np.newaxis]
    elif isinstance(performance, np.ndarray):
        assert performance.shape[-1] == 4
        ptn_ = performance[..., 0][:, np.newaxis, np.newaxis]
        pfp_ = performance[..., 1][:, np.newaxis, np.newaxis]
        pfn_ = performance[..., 2][:, np.newaxis, np.newaxis]
        ptp_ = performance[..., 3][:, np.newaxis, np.newaxis]
    else:
        if (ptn is None) or (pfp is None) or (pfn is None) or (ptp is None):
            raise ValueError(
                "Either performance or all ptn, pfp, pfn, ptp must be provided."
            )
        ptn_, pfp_, pfn_, ptp_ = ptn, pfp, pfn, ptp
    return ptn_, pfp_, pfn_, ptp_


if __name__ == "__main__":
    import numpy as np

    # Example usage
    list_tn_fp_fn_tp = np.array(
        [
            (0.70, 0.05, 0.10, 0.15),
            (0.60, 0.10, 0.15, 0.15),
            (0.80, 0.02, 0.08, 0.10),
        ]
    )

    print(f"Used dim {list_tn_fp_fn_tp.shape}")

    finite_set = FiniteSetOfTwoClassClassificationPerformances(list_tn_fp_fn_tp)
    print(finite_set)
