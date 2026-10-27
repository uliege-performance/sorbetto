# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
import math
from typing import Self

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.core.matplotlib_utils import _setupROC

from ._abstract_performance import AbstractPerformance


class TwoClassClassificationPerformance(AbstractPerformance):
    r"""
    A two-class (crisp) classification performance :math:`P` is a probability
    measure over the measurable space :math:`(\Omega,\Sigma)` where the sample
    (a.k.a. universe) is :math:`\Omega=\{tn,fp,fn,tp\}` and the event space is
    :math:`\Sigma=2^\Omega`.  By convention, :math:`tn`, :math:`fp`, :math:`fn`,
    and :math:`tp` represent the four cases that can arise: a true negative, a
    false positive, a false negative, and a true positive, respectively.  The
    four elementary probability measures :math:`P(\{tn\})`, :math:`P(\{fp\})`,
    :math:`P(\{fn\})`, and :math:`P(\{tp\})` are the elements of the normalized
    confusion matrix.

    See :cite:t:`Pierard2025Foundations` for more information on this topic."""

    tol = 1e-10

    def __init__(
        self,
        ptn: float,
        pfp: float,
        pfn: float,
        ptp: float,
        name: str | None = None,
    ):
        assert isinstance(ptn, float)
        assert isinstance(pfp, float)
        assert isinstance(pfn, float)
        assert isinstance(ptp, float)
        assert ptn >= 0
        assert pfp >= 0
        assert pfn >= 0
        assert ptp >= 0
        sum = ptn + pfp + pfn + ptp
        assert math.isclose(sum, 1.0, abs_tol=1e-8)

        self._ptn = ptn
        self._pfp = pfp
        self._pfn = pfn
        self._ptp = ptp

        if name is None:
            name = "unnamed two-class classification performance"
        else:
            if not isinstance(name, str):
                name = str(name)
        super().__init__(name=name)

    @property
    def ptn(self) -> float:
        r"""
        The probability of a true negative, :math:`P( \{ tn \} )`.

        Returns:
            float: The probability of a true negative, :math:`P( \{ tn \} )`.
        """
        return self._ptn

    @property
    def pfp(self) -> float:
        r"""
        The probability of a false positive, :math:`P( \{ fp \} )`.

        Returns:
            float: The probability of a false positive, :math:`P( \{ fp \} )`.
        """
        return self._pfp

    @property
    def pfn(self) -> float:
        r"""
        The probability of a false negative, :math:`P( \{ fn \} )`.

        Returns:
            float: The probability of a false negative, :math:`P( \{ fn \} )`.
        """
        return self._pfn

    @property
    def ptp(self) -> float:
        r"""
        The probability of a true positive, :math:`P( \{ tp \} )`.

        Returns:
            float: The probability of a true positive, :math:`P( \{ tp \} )`.
        """
        return self._ptp

    # TODO: should we add @property?
    def getMassFunction(self) -> np.ndarray:
        return np.array([self._ptn, self._pfp, self._pfn, self._ptp])

    # TODO: should we add @property?
    def _accuracy(self) -> float:
        return self.ptn + self.ptp

    # TODO: should we add @property?
    def _tnr(self) -> float:
        return self.ptn / (self.ptn + self.pfp)

    # TODO: should we add @property?
    def _fpr(self) -> float:
        return self.pfp / (self.ptn + self.pfp)

    # TODO: should we add @property?
    def _fnr(self) -> float:
        return self.pfn / (self.pfn + self.pfp)

    # TODO: should we add @property?
    def _tpr(self) -> float:
        return self.ptp / (self.pfn + self.ptp)

    # TODO: should we add @property?
    def _npv(self) -> float:
        return self.ptn / (self.ptn + self.pfn)

    # TODO: should we add @property?
    def _ppv(self) -> float:
        return self.ptp / (self.pfp + self.ptp)

    # TODO: should we add @property?
    def _prior_neg(self) -> float:
        return self.ptn + self.pfp

    # TODO: should we add @property?
    def _prior_pos(self) -> float:
        return self.pfn + self.ptp

    # TODO: should we add @property?
    def _rate_neg(self) -> float:
        return self.ptn + self.pfn

    # TODO: should we add @property?
    def _rate_pos(self) -> float:
        return self.pfp + self.ptp

    @staticmethod
    def getNoSkill(
        *,
        priorNeg: float | None = None,
        priorPos: float | None = None,
        rateNeg: float | None = None,
        ratePos: float | None = None,
        name: str | None = None,
    ) -> Self:
        r"""
        Computes the performance of the no-skill classifier fo the given class
        priors and the prediction rates. A performance :math:`P` is said "no-skill"
        if and only if :math:`P(Y,\hat{Y}) = P(Y) P(\hat{Y})`.

        Args:
            priorNeg (float | None, optional): The prior of the negative class, :math:`\pi_- = P( Y=c_- )`. If set to None, it is computed as :math:`1-\pi_+`. Defaults to None.
            priorPos (float | None, optional): The prior of the positive class, :math:`\pi_+ = P( Y=c_+ )`. If set to None, it is computed as :math:`1-\pi_-`. Defaults to None.
            rateNeg (float | None, optional): The rate of negative predictions, :math:`\tau_- = P( \hat{Y}=c_- )`. If set to None, it is computed as :math:`1-\tau_+`. Defaults to None.
            ratePos (float | None, optional): The rate of negative predictions, :math:`\tau_+ = P( \hat{Y}=c_+ )`. If set to None, it is computed as :math:`1-\tau_-`. Defaults to None.
            name (str | None, optional): _description_. The name of the no-skill performance. Defaults to None.

        Returns:
            Self: The no-skill performance.
        """

        def snoopy(v1: float | None = None, v2: float | None = None):
            if v1 is not None:
                assert isinstance(v1, float)
                assert 0.0 <= v1 and v1 <= 1.0
            if v2 is not None:
                assert isinstance(v2, float)
                assert 0.0 <= v2 and v2 <= 1.0

            if v1 is None:
                if v2 is None:
                    assert False
                else:
                    v1 = 1.0 - v2
            else:
                if v2 is None:
                    v2 = 1.0 - v1
                else:
                    assert math.isclose(v1 + v2, 1.0, abs_tol=1e-8)

            return v1, v2

        priorNeg, priorPos = snoopy(priorNeg, priorPos)
        rateNeg, ratePos = snoopy(rateNeg, ratePos)

        ptn = priorNeg * rateNeg
        pfp = priorNeg * ratePos
        pfn = priorPos * rateNeg
        ptp = priorPos * ratePos

        return TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name)

    def toNoSkillCohen(self) -> Self:
        """
        Returns the no-skill performance that is considered as achievable by
        chance by Cohen in his definition of the score kappa.

        For SciPy users, this is what `scipy.stats.contingency.expected_freq`
        computes when fed with a normalized confusion matrix.

        Returns:
            Self: the computed no-skill performance.
        """
        ptn = self._prior_neg() * self._rate_neg()
        pfp = self._prior_neg() * self._rate_pos()
        pfn = self._prior_pos() * self._rate_neg()
        ptp = self._prior_pos() * self._rate_pos()

        return TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, "no-skill")

    def toNoSkillScottFleiss(self) -> Self:
        """
        Returns the no-skill performance that is considered as achievable by
        chance by Scott in his definition of the score pi as well as by Fleiss
        in his definition of the score kappa.

        Returns:
            Self: the computed no-skill performance.
        """
        proba_neg = 0.5 * (self._prior_neg() + self._rate_neg())
        proba_pos = 0.5 * (self._prior_pos() + self._rate_pos())

        ptn = proba_neg * proba_neg
        pfp = proba_neg * proba_pos
        pfn = proba_pos * proba_neg
        ptp = proba_pos * proba_pos

        return TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, "no-skill")

    def isNoSkill(self) -> bool:
        ptn = self._ptn
        pfp = self._pfp
        pfn = self._pfn
        ptp = self._ptp

        fpr = pfp / (ptn + pfp)
        tpr = ptp / (pfn + ptp)

        return np.isclose(tpr, fpr, atol=self.tol)  # type: ignore

    def isAboveNoSkills(self) -> bool:
        ptn = self._ptn
        pfp = self._pfp
        pfn = self._pfn
        ptp = self._ptp

        fpr = pfp / (ptn + pfp)
        tpr = ptp / (pfn + ptp)

        return (tpr - self.tol) >= fpr

    def isBelowNoSkills(self) -> bool:
        ptn = self._ptn
        pfp = self._pfp
        pfn = self._pfn
        ptp = self._ptp

        fpr = pfp / (ptn + pfp)
        tpr = ptp / (pfn + ptp)

        return (tpr + self.tol) <= fpr

    def __eq__(self, other) -> bool:
        comps = np.isclose(
            [self._ptn, self._pfp, self._pfn, self._ptp],
            [other._ptn, other._pfp, other._pfn, other._ptp],
            atol=self.tol,
        )
        return np.all(comps)  # type: ignore

    def __ne__(self, other):
        return not self.__eq__(other)

    def buildForConstantCanonicalRankingScoreValue(
        value: float,
    ) -> "TwoClassClassificationPerformance":
        """
        Builds a two-class classification performance such that all canonical
        ranking scores (ie, the ranking scores such that :math:`I(tn)+I(tp)=1`
        and :math:`I(fp)+I(fn)=1`) take the same value, given in argument.

        See footnote number 7 in :cite:t:`Pierard2025AMethodology`.

        Args:
            value (float): The value to be taken by all canonical ranking scores, between 0.0 and 1.0.

        Returns:
            TwoClassClassificationPerformance: The two-class classification performance.
        """
        assert isinstance(value, float)
        assert value >= 0.0
        assert value <= 1.0
        ptn = 0.5 * value
        pfp = 0.5 * (1.0 - value)
        pfn = 0.5 * (1.0 - value)
        ptp = 0.5 * value
        name = "Performance for which all canonical ranking scores take the value {:g}".format(
            value
        )
        return TwoClassClassificationPerformance(ptn, pfp, pfn, ptp, name)

    @staticmethod
    def buildFromRankingScoreValues(
        name, *pairsOfRankingScoresAndValues
    ) -> "TwoClassClassificationPerformance":
        raise NotImplementedError()

    def drawInROC(
        self,
        fig: Figure | None = None,
        ax: Axes | None = None,
        color_classifier: str | np.ndarray | None = "blue",
        color_classifier_opp: str | np.ndarray | None = "black",
        color_classifier_neg: str | np.ndarray | None = "black",
        color_classifier_pos: str | np.ndarray | None = "black",
        show_no_skills: bool = True,
        show_priors: bool = True,
        show_unbiased: bool = True,
        show_opposite_unbiased: bool = True,
    ) -> tuple[Figure, Axes]:
        """
        See https://en.wikipedia.org/wiki/Receiver_operating_characteristic

        Args:
            fig (Figure | None, optional): The matplotlib.pyplot Figure to use for drawing. Defaults to None in which case a new Figure is created.
            ax (Axes | None, optional): The matplotlib.pyplot Axes to use for drawing. Defaults to None in which case the current Axes are used.
            color_classifier (_type_, optional): The color of the point that represents the classifier. Defaults to "blue".
            color_classifier_opp (_type_, optional): The color of the point that represents the opposite classifier. Defaults to "black".
            color_classifier_neg (_type_, optional): The color of the point that represents the no-skill classifier predicting the negative class with a probability of 1. Defaults to "black".
            color_classifier_pos (_type_, optional):The color of the point that represents the no-skill classifier predicting the positive class with a probability of 1. Defaults to "black".

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

        priorNeg = self._prior_neg()
        if priorNeg < 1e-8:
            message = "The prior of the negative class is {:g}".format(priorNeg)
            message += "It is too low to produce a ROC plot."
            logging.warning(message)
            return fig, ax
        priorPos = self._prior_pos()
        if priorPos < 1e-8:
            message = "The prior of the positive class is {:g}".format(priorPos)
            message += "It is too low to produce a ROC plot."
            logging.warning(message)
            return fig, ax

        fpr = self._fpr()
        tpr = self._tpr()

        ax.fill(
            [0.0, fpr, 1.0, 1.0 - fpr], [0.0, tpr, 1.0, 1 - tpr], facecolor="lightgray"
        )

        _setupROC(
            fig,
            ax,
            priorPos=priorPos,
            show_no_skills=show_no_skills,
            show_priors=show_priors,
            show_unbiased=show_unbiased,
            show_opposite_unbiased=show_opposite_unbiased,
        )

        def drawPointAndLabel(x, y, label, color):
            ax.plot(x, y, marker="o", label=label, color=color)
            center_x = 0.5
            center_y = 0.5
            if x < center_x:
                if y < center_y:
                    ax.text(x, y, label, ha="left", va="bottom", color=color)
                else:
                    ax.text(x, y, label, ha="left", va="top", color=color)
            else:
                if y < center_y:
                    ax.text(x, y, label, ha="right", va="bottom", color=color)
                else:
                    ax.text(x, y, label, ha="right", va="top", color=color)

        drawPointAndLabel(fpr, tpr, r"$\mathcal{C}$", color_classifier)
        drawPointAndLabel(
            1.0 - fpr, 1.0 - tpr, r"$\overline{\mathcal{C}}$", color_classifier_opp
        )
        drawPointAndLabel(0.0, 0.0, r"$\mathcal{C}_-$", color_classifier_neg)
        drawPointAndLabel(1.0, 1.0, r"$\mathcal{C}_+$", color_classifier_pos)

        return fig, ax

    def __str__(self):
        return f"TwoClassClassificationPerformance(name={self.name}, ptn={self._ptn}, pfp={self._pfp}, pfn={self._pfn}, ptp={self._ptp})"


if __name__ == "__main__":
    perf = TwoClassClassificationPerformance(0.9, 0.1, 0.05, 0.95, name="MyPerf")
    print(perf)
    print("isNoSkill:", perf.isNoSkill())
    print("isAboveNoSkills:", perf.isAboveNoSkills())
    print("isBelowNoSkills:", perf.isBelowNoSkills())
    print("getMassFunction:", perf.getMassFunction())

    # no skill
    perf = TwoClassClassificationPerformance(0.5, 0.5, 0.5, 0.5, name="NoSkillPerf")
    print(perf)
    print("isNoSkill:", perf.isNoSkill())
    print("isAboveNoSkills:", perf.isAboveNoSkills())
    print("isBelowNoSkills:", perf.isBelowNoSkills())
    print("getMassFunction:", perf.getMassFunction())

    perf = TwoClassClassificationPerformance(0.1, 0.9, 0.95, 0.05, name="BadSkillPerf")
    print(perf)
    print("isNoSkill:", perf.isNoSkill())
    print("isAboveNoSkills:", perf.isAboveNoSkills())
    print("isBelowNoSkills:", perf.isBelowNoSkills())
    print("getMassFunction:", perf.getMassFunction())
