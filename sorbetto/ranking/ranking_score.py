# import numpy as np
import math
import logging
from typing import Self
from ..core.importance import Importance
from ..performance.two_class_classification import TwoClassClassificationPerformance


class RankingScore:
    def __init__(
        self, importance: Importance, constraint=None, name: str | None = None
    ):
        """
        Args:
            importance (Importance): _description_
            constraint (_type_, optional): _description_. Defaults to None.
            name (str | None, optional): _description_. Defaults to None.

        Raises:
            TypeError: _description_
        """
        if not isinstance(importance, Importance):
            raise TypeError(
                f"importance must be an instance of Importance, got {type(importance)}"
            )
        self.importance = importance

        if not callable(constraint):
            raise TypeError(f"constraint must be a callable, got {type(constraint)}")
        self.constraint = constraint

        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        itn = self.importance.itn
        ifp = self.importance.ifp
        ifn = self.importance.ifn
        itp = self.importance.itp
        if name is None:
            name = "R_I for I(tn)={:g}, I(fp)={:g}, I(fn)={:g}, I(tp)={:g}".format(
                itn, ifp, ifn, itp
            )
        elif not isinstance(name, str):
            name = str(name)
        self._name = name

    def getImportance(self) -> Importance:
        return self.importance

    def isCanonical(self, tol=1e-8) -> bool:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Definition 1.
        """
        itn = self.importance.itn
        ifp = self.importance.ifp
        ifn = self.importance.ifn
        itp = self.importance.itp
        return math.isclose(itn + itp, 1.0, abs_tol=tol) and math.isclose(
            ifp + ifn, 1.0, abs_tol=tol
        )

    def toPABDC(self) -> Self:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Example 3.
        """
        pass  # TODO: implement

    def drawInROC(self, fig, ax, priorPos):
        pass  # TODO: implement Seb

    def getPencilInROC(self, priorPos):  # -> Pencil: # TODO: implement Pencil class
        pass  # TODO: implement Seb

    def __call__(self, performance) -> float:
        if not self.constraint(performance):
            logging.warning(
                f"Performance {performance} does not satisfy the constraint of the ranking score {self.name}"
            )
        satisfying = (
            performance.ptn * self.importance.itn
            + performance.ptp * self.importance.itp
        )
        unsatisfying = (
            performance.pfp * self.importance.ifp
            + performance.pfn * self.importance.ifn
        )
        return satisfying / (satisfying + unsatisfying)

    @staticmethod
    def getTrueNegativeRate() -> (
        "RankingScore"
    ):  # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        True Negative Rate (TNR).
        Synonyms: specificity, selectivity, inverse recall.
        """
        I = Importance(itn=1, ifp=1, ifn=0, itp=0)
        return RankingScore(I, name="TNR")

    @staticmethod
    def getTruePositiveRate() -> (
        "RankingScore"
    ):  # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        True Positive Rate (TPR).
        Synonyms: sensitivity, recall.
        """
        I = Importance(itn=0, ifp=0, ifn=1, itp=1)
        return RankingScore(I, name="TPR")

    @staticmethod
    def getSpecificity() -> "RankingScore":
        rs = RankingScore.getTrueNegativeRate()
        rs.name = "Specificity"
        return rs

    @staticmethod
    def getSelectivity() -> "RankingScore":
        rs = RankingScore.getTrueNegativeRate()
        rs.name = "Selectivity"
        return rs

    @staticmethod
    def getSensitivity() -> "RankingScore":
        rs = RankingScore.getTruePositiveRate()
        rs.name = "Sensitivity"
        return rs

    @staticmethod
    def getNegativePredictiveValue() -> (
        "RankingScore"
    ):  # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        Negative Predictive Value (NPV).
        Synonym: inverse precision
        """
        I = Importance(itn=1, ifp=0, ifn=1, itp=0)
        return RankingScore(I, name="NPV")

    @staticmethod
    def getPositivePredictiveValue() -> (
        "RankingScore"
    ):  # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        Positive Predictive Value (PPV).
        Synonym: precision
        """
        I = Importance(itn=0, ifp=1, ifn=0, itp=1)
        return RankingScore(I, name="PPV")

    @staticmethod
    def getPrecision() -> "RankingScore":
        rs = RankingScore.getPositivePredictiveValue()
        rs.name = "Precision"
        return rs

    @staticmethod
    def getInversePrecision() -> "RankingScore":
        rs = RankingScore.getNegativePredictiveValue()
        rs.name = "Inverse Precision"
        return rs

    @staticmethod
    def getRecall() -> "RankingScore":
        rs = RankingScore.getTruePositiveRate()
        rs.name = "Recall"
        return rs

    @staticmethod
    def getInverseRecall() -> "RankingScore":
        rs = RankingScore.getTrueNegativeRate()
        rs.name = "Inverse Recall"
        return rs

    @staticmethod
    def getIntersectionOverUnion() -> "RankingScore":
        """
        Intersection over Union (IoU).
        Synonyms: Jaccard index, Jaccard similarity coefficient, Tanimoto coefficient, similarity, critical success index (CSI), threat score.
        """
        I = Importance(itn=0, ifp=1, ifn=1, itp=1)
        return RankingScore(I, name="IoU")

    @staticmethod
    def getInverseIntersectionOverUnion() -> "RankingScore":
        I = Importance(itn=1, ifp=1, ifn=1, itp=0)
        return RankingScore(I, name="Inverse IoU")

    @staticmethod
    def getJaccard() -> "RankingScore":
        rs = RankingScore.getIntersectionOverUnion()
        rs.name = "J"
        return rs

    @staticmethod
    def getInverseJaccard() -> "RankingScore":
        rs = RankingScore.getInverseIntersectionOverUnion()
        rs.name = "Inverse J"
        return rs

    @staticmethod
    def getTanimotoCoefficient() -> "RankingScore":
        rs = RankingScore.getIntersectionOverUnion()
        rs.name = "Tanimoto Coefficient"
        return rs

    @staticmethod
    def getSimilarity() -> "RankingScore":
        rs = RankingScore.getIntersectionOverUnion()
        rs.name = "Similarity"
        return rs

    @staticmethod
    def getCriticalSuccessIndex() -> "RankingScore":
        rs = RankingScore.getIntersectionOverUnion()
        rs.name = "CSI"
        return rs

    @staticmethod
    def getF(
        beta=1.0,
    ) -> "RankingScore":  # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        if beta < 0:
            raise ValueError(f"beta must be positive, got {beta}")

        I = Importance(itn=0, ifp=1 / (1 + beta**2), ifn=beta**2 / (1 + beta**2), itp=1)
        return RankingScore(I, name=f"F{beta}")

    @staticmethod
    def getInverseF(beta=1.0) -> "RankingScore":
        if beta < 0:
            raise ValueError(f"beta must be positive, got {beta}")

        I = Importance(itn=1, ifp=beta**2 / (1 + beta**2), ifn=1 / (1 + beta**2), itp=0)
        return RankingScore(I, name=f"Inverse F{beta}")

    @staticmethod
    def getDiceSorensenCoefficient() -> "RankingScore":
        rs = RankingScore.getF(beta=1.0)
        rs.name = "DSC"
        return rs

    @staticmethod
    def getZijdenbosSimilarityIndex() -> "RankingScore":
        rs = RankingScore.getF(beta=1.0)
        rs.name = "ZSI"
        return rs

    @staticmethod
    def getCzekanowskiBinaryIndex() -> "RankingScore":
        rs = RankingScore.getF(beta=1.0)
        rs.name = "CBI"
        return rs

    @staticmethod
    def getAccuracy() -> (
        "RankingScore"
    ):  # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        I = Importance(itn=1, ifp=1, ifn=1, itp=1)
        return RankingScore(I, name="A")

    @staticmethod
    def getMatchingCoefficient() -> (
        "RankingScore"
    ):  # SimpleMatchingCoefficient ??? Same as Jaccard ???
        rs = RankingScore.getAccuracy()
        rs.name = "MC"
        return rs

    @staticmethod
    def getSkewInsensitiveVersionOfF(
        priorPos,
    ) -> "RankingScore":  # TODO: implement constraint
        """
        The skew-insensitive version of $\scoreFOne$.
        Defined in cite:t:`Flach2003TheGeometry`.
        """
        pass

    @staticmethod
    def getWeightedAccuracy(
        priorPos, weightPos
    ) -> "RankingScore":  # TODO: implement constraint.
        pass  # See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.4.

    @staticmethod
    def getBalancedAccuracy(priorPos) -> "RankingScore":  # TODO: implement constraint
        pass  # See :cite:t:`Pierard2025Foundations`, Section A.7.4

    @staticmethod
    def getProbabilityTrueNegative(
        priorPos,
    ) -> "RankingScore":  # TODO: implement constraint
        pass  # See :cite:t:`Pierard2025Foundations`, Section A.7.4

    @staticmethod
    def getProbabilityFalsePositiveComplenent(
        priorPos,
    ) -> "RankingScore":  # TODO: implement constraint
        pass

    @staticmethod
    def getProbabilityFalseNegativeComplenent(
        priorPos,
    ) -> "RankingScore":  # TODO: implement constraint
        pass

    @staticmethod
    def getProbabilityTruePositive(
        priorPos,
    ) -> "RankingScore":  # TODO: implement constraint
        pass  # See :cite:t:`Pierard2025Foundations`, Section A.7.4

    @staticmethod
    def getDetectionRate(priorPos) -> "RankingScore":  # TODO: implement constraint
        pass

    @staticmethod
    def getRejectionRate(priorPos) -> "RankingScore":  # TODO: implement constraint
        pass

    def getName(self):
        return self.name

    def __str__(self):
        return f"Ranking Score: {self.name} with importance {str(self.importance)}"
