# import numpy as np
import logging
import math
from typing import Self
import numpy as np
import matplotlib.pyplot as plt

from sorbetto.core.importance import Importance
from sorbetto.geometry.pencil import Pencil


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
        self._importance = importance

        if not callable(constraint):
            raise TypeError(f"constraint must be a callable, got {type(constraint)}")
        self._constraint = constraint

        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        itn = self._importance.itn
        ifp = self._importance.ifp
        ifn = self._importance.ifn
        itp = self._importance.itp
        if value is None:
            value = "Ranking Score R_I for I(tn)={:g}, I(fp)={:g}, I(fn)={:g}, I(tp)={:g}".format(
                itn, ifp, ifn, itp
            )
        elif not isinstance(value, str):
            value = str(value)
        self._name = value

    @property
    def importance(self) -> Importance:
        return self._importance

    def isCanonical(self, tol=1e-8) -> bool:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Definition 1.
        """
        itn = self._importance.itn
        ifp = self._importance.ifp
        ifn = self._importance.ifn
        itp = self._importance.itp
        canonical_for_satisfying = math.isclose(itn + itp, 1.0, abs_tol=tol)
        canonical_for_unsatisfying = math.isclose(ifp + ifn, 1.0, abs_tol=tol)
        return canonical_for_satisfying and canonical_for_unsatisfying

    def toPABDC(self) -> Self:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Example 3.
        """
        pass  # TODO: implement

    def drawInROC(self, fig, ax, priorPos: float) -> None:
        """
        See https://en.wikipedia.org/wiki/Receiver_operating_characteristic

        Args:
            fig (_type_): _description_
            ax (_type_): _description_
            priorPos (float): prior of the positive class $\pi_+ \in (0,1)$
        """

        # Configure here what we want to show:
        # TODO: create an argument for all of this instead of hardcoding it
        show_values_map = True
        show_iso_value_lines = True
        show_colorbar = True
        show_no_skills = True
        show_priors = True
        show_unbiased = True

        # Check priors
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        priorNeg = 1.0 - priorPos

        # TNR, FPR, FNR, TPR
        grid_size = 1001
        vec_fpr = vec_tpr = np.linspace(0, 1, num=grid_size)
        mat_fpr, mat_tpr = np.meshgrid(vec_fpr, vec_tpr, indexing="xy")
        mat_tnr = 1 - mat_fpr
        mat_fnr = 1 - mat_tpr

        # PTN, PFP, PFN, PTP
        mat_ptn = mat_tnr * priorNeg
        mat_pfp = mat_fpr * priorNeg
        mat_pfn = mat_fnr * priorPos
        mat_ptp = mat_tpr * priorPos

        # ITN, IFP, IFN, ITP
        itn = self._importance.itn
        ifp = self._importance.ifp
        ifn = self._importance.ifn
        itp = self._importance.itp

        # Values taken by the scores
        mat_satisfying = itn * mat_ptn + itp * mat_ptp
        mat_unsatisfying = ifp * mat_pfp + ifn * mat_pfn
        mat_values = mat_satisfying / (mat_satisfying + mat_unsatisfying)

        if show_values_map:
            extent = 0, 1, 0, 1
            cmap = plt.cm.bone
            im = ax.imshow(
                mat_values,
                extent=extent,
                origin="lower",
                interpolation="bilinear",
                cmap=cmap,
            )

        if show_iso_value_lines:
            cs = ax.contour(
                vec_fpr,
                vec_tpr,
                mat_values,
                levels=np.linspace(0, 1, 21),
                colors="cornflowerblue",
            )
            ax.clabel(cs, inline=True, fontsize=8)

        if show_values_map and show_colorbar:
            fig.colorbar(im, ax=ax, label=self.getName())

        if show_no_skills:
            ax.plot([0, 1], [0, 1], "--", c="palevioletred")
            ax.text(
                0.5,
                0.5,
                "no-skill",
                ha="center",
                va="baseline",
                rotation=45,
                c="palevioletred",
            )

        if show_priors:
            ax.plot(
                [0, priorPos, priorPos], [priorPos, priorPos, 0], ":", c="palevioletred"
            )

        if show_unbiased:
            if priorPos <= 0.5:
                ax.plot([0, priorPos / priorNeg], [1, 0], "--", c="palevioletred")
            else:
                ax.plot([0, 1], [1, 1 - priorNeg / priorPos], "--", c="palevioletred")
            x = 0.5 * priorPos
            y = 0.5 + 0.5 * priorPos
            a = math.atan2(priorNeg, -priorPos) * 180.0 / math.pi
            ax.text(
                x,
                y,
                "unbiased",
                ha="center",
                va="baseline",
                rotation=a,
                c="palevioletred",
            )

        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_xlabel("False Positive Rate (FPR)")
        ax.set_ylabel("True Positive Rate (TPR)")
        ax.set_aspect("equal")
        ax.set_title("ROC for $\pi_+={:g}".format(priorPos))

    def getPencilInROC(self, priorPos) -> Pencil:
        pass  # TODO: implement Seb

    def __call__(self, performance) -> float:
        if not self._constraint(performance):
            logging.warning(
                f"Performance {performance} does not satisfy the constraint of the ranking score {self._name}"
            )
        satisfying = (
            performance.ptn * self._importance.itn
            + performance.ptp * self._importance.itp
        )
        unsatisfying = (
            performance.pfp * self._importance.ifp
            + performance.pfn * self._importance.ifn
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
        importance = Importance(itn=1, ifp=1, ifn=0, itp=0)
        return RankingScore(importance, name="TNR")

    @staticmethod
    def getTruePositiveRate() -> (
        "RankingScore"
    ):  # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        True Positive Rate (TPR).
        Synonyms: sensitivity, recall.
        """
        importance = Importance(itn=0, ifp=0, ifn=1, itp=1)
        return RankingScore(importance, name="TPR")

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
        importance = Importance(itn=1, ifp=0, ifn=1, itp=0)
        return RankingScore(importance, name="NPV")

    @staticmethod
    def getPositivePredictiveValue() -> (
        "RankingScore"
    ):  # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        Positive Predictive Value (PPV).
        Synonym: precision
        """
        importance = Importance(itn=0, ifp=1, ifn=0, itp=1)
        return RankingScore(importance, name="PPV")

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
        importance = Importance(itn=0, ifp=1, ifn=1, itp=1)
        return RankingScore(importance, name="IoU")

    @staticmethod
    def getInverseIntersectionOverUnion() -> "RankingScore":
        importance = Importance(itn=1, ifp=1, ifn=1, itp=0)
        return RankingScore(importance, name="Inverse IoU")

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

        importance = Importance(
            itn=0, ifp=1 / (1 + beta**2), ifn=beta**2 / (1 + beta**2), itp=1
        )
        return RankingScore(importance, name=f"F{beta}")

    @staticmethod
    def getInverseF(beta=1.0) -> "RankingScore":
        if beta < 0:
            raise ValueError(f"beta must be positive, got {beta}")

        importance = Importance(
            itn=1, ifp=beta**2 / (1 + beta**2), ifn=1 / (1 + beta**2), itp=0
        )
        return RankingScore(importance, name=f"Inverse F{beta}")

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
        importance = Importance(itn=1, ifp=1, ifn=1, itp=1)
        return RankingScore(importance, name="A")

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

    def __str__(self):
        return f"Ranking Score: {self._name} with importance {str(self._importance)}"
