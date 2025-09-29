# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy.spatial import ConvexHull

from sorbetto.core.named import Named
from sorbetto.performance.roc import _setupROC
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)


class FiniteSetOfTwoClassClassificationPerformances(Named):
    # TODO: FiniteSet or Multiset ?

    def __init__(
        self,
        performance_list: list[TwoClassClassificationPerformance] | np.ndarray,
        name: str | None = None,
    ):
        if isinstance(performance_list, np.ndarray):
            self._performance_list = (
                FiniteSetOfTwoClassClassificationPerformances._from_array(
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

        self._ptn = np.array([perf.ptn for perf in self._performance_list])
        self._pfp = np.array([perf.pfp for perf in self._performance_list])
        self._pfn = np.array([perf.pfn for perf in self._performance_list])
        self._ptp = np.array([perf.ptp for perf in self._performance_list])

        default_name = "unnamed multiset of two-class classification performances"
        Named.__init__(self, default_name, name)

    @staticmethod
    def _from_array(array_tn_fp_fn_tp):
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
    def _update_probabilities(self):
        self._ptn = np.array([perf.ptn for perf in self._performance_list])
        self._pfp = np.array([perf.pfp for perf in self._performance_list])
        self._pfn = np.array([perf.pfn for perf in self._performance_list])
        self._ptp = np.array([perf.ptp for perf in self._performance_list])

    @property
    def performance_list(self) -> list[TwoClassClassificationPerformance]:
        return self._performance_list

    def getMean(self) -> TwoClassClassificationPerformance:
        """
        The mean is know as the summarized performance :cite:t:`Pierard2020Summarizing`
        as well as Fawcett's interpolated performance :cite:t:`Fawcett2006AnIntroduction`.
        """
        if len(self._performance_list) == 0:
            raise RuntimeError("The mean of an empty set of performances is undefines.")
        ptn = np.mean(self._ptn)
        pfp = np.mean(self._pfp)
        pfn = np.mean(self._pfn)
        ptp = np.mean(self._ptp)
        name = 'mean of the performances "{}"'.format(self.name)
        return TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name)

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

    def _plotBestPerformancesInROC(fpr: np.ndarray, tpr: np.ndarray, style: str) -> set:
        """
        This method assumes that all performances are for fixed priors.
        This function draws a broken line corresponding to the supremum of
        all achievable performances and returns the list of indices of all
        the entities that are on this broken line, called the supremum line.
        An entity will be part of the Entity Tile "Who's first?" if its
        performance is in this list.

        Args:
            fpr (np.ndarray): the values of false positive rate
            tpr (np.ndarray): the values of true positive rate
            style (str): the line style for matplotlib.pyplot.plot

        Returns:
            set: the set of indices of the entities on the supremum.
        """
        assert isinstance(fpr, np.ndarray)
        assert isinstance(tpr, np.ndarray)
        assert isinstance(style, str)

        n = (fpr + tpr).size
        min_fpr = np.min(fpr)
        max_tpr = np.max(tpr)
        fprs_ = np.append(fpr, [1, 1, min_fpr])
        tprs_ = np.append(tpr, [max_tpr, 0, 0])
        points = np.empty((n + 3, 2))
        points[:, 0] = fprs_
        points[:, 1] = tprs_
        hull = ConvexHull(points)
        best_entities_idx = set()
        for simplex in hull.simplices:
            for entity_idx in simplex:
                if entity_idx < n:
                    best_entities_idx.add(entity_idx)
            xs = points[simplex, 0]
            ys = points[simplex, 1]
            if np.any(xs < 1) and np.any(ys > 0):
                plt.plot(xs, ys, style)
        return best_entities_idx

    def _plotWorstPerformancesInROC(
        fpr: np.ndarray, tpr: np.ndarray, style: str
    ) -> set:
        """
        This method assumes that all performances are for fixed priors.
        This function draws a broken line corresponding to the infimum of
        all achievable performances and returns the list of indices of all
        the entities that are on this broken line, called the infimum line.
        An entity will be part of the Entity Tile "Who's last?" if its
        performance is in this list.

        Args:
            fpr (np.ndarray): the values of false positive rate
            tpr (np.ndarray): the values of true positive rate
            style (str): the line style for matplotlib.pyplot.plot

        Returns:
            set: the set of indices of the entities on the infimum.
        """
        assert isinstance(fpr, np.ndarray)
        assert isinstance(tpr, np.ndarray)
        assert isinstance(style, str)

        n = (fpr + tpr).size
        max_fpr = np.max(fpr)
        min_tpr = np.min(tpr)
        fprs_ = np.append(fpr, [max_fpr, 0, 0])
        tprs_ = np.append(tpr, [1, 1, min_tpr])
        points = np.empty((n + 3, 2))
        points[:, 0] = fprs_
        points[:, 1] = tprs_
        hull = ConvexHull(points)
        worst_entities_idx = set()
        for simplex in hull.simplices:
            for entity_idx in simplex:
                if entity_idx < n:
                    worst_entities_idx.add(entity_idx)
            xs = points[simplex, 0]
            ys = points[simplex, 1]
            if np.any(xs > 0) and np.any(ys < 1):
                plt.plot(xs, ys, style)
        return worst_entities_idx

    # TODO: A very nice idea would be to depict differently all the performances
    # that are at a given rank for some ranking score. The rank woulld be an
    # argument of the method.
    def drawInROC(
        self, fig: Figure | None = None, ax: Axes | None = None
    ) -> tuple[Figure, Axes]:
        """
        See https://en.wikipedia.org/wiki/Receiver_operating_characteristic

        Args:
            fig (Figure | None, optional): The matplotlib.pyplot Figure to use for drawing. Defaults to None in which case a new Figure is created.
            ax (Axes | None, optional): The matplotlib.pyplot Axes to use for drawing. Defaults to None in which case the current Axes are used.

        Returns:
            tuple[Figure, Axes]: The matplotlib.pyplot Figure and Axes used for drawing.
        """

        assert fig is None or isinstance(fig, Figure)
        assert ax is None or isinstance(ax, Axes)

        if fig is None:
            fig = plt.figure()
            ax = fig.gca()
        elif ax is None:
            ax = fig.gca()

        all_prior_pos = self._pfn + self._ptp
        min_prior_pos = np.min(all_prior_pos)
        max_prior_pos = np.max(all_prior_pos)
        if math.isclose(min_prior_pos, max_prior_pos, abs_tol=1e-6):
            fixed_priors = True
            prior_pos = np.mean(all_prior_pos)
            prior_neg = 1.0 - prior_pos
        else:
            fixed_priors = False

        all_fpr = self._pfp / (self._ptn + self._pfp)
        all_tpr = self._ptp / (self._pfn + self._ptp)

        num_performances = len(self._performance_list)

        if fixed_priors:
            if prior_neg < 1e-8:
                message = "The prior of the negative class is {:g}".format(prior_neg)
                message += "It is too low to produce a ROC plot."
                logging.warning(message)
                return fig, ax
            priorPos = self._prior_pos()
            if prior_pos < 1e-8:
                message = "The prior of the positive class is {:g}".format(prior_pos)
                message += "It is too low to produce a ROC plot."
                logging.warning(message)
                return fig, ax

            _setupROC(
                fig,
                ax,
                priorPos=priorPos,
                show_no_skills=True,
                show_priors=True,
                show_unbiased=True,
                show_opposite_unbiased=True,
            )

            best_entities_idx = self._plotBestPerformancesInROC(all_fpr, all_tpr, "k:")
            worst_entities_idx = self._plotWorstPerformancesInROC(
                all_fpr, all_tpr, "k:"
            )
            for e in range(num_performances):
                label = self._performance_list[e].name
                if e in worst_entities_idx:
                    plt.scatter(all_fpr[e], all_tpr[e], marker="d", s=10, label=label)
                elif e in best_entities_idx:
                    plt.scatter(all_fpr[e], all_tpr[e], marker="*", s=10, label=label)
                else:
                    plt.scatter(all_fpr[e], all_tpr[e], marker="o", s=1, label=label)

        else:
            _setupROC(fig, ax, priorPos=None, show_no_skills=True)
            # ax.plot(all_fpr, all_tpr, "o", color="blue")
            for e in range(num_performances):
                label = self._performance_list[e].name
                plt.scatter(all_fpr[e], all_tpr[e], marker="o", s=1, label=label)

        max_elements_per_colums = 18
        ax.legend(
            bbox_to_anchor=(1.05, 0.5),
            loc="center left",
            borderaxespad=0,
            ncols=1 + (num_performances - 1) / max_elements_per_colums,
        )

        return fig, ax

    def __str__(self):
        txt = (
            f"FiniteSetOfTwoClassClassificationPerformances(name={self.name} and "
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
    elif isinstance(performance, FiniteSetOfTwoClassClassificationPerformances):
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
    list_ptn_pfp_pfn_ptp = np.array(
        [
            (0.70, 0.05, 0.10, 0.15),
            (0.60, 0.10, 0.15, 0.15),
            (0.80, 0.02, 0.08, 0.10),
        ]
    )

    print(f"Used dim {list_ptn_pfp_pfn_ptp.shape}")

    finite_set = FiniteSetOfTwoClassClassificationPerformances(list_ptn_pfp_pfn_ptp)
    print(finite_set)
