import math
from typing import Self

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.performance.abstract_performance import AbstractPerformance
from sorbetto.performance.roc import _setupROC


class TwoClassClassificationPerformance(AbstractPerformance):
    """A two-class (crisp) classification performance :math:`P` is a probability measure over the measurable space :math:`(\\Omega,\\Sigma)` where the sample (a.k.a. universe) is :math:`\\Omega=\\{tn,fp,fn,tp\\}` and the event space is :math:`\\Sigma=2^\\Omega`.
    By convention, :math:`tn`, :math:`fp`, :math:`fn`, and :math:`tp` represent the four cases that can arise: a true negative, a false positive, a false negative, and a true positive, respectively.
    The four elementary probability measures :math:`P(\\{tn\\})`, :math:`P(\\{fp\\})`, :math:`P(\\{fn\\})`, and :math:`P(\\{tp\\})` are the elements of the normalized confusion matrix.

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
        """
        The probability of a true negative, :math:`P( \\{ tn \\} )`.

        Returns:
            float: The probability of a true negative, :math:`P( \\{ tn \\} )`.
        """
        return self._ptn

    @property
    def pfp(self) -> float:
        """
        The probability of a false positive, :math:`P( \\{ fp \\} )`.

        Returns:
            float: The probability of a false positive, :math:`P( \\{ fp \\} )`.
        """
        return self._pfp

    @property
    def pfn(self) -> float:
        """
        The probability of a false negative, :math:`P( \\{ fn \\} )`.

        Returns:
            float: The probability of a false negative, :math:`P( \\{ fn \\} )`.
        """
        return self._pfn

    @property
    def ptp(self) -> float:
        """
        The probability of a true positive, :math:`P( \\{ tp \\} )`.

        Returns:
            float: The probability of a true positive, :math:`P( \\{ tp \\} )`.
        """
        return self._ptp

    def getMassFunction(self) -> np.ndarray:
        return np.array([self._ptn, self._pfp, self._pfn, self._ptp])

    @staticmethod
    def getNoSkill(
        *,
        priorNeg: float | None = None,
        priorPos: float | None = None,
        rateNeg: float | None = None,
        ratePos: float | None = None,
        name: str | None = None,
    ) -> Self:
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

    @staticmethod
    def buildFromRankingScoreValues(
        name, *pairsOfRankingScoresAndValues
    ) -> "TwoClassClassificationPerformance":
        raise NotImplementedError()

    def drawInROC(self, fig: Figure, ax: Axes) -> None:
        """
        See https://en.wikipedia.org/wiki/Receiver_operating_characteristic

        Args:
            fig (Figure): _description_
            ax (Axes): _description_
        """

        ptn = self._ptn
        pfp = self._pfp
        pfn = self._pfn
        ptp = self._ptp

        fpr = pfp / (ptn + pfp)
        tpr = ptp / (pfn + ptp)
        priorPos = self._pfn + self._ptp

        _setupROC(
            fig,
            ax,
            priorPos=priorPos,
            show_no_skills=True,
            show_priors=True,
            show_unbiased=True,
        )

        ax.plot(fpr, tpr, marker="o", label=self._name)

    def __str__(self):
        return f"TwoClassClassificationPerformance(name={self._name}, ptn={self._ptn}, pfp={self._pfp}, pfn={self._pfn}, ptp={self._ptp})"


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
