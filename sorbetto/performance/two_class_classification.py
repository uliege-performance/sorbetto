import numpy as np

from sorbetto.performance.abstract_performance import AbstractPerformance


def getTpr(tp, fn):
    return tp / (tp + fn)


def getFpr(fp, tn):
    return fp / (fp + tn)


class TwoClassClassificationPerformance(AbstractPerformance):
    """A two-class (crisp) classification performance $P$ is a probability measure over the measurable space $(\\Omega,\\Sigma)$ where the sample (a.k.a. universe) is $\\Omega=\\{tn,fp,fn,tp\\}$ and the event space is $\\Sigma=2^\\Omega$.
    By convention, $tn$, $fp$, $fn$, and $tp$ represent the four cases that can arise: a true negative, a false positive, a false negative, and a true positive, respectively.
    The four elementary probability measures $P(\\{tn\\})$, $P(\\{fp\\})$, $P(\\{fn\\})$, and $P(\\{tp\\})$ are the elements of the normalized confusion matrix.

    See :cite:t:`Pierard2025Foundations` for more information on this topic."""

    tol = 1e-10

    def __init__(self, ptn, pfp, pfn, ptp, name: str = "Two class P"):
        self._ptn = ptn
        self._pfp = pfp
        self._pfn = pfn
        self._ptp = ptp

        super().__init__(name=name)

    @property
    def ptn(self) -> float:
        # P (tn)
        return self._ptn

    @property
    def pfp(self) -> float:
        # P (fp)
        return self._pfp

    @property
    def pfn(self) -> float:
        return self._pfn

    @property
    def ptp(self) -> float:
        return self._ptp

    def getMassFunction(self):
        return np.array([self._ptn, self._pfp, self._pfn, self._ptp])

    def isNoSkill(self) -> bool:
        tpr = getTpr(self._ptp, self._pfn)
        fpr = getFpr(self._pfp, self._ptn)

        return np.isclose(tpr, fpr, atol=self.tol)

    def isAboveNoSkills(self) -> bool:
        tpr = getTpr(self._ptp, self._pfn)
        fpr = getFpr(self._pfp, self._ptn)

        return (tpr - self.tol) >= fpr

    def isBelowNoSkills(self) -> bool:
        tpr = getTpr(self._ptp, self._pfn)
        fpr = getFpr(self._pfp, self._ptn)

        return (tpr + self.tol) <= fpr

    def __eq__(self, other):
        comps = np.isclose(
            [self._ptn, self._pfp, self._pfn, self._ptp],
            [other._ptn, other._pfp, other._pfn, other._ptp],
            atol=self.tol,
        )
        return np.all(comps)

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def buildFromRankingScoreValues(
        name, *pairsOfRankingScoresAndValues
    ) -> "TwoClassClassificationPerformance":
        raise NotImplementedError()

    def drawInROC(self, fig, ax) -> None:
        # TODO do we need the fig?
        tpr = getTpr(self._ptp, self._pfn)
        fpr = getFpr(self._pfp, self._ptn)

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
