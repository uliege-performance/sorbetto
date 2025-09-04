import math

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.performance.abstract_performance import AbstractPerformance
from sorbetto.performance.roc import setupROC


class TwoClassClassificationPerformance(AbstractPerformance):
    """A two-class (crisp) classification performance $P$ is a probability measure over the measurable space $(\\Omega,\\Sigma)$ where the sample (a.k.a. universe) is $\\Omega=\\{tn,fp,fn,tp\\}$ and the event space is $\\Sigma=2^\\Omega$.
    By convention, $tn$, $fp$, $fn$, and $tp$ represent the four cases that can arise: a true negative, a false positive, a false negative, and a true positive, respectively.
    The four elementary probability measures $P(\\{tn\\})$, $P(\\{fp\\})$, $P(\\{fn\\})$, and $P(\\{tp\\})$ are the elements of the normalized confusion matrix.

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
        The probability of a true negative, $P( \\{ tn \\} )$.

        Returns:
            float: The probability of a true negative, $P( \\{ tn \\} )$.
        """
        return self._ptn

    @property
    def pfp(self) -> float:
        """
        The probability of a false positive, $P( \\{ fp \\} )$.

        Returns:
            float: The probability of a false positive, $P( \\{ fp \\} )$.
        """
        return self._pfp

    @property
    def pfn(self) -> float:
        """
        The probability of a false negative, $P( \\{ fn \\} )$.

        Returns:
            float: The probability of a false negative, $P( \\{ fn \\} )$.
        """
        return self._pfn

    @property
    def ptp(self) -> float:
        """
        The probability of a true positive, $P( \\{ tp \\} )$.

        Returns:
            float: The probability of a true positive, $P( \\{ tp \\} )$.
        """
        return self._ptp

    def getMassFunction(self):
        return np.array([self._ptn, self._pfp, self._pfn, self._ptp])

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

        setupROC(
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
