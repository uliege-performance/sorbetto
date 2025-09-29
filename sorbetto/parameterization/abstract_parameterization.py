# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod

import numpy as np

from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D
from sorbetto.geometry.conic import Conic
from sorbetto.geometry.line import Line
from sorbetto.geometry.point import Point
from sorbetto.ranking.importance import Importance
from sorbetto.ranking.ranking_score import RankingScore


class AbstractParameterization(ABC):
    """
    This is the base class for all possible ways of mapping all (or a subset of)
    4D importances (that is some application-related preferences) onto 2D Tiles.
    This mechanism allows to map ranking scores, importance values, performance
    orderings, and rankings onto Tiles.

    All ranking scores inducing the same performance ordering should be mapped
    to the same point. It is recommended that the subclasses implement continuous
    mappings between the four importance values and the two parameters.

    Also, it is recommended that:
    (1) the ranking scores giving no importance at all to the true positives are
    mapped to points on the left border (minimal value for the first parameter);
    (2) the ranking scores giving no importance at all to the true negatives are
    mapped to points on the right border (maximal value for the first parameter);
    (3) the ranking scores giving no importance at all to the false positives are
    mapped to points on the lower border (minimal value for the second parameter);
    and (4) the ranking scores giving no importance at all to the false negatives
    are mapped to points on the upper border (minimal value for the second parameter).

    An example of parameterization is the "default" parameterization
    :math:`(x, y)=(a(I), b(I))` that has been defined in :cite:t:`Pierard2024TheTile-arxiv`.
    """

    def __init__(self):
        """
        Constructor.
        """
        ABC.__init__(self)

    @abstractmethod
    def getNameParameter1(self) -> str:
        """
        Returns the name of the first parameter (the horizontal coordinate, :math:`x`, in Tiles)

        Returns:
            str: The name of the first parameter.
        """
        ...

    @abstractmethod
    def getNameParameter2(self) -> str:
        """
        Returns the name of the second parameter (the vertical coordinate, :math:`y`, in Tiles)

        Returns:
            str: The name of the second parameter.
        """
        ...

    @abstractmethod
    def getBoundsParameter1(self) -> tuple[float, float]:
        """
        Returns the bounds for the first parameter (the horizontal coordinate, :math:`x`, in Tiles)

        Returns:
            tuple[float, float]: The bounds :math:`(\\min_x, \\max_x)` for the first parameter, with :math:`\\min_x < \\max_x`.
        """
        ...

    @abstractmethod
    def getBoundsParameter2(self) -> tuple[float, float]:
        """
        Returns the bounds for the second parameter (the vertical coordinate, :math:`y`, in Tiles)

        Returns:
            tuple[float, float]: The bounds :math:`(\\min_y, \\max_y)` for the second parameter, with :math:`\\min_y < \\max_y`.
        """
        ...

    def getExtent(self) -> tuple[float, float, float, float]:
        """
        The axis-aligned bounding box, :math:`(\\min_x, \\max_x, \\min_y, \\max_y)`,
        of Tiles with this parameterization :math:`(x, y)`. This bounding box is
        such that :math:`\\min_x < \\max_x` and :math:`\\min_y < \\max_y`.

        Returns:
            tuple[float, float, float, float]: The axis-aligned bounding box.
        """
        min_x, max_x = self.getBoundsParameter1()
        assert min_x < max_x
        min_y, max_y = self.getBoundsParameter2()
        assert min_y < max_y
        return (min_x, max_x, min_y, max_y)

    def getCanonicalImportance(self, param1: float, param2: float) -> Importance:
        """Returns the canonical importance corresponding to the given parameters.

        Default implementation calls the getCanonicalImportanceVectorized (abstract)
        method.

        Args:
            param1 (float): The first parameter.
            param2 (float): The second parameter.

        Returns:
            The canonical importance.
        """
        assert isinstance(param1, float)
        assert isinstance(param2, float)

        return Importance(
            *self.getCanonicalImportanceVectorized(
                np.array([param1]),
                np.array([param2]),
            )
        )

    @abstractmethod
    def getCanonicalImportanceVectorized(
        self, param1: np.ndarray, param2: np.ndarray
    ) -> np.ndarray:
        """Computes an array of canonical importance values corresponding to
        the given parameters.

        This needs to be implemented by subclasses.

        Args:
            param1 (np.ndarray): The first parameter array.
            param2 (np.ndarray): The second parameter array.

        Returns:
            an array of shape (N, 4) where N is the number of elements in param1 and param2.
        """
        ...

    def getCanonicalRankingScore(self, param1: float, param2: float) -> RankingScore:
        importance = self.getCanonicalImportance(param1, param2)
        return RankingScore(importance)

    @abstractmethod
    def getValueParameter1(self, rankingScore: RankingScore) -> float:
        """
        Returns the value of the first parameter (the horizontal coordinate, :math:`x`, in Tiles)
        corresponding to the given ranking score.

        Args:
            rankingScore (RankingScore): The ranking score.

        Returns:
            float: The value of the first parameter.
        """
        ...

    @abstractmethod
    def getValueParameter2(self, rankingScore) -> float:
        """
        Returns the value of the second parameter (the vertical coordinate, :math:`y`, in Tiles)
        corresponding to the given ranking score.

        Args:
            rankingScore (RankingScore): The ranking score.

        Returns:
            float: The value of the second parameter.
        """
        ...

    def locateRankingScore(self, rankingScore) -> Point:
        """
        Locates any *Ranking Score*.
        """
        assert isinstance(rankingScore, RankingScore)
        param1 = self.getValueParameter1(rankingScore)
        param2 = self.getValueParameter2(rankingScore)
        return Point(param1, param2)

    def locateCohenCorrected(self, score: RankingScore) -> Point:
        """
        Locates the performance ordering induced by the Cohen-corrected version of the provided ranking score.
        See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.4.
        """
        raise NotImplementedError()  # TODO

    def locateTrueNegativeRate(self) -> Point:
        """
        Locates the score *True Negative Rate*.
        See :meth:`sorbetto.ranking.RankingScore.getTrueNegativeRate`
        """
        score = RankingScore.getTrueNegativeRate()
        return self.locateRankingScore(score)

    def locateTruePositiveRate(self) -> Point:
        """
        Locates the score *True Positive Rate*.
        See :meth:`sorbetto.ranking.RankingScore.getTruePositiveRate`
        """
        score = RankingScore.getTruePositiveRate()
        return self.locateRankingScore(score)

    def locateSpecificity(self) -> Point:
        """
        Locates the score *Specificity*.
        See :meth:`sorbetto.ranking.RankingScore.getSpecificity`
        """
        score = RankingScore.getSpecificity()
        return self.locateRankingScore(score)

    def locateSelectivity(self) -> Point:
        """
        Locates the score *Selectivity*.
        See :meth:`sorbetto.ranking.RankingScore.getSelectivity`
        """
        score = RankingScore.getSelectivity()
        return self.locateRankingScore(score)

    def locateSensitivity(self) -> Point:
        """
        Locates the score *Sensitivity*.
        See :meth:`sorbetto.ranking.RankingScore.getSensitivity`
        """
        score = RankingScore.getSensitivity()
        return self.locateRankingScore(score)

    def locateNegativePredictiveValue(self) -> Point:
        """
        Locates the score *Negative Predictive Value*.
        See :meth:`sorbetto.ranking.RankingScore.getNegativePredictiveValue`
        """
        score = RankingScore.getNegativePredictiveValue()
        return self.locateRankingScore(score)

    def locatePositivePredictiveValue(self) -> Point:
        """
        Locates the score *Positive Predictive Value*.
        See :meth:`sorbetto.ranking.RankingScore.getPositivePredictiveValue`
        """
        score = RankingScore.getPositivePredictiveValue()
        return self.locateRankingScore(score)

    def locatePrecision(self) -> Point:
        """
        Locates the score *Precision*.
        See :meth:`sorbetto.ranking.RankingScore.getPrecision`
        """
        score = RankingScore.getPrecision()
        return self.locateRankingScore(score)

    def locateInversePrecision(self) -> Point:
        """
        Locates the score *Inverse Precision*.
        See :meth:`sorbetto.ranking.RankingScore.getInversePrecision`
        """
        score = RankingScore.getInversePrecision()
        return self.locateRankingScore(score)

    def locateRecall(self) -> Point:
        """
        Locates the score *Recall*.
        See :meth:`sorbetto.ranking.RankingScore.getRecall`
        """
        score = RankingScore.getRecall()
        return self.locateRankingScore(score)

    def locateInverseRecall(self) -> Point:
        """
        Locates the score *Inverse Recall*.
        See :meth:`sorbetto.ranking.RankingScore.getInverseRecall`
        """
        score = RankingScore.getInverseRecall()
        return self.locateRankingScore(score)

    def locateIntersectionOverUnion(self) -> Point:
        """
        Locates the score *Intersection over Union*.
        See :meth:`sorbetto.ranking.RankingScore.getIntersectionOverUnion`
        """
        score = RankingScore.getIntersectionOverUnion()
        return self.locateRankingScore(score)

    def locateInverseIntersectionOverUnion(self) -> Point:
        """
        Locates the score *Inverse Intersection over Union*.
        See :meth:`sorbetto.ranking.RankingScore.getInverseIntersectionOverUnion`
        """
        score = RankingScore.getInverseIntersectionOverUnion()
        return self.locateRankingScore(score)

    def locateJaccard(self) -> Point:
        """
        Locates the score *Jaccard*.
        See :meth:`sorbetto.ranking.RankingScore.getJaccard`
        """
        score = RankingScore.getJaccard()
        return self.locateRankingScore(score)

    def locateInverseJaccard(self) -> Point:
        """
        Locates the score *Inverse Jaccard*.
        See :meth:`sorbetto.ranking.RankingScore.getInverseJaccard`
        """
        score = RankingScore.getInverseJaccard()
        return self.locateRankingScore(score)

    def locateTanimotoCoefficient(self) -> Point:
        """
        Locates the score *Tanimoto Coefficient*.
        See :meth:`sorbetto.ranking.RankingScore.getTanimotoCoefficient`
        """
        score = RankingScore.getTanimotoCoefficient()
        return self.locateRankingScore(score)

    def locateSimilarity(self) -> Point:
        """
        Locates the score *Similarity*.
        See :meth:`sorbetto.ranking.RankingScore.getSimilarity`
        """
        score = RankingScore.getSimilarity()
        return self.locateRankingScore(score)

    def locateCriticalSuccessIndex(self) -> Point:
        """
        Locates the score *Critical Success Index*.
        See :meth:`sorbetto.ranking.RankingScore.getCriticalSuccessIndex`
        """
        score = RankingScore.getCriticalSuccessIndex()
        return self.locateRankingScore(score)

    def locateF(self, beta=1.0) -> Point:
        """
        Locates the score *F*.
        See :meth:`sorbetto.ranking.RankingScore.getF`
        """
        score = RankingScore.getF(beta=beta)
        return self.locateRankingScore(score)

    def locateInverseF(self, beta=1.0) -> Point:
        """
        Locates the score *Inverse F*.
        See :meth:`sorbetto.ranking.RankingScore.getInverseF`
        """
        score = RankingScore.getInverseF(beta=beta)
        return self.locateRankingScore(score)

    def locateDiceSorensenCoefficient(self) -> Point:
        """
        Locates the score *Dice-Sørensen Coefficient*.
        See :meth:`sorbetto.ranking.RankingScore.getDiceSorensenCoefficient`
        """
        score = RankingScore.getDiceSorensenCoefficient()
        return self.locateRankingScore(score)

    def locateZijdenbosSimilarityIndex(self) -> Point:
        """
        Locates the score *Zijdenbos Similarity Index*.
        See :meth:`sorbetto.ranking.RankingScore.getZijdenbosSimilarityIndex`
        """
        score = RankingScore.getZijdenbosSimilarityIndex()
        return self.locateRankingScore(score)

    def locateCzekanowskiBinaryIndex(self) -> Point:
        """
        Locates the score *Czekanowski Binary Index*.
        See :meth:`sorbetto.ranking.RankingScore.getCzekanowskiBinaryIndex`
        """
        score = RankingScore.getCzekanowskiBinaryIndex()
        return self.locateRankingScore(score)

    def locateAccuracy(self) -> Point:
        """
        Locates the score *Accuracy*.
        See :meth:`sorbetto.ranking.RankingScore.getAccuracy`
        """
        score = RankingScore.getAccuracy()
        return self.locateRankingScore(score)

    def locateBennettS(self) -> Point:
        """
        Locates the performance ordering induced by the score *Bennett's :math:`S`*.
        This score is related to the accuracy :math:`A` by :math:`S=2A-1`.

        Reference: :cite:t:`Warrens2012TheEffect`.
        """
        return self.locateAccuracy()

    def locateSimilarityCoefficientsT(self) -> Point:
        """
        Locates the performance ordering induced by the scores *Similarity Coefficients T*.
        Similarity coefficients of the family :math:`T_\\theta`, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateSimilarityCoefficientsS(self) -> Point:
        """
        Locates the performance ordering induced by the scores *Similarity Coefficients S*.
        Similarity coefficients of the family :math:`S_\\theta`, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateSimilarityCoefficients(self) -> Conic:
        """
        Locates the performance ordering induced by the scores *Similarity Coefficients*.
        Similarity coefficients, as defined in :cite:t:`Batyrshin2016Visualization`.
        See :cite:t:`Batyrshin2016Visualization` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateStandardizedNegativePredictiveValue(self, priorPos) -> Point:
        """
        Locates the performance ordering induced by the score *Standardized Negative Predictive Value*.
        The Standardized Negative Predictive Value (SNPV) is defined in :cite:t:`Heston2011Standardizing` as

        .. math::
            SNPV=\\frac{TNR}{TNR+FNR}=\\frac{NPV \\pi_+ }{NPV( \\pi_+ - \\pi_- )+ \\pi_- }

        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateStandardizedPositivePredictiveValue(self, priorPos) -> Point:
        """
        Locates the performance ordering induced by the score *Standardized Positive Predictive Value*.
        Standardized Positive Predictive Value (SPPV) is defined in :cite:t:`Heston2011Standardizing` as

        .. math::
            SPPV=\\frac{ TPR }{ FPR + TPR }=\\frac{ PPV  \\pi_- }{ PPV ( \\pi_- - \\pi_+ )+ \\pi_+ }

        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateNegativeLikelihoodRatioComplement(self, priorPos) -> Point:
        """
        Locates the performance ordering induced by the score *Negative Likelihood Ratio Complement*.
        Negative Likelihood Ratio.
        References: :cite:t:`Gardner2006Receiver‐operating,Glas2003TheDiagnosticOddsRatio,Powers2020Evaluation-arxiv,Brown2006ROC`
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locatePositiveLikelihoodRatio(self, priorPos) -> Point:
        """
        Locates the performance ordering induced by the score *Positive Likelihood Ratio*.
        Positive Likelihood Ratio.
        References: :cite:t:`Gardner2006Receiver-operating,Glas2003TheDiagnosticOddsRatio,Powers2020Evaluation-arxiv,Brown2006ROC,Altman1994Diagnostic`
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateSkewInsensitiveVersionOfF(self, priorPos) -> Point:
        """
        Locates the score *Skew-Insensitive Version of F1*.
        The skew-insensitive version of :math:`F_1`.
        Defined in cite:t:`Flach2003TheGeometry`.
        """
        return self.locateRankingScore(RankingScore.getSkewInsensitiveVersionOfF1())

    def locateWeightedAccuracy(self, priorPos: float, weightPos: float) -> Point:
        """
        Locates the score *Weighted Accuracy*.
        See :meth:`sorbetto.ranking.RankingScore.getWeightedAccuracy`
        """
        score = RankingScore.getWeightedAccuracy(priorPos, weightPos)
        return self.locateRankingScore(score)

    def locateMacroAveragedRecall(self, priorPos: float) -> Point:
        """
        Locates the score *(Arithmetically) Macro-Averaged Recall*.
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedRecall`
        """
        score = RankingScore.getMacroAveragedRecall(priorPos)
        return self.locateRankingScore(score)

    def locateBalancedAccuracy(self, priorPos: float) -> Point:
        """
        Locates the score *Balanced Accuracy*.
        See :meth:`sorbetto.ranking.RankingScore.getBalancedAccuracy`
        """
        score = RankingScore.getBalancedAccuracy(priorPos)
        return self.locateRankingScore(score)

    def locateYoudenJ(self, priorPos: float) -> Point:
        """
        Locates the performance ordering induced by the score *Youden*.
        Youden's index or Youden's :math:` Y_J ` statistic.
        Defined in :cite:t:`Youden1950Index`
        References: :cite:t:`Fluss2005Estimation`.
        Related to the balanced accuracy by :math:` Y_J =TNR+ TPR -1=2 BA -1`.
        Synonyms: informedness and Peirce Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locatePeirceSkillScore(self, priorPos: float) -> Point:
        """
        Locates the performance ordering induced by the score *Peirce Skill Score*.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateInformedness(self, priorPos: float) -> Point:
        """
        Locates the performance ordering induced by the score *Informedness*.
        """
        """
        See :cite:t:`Pierard2025Foundations`, Section A.7.4
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateCohenKappa(self, priorPos: float) -> Point:
        """
        Locates the performance ordering induced by the score *Cohen Kappa*.
        """
        """
        Cohen's :math:`\\scoreCohenKappa` statistic.
        Defined in :cite:t:`Cohen1960ACoefficient`
        References: :cite:t:`Kaymak2012TheAUK`
        Synonyms: Heidke Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.3.
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateHeidkeSkillScore(self, priorPos: float) -> Point:
        """
        Locates the performance ordering induced by the score "Heidke Skill Score".
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateProbabilityTrueNegative(
        self, *, priorPos: float | None = None, ratePos: float | None = None
    ) -> Point:
        """
        Locates the performance ordering induced by the score "Probability of True Negative".
        It is defined as

        .. math::
            PTN : \\mathbb{P} \\rightarrow [0,1] : P \\mapsto PTN(P) = P(\\{tn\\})

        When the class priors are fixed, and given by :math:`P(Y=c_-)=\\pi_- \\ne 0`
        and :math:`P(Y=c_+)=\\pi_+ \\ne 0`, we have :math:`PTN = TNR \\pi_-`, so the
        performance ordering induced by :math:`PTN` is the same as the one induced
        by the canonical ranking score :math:`TNR`.
        See :cite:t:`Pierard2025Foundations`, Section A.7.4.

        When the prediction rates are fixed, and given by :math:`P(\\hat{Y}=c_-)=\\tau_- \\ne 0`
        and :math:`P(\\hat{Y}=c_+)=\\tau_+ \\ne 0`, we have :math:`PTN = NPV \\tau_-`, so the
        performance ordering induced by :math:`PTN` is the same as the one induced
        by the canonical ranking score :math:`NPV`.

        Args:
            priorPos (float | None): The prior of the positive class, :math:`\\pi_+ = P(Y=c_+) \\in (0,1)`. Defaults to None.
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ \\in (0,1) `. Defaults to None.

        Returns:
            Point: the point on the Tile where the performance ordering induced
                by the score :math:`PTN` is, when the ordering is restricted to the
                performances with the specified constraint.
        """
        if priorPos is None:
            if ratePos is None:
                raise RuntimeError("You should specify either ratePos or priorPos.")
            else:
                assert isinstance(ratePos, float)
                assert ratePos > 0.0  # not >=, see doc here-above
                assert ratePos < 1.0  # not <=, see doc here-above
                return self.locateNegativePredictiveValue()
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                return self.locateTrueNegativeRate()
            else:
                raise RuntimeError("You should not specify both ratePos and priorPos.")

    def locateRejectionRate(
        self, *, priorPos: float | None = None, ratePos: float | None = None
    ) -> Point:
        """
        Locates the performance ordering induced by the score "Rejection Rate".
        See :meth:`locateProbabilityTrueNegative`.
        """
        return self.locateProbabilityTrueNegative(priorPos=priorPos, ratePos=ratePos)

    def locateProbabilityFalsePositiveComplement(
        self, *, priorPos: float | None = None, ratePos: float | None = None
    ) -> Point:
        """
        Locates the performance ordering induced by the score "Complement of the Probability of False Positive".
        It is defined as

        .. math::
            (1-PFP)(P) = P(\\{tn,fn,tp\\}

        When the class priors are fixed, and given by :math:`P(Y=c_-)=\\pi_- \\ne 0`
        and :math:`P(Y=c_+)=\\pi_+ \\ne 0`, we have :math:`(1-PFP) = \\pi_+ + TNR \\pi_-`, so the
        performance ordering induced by :math:`(1-PFP)` is the same as the one induced
        by the canonical ranking score :math:`TNR`.

        When the prediction rates are fixed, and given by :math:`P(\\hat{Y}=c_-)=\\tau_- \\ne 0`
        and :math:`P(\\hat{Y}=c_+)=\\tau_+ \\ne 0`, we have :math:`(1-PFP) = \\tau_- + PPV \\tau_+`, so the
        performance ordering induced by :math:`(1-PFP)` is the same as the one induced
        by the canonical ranking score :math:`PPV`.

        Args:
            priorPos (float | None): The prior of the positive class, :math:`\\pi_+ = P(Y=c_+) \\in (0,1)`. Defaults to None.
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ \\in (0,1)`. Defaults to None.

        Returns:
            Point: the point on the Tile where the performance ordering induced
                by the score :math:`(1-PFP)` is, when the ordering is restricted to the
                performances with the specified constraint.
        """
        if priorPos is None:
            if ratePos is None:
                raise RuntimeError("You should specify either ratePos or priorPos.")
            else:
                assert isinstance(ratePos, float)
                assert ratePos > 0.0  # not >=, see doc here-above
                assert ratePos < 1.0  # not <=, see doc here-above
                return self.locatePositivePredictiveValue()
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                return self.locateTrueNegativeRate()
            else:
                raise RuntimeError("You should not specify both ratePos and priorPos.")

    def locateProbabilityFalseNegativeComplement(
        self, *, priorPos: float | None = None, ratePos: float | None = None
    ) -> Point:
        """
        Locates the performance ordering induced by the score "Complement of the Probability of False Negative".
        It is defined as

        .. math::
            (1-PFN)(P) = P(\\{tn,fp,tp\\}

        When the class priors are fixed, and given by :math:`P(Y=c_-)=\\pi_- \\ne 0`
        and :math:`P(Y=c_+)=\\pi_+ \\ne 0`, we have :math:`(1-PFN) = \\pi_- + TPR \\pi_+`, so the
        performance ordering induced by :math:`(1-PFN)` is the same as the one induced
        by the canonical ranking score :math:`TPR`.

        When the prediction rates are fixed, and given by :math:`P(\\hat{Y}=c_-)=\\tau_- \\ne 0`
        and :math:`P(\\hat{Y}=c_+)=\\tau_+ \\ne 0`, we have :math:`(1-PFN) = \\tau_+ + NPV \\tau_-`, so the
        performance ordering induced by :math:`(1-PFN)` is the same as the one induced
        by the canonical ranking score :math:`NPV`.

        Args:
            priorPos (float | None): The prior of the positive class, :math:`\\pi_+ = P(Y=c_+) \\in (0,1)`. Defaults to None.
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ \\in (0,1)`. Defaults to None.

        Returns:
            Point: the point on the Tile where the performance ordering induced
                by the score :math:`(1-PFN)` is, when the ordering is restricted to the
                performances with the specified constraint.
        """
        if priorPos is None:
            if ratePos is None:
                raise RuntimeError("You should specify either ratePos or priorPos.")
            else:
                assert isinstance(ratePos, float)
                assert ratePos > 0.0  # not >=, see doc here-above
                assert ratePos < 1.0  # not <=, see doc here-above
                return self.locateNegativePredictiveValue()
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                return self.locateTruePositiveRate()
            else:
                raise RuntimeError("You should not specify both ratePos and priorPos.")

    def locateProbabilityTruePositive(
        self, *, priorPos: float | None = None, ratePos: float | None = None
    ) -> Point:
        """
        Locates the performance ordering induced by the score "Probability of True Positive".
        It is defined as

        .. math::
            PTP : \\mathbb{P} \\rightarrow [0,1] : P \\mapsto PTP(P) = P(\\{tp\\})

        When the class priors are fixed, and given by :math:`P(Y=c_-)=\\pi_- \\ne 0`
        and :math:`P(Y=c_+)=\\pi_+ \\ne 0`, we have :math:`PTP = TPR \\pi_+`, so the
        performance ordering induced by :math:`PTP` is the same as the one induced
        by the canonical ranking score :math:`TPR`.
        See :cite:t:`Pierard2025Foundations`, Section A.7.4.

        When the prediction rates are fixed, and given by :math:`P(\\hat{Y}=c_-)=\\tau_- \\ne 0`
        and :math:`P(\\hat{Y}=c_+)=\\tau_+ \\ne 0`, we have :math:`PTP = PPV \\tau_+`, so the
        performance ordering induced by :math:`PTP` is the same as the one induced
        by the canonical ranking score :math:`PPV`.

        Args:
            priorPos (float | None): The prior of the positive class, :math:`\\pi_+ = P(Y=c_+) \\in (0,1)`. Defaults to None.
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ \\in (0,1) `. Defaults to None.

        Returns:
            Point: the point on the Tile where the performance ordering induced
                by the score :math:`PTP` is, when the ordering is restricted to the
                performances with the specified constraint.
        """
        if priorPos is None:
            if ratePos is None:
                raise RuntimeError("You should specify either ratePos or priorPos.")
            else:
                assert isinstance(ratePos, float)
                assert ratePos > 0.0  # not >=, see doc here-above
                assert ratePos < 1.0  # not <=, see doc here-above
                return self.locatePositivePredictiveValue()
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                return self.locateTruePositiveRate()
            else:
                raise RuntimeError("You should not specify both ratePos and priorPos.")

    def locateDetectionRate(
        self, *, priorPos: float | None = None, ratePos: float | None = None
    ) -> Point:
        """
        Locates the performance ordering induced by the score "Detection Rate".
        See :meth:`locateProbabilityTruePositive`.
        """
        return self.locateProbabilityTruePositive(priorPos=priorPos, ratePos=ratePos)

    def locateNormalizedConfusionMatrixDeterminant(self, priorPos: float) -> Point:
        """
        Locates the performance ordering induced by the determinant of the normalized
        confusion matrix is :math:`|\\mathcal{C}|= \\pi_-  \\pi_+  Y_J `.
        Some works using this score: :cite:t:`Wimmer2006APerson`.

        See https://en.wikipedia.org/wiki/Confusion_matrix
        See https://en.wikipedia.org/wiki/Determinant
        """
        raise NotImplementedError()  # TODO: Implement this!

    def locateMacroAveragedPrecision(self, ratePos: float) -> Point:
        """
        Locates the score *(Arithmetically) Macro-Averaged Precision*.
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedPrecision`
        """
        return self.locateRankingScore(RankingScore.getMacroAveragedPrecision(ratePos))

    def locateMarkedness(self, ratePos: float) -> Point:
        """
        Locates the performance ordering induced by the score "Markedness".
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedPrecision`
        Defined in :cite:t:`Powers2020Evaluation-arxiv` as :math:`NPV+ PPV -1`.
        Synonyms: Clayton Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        """
        return self.locateRankingScore(RankingScore.getMacroAveragedPrecision(ratePos))

    def locateClaytonSkillScore(self, ratePos: float) -> Point:
        """
        Locates the performance ordering induced by the score "Clayton Skill Score".
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedPrecision`
        """
        return self.locateRankingScore(RankingScore.getMacroAveragedPrecision(ratePos))

    @abstractmethod
    def locateOrderingsPuttingNoSkillPerformancesOnAnEqualFootingForFixedClassPriors(
        self, priorPos: float
    ) -> AbstractGeometricObject2D:
        """
        Locates the set of performance orderings induced by ranking scores that put all no-skill
        performances, for given class priors :math:`(\\pi_-, \\pi_+)`, on an equal footing is given by

        .. math::
            \\left\\{ \\pi_+^2 I(tp) I(fn) = \\pi_-^2 I(tn) I(fp) \\right\\}


        See :cite:t:`Pierard2024TheTile-arxiv`, Figure 6, left.
        # See Theorem 3 of :cite:t:`Pierard2025TheManifold`.
        # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 8.

        Args:
            priorPos (float): the prior of the positive class, :math:`\\pi_+`

        Returns:
            AbstractGeometricObject2D: The locus (a curve).
        """
        ...

    @abstractmethod
    def locateOrderingsPuttingNoSkillPerformancesOnAnEqualFootingForFixedPredictionRates(
        self, ratePos: float
    ) -> AbstractGeometricObject2D:
        """
        Locates the set of performance orderings induced by ranking scores that put all no-skill
        performances, for given prediction rates :math:`(\\tau_-, \\tau_+)`, on an equal footing is given by

        .. math::
            \\left\\{ \\tau_+^2 I(tp) I(fp) = \\tau_-^2 I(tn) I(fn) \\right\\}

        See :cite:t:`Pierard2024TheTile-arxiv`, Figure 6, right.
        # See Theorem 4 of :cite:t:`Pierard2025TheManifold`.

        Args:
            ratePos (float): the prediction rate for the positive class, :math:`\\tau_+`

        Returns:
            AbstractGeometricObject2D: The locus (a curve).
        """
        ...

    @abstractmethod
    def locateOrderingsInvertedWithOpChangePredictedClass(self) -> Conic:
        """
        Locates the set of performance orderings induced by ranking scores
        that are inverted when the operation that consists in changing the
        predicted class is applied to all performances.
        :math:`\\hat{Y}=c_-` becomes :math:`\\hat{Y}=c_+` and vice-versa.
        A performance :math:`P` becomes a performance :math:`P'` such that:

        - :math:`P'(\\{tn\\}) = P(\\{fp\\})`
        - :math:`P'(\\{fp\\}) = P(\\{tn\\})`
        - :math:`P'(\\{fn\\}) = P(\\{tp\\})`
        - :math:`P'(\\{tp\\}) = P(\\{fn\\})`

        As demonstrated in Theorem 1 of :cite:t:`Pierard2025TheManifold`,
        the set is

        .. math::
            \\left\\{ I: I(tp) I(fp) = I(tn) I(fn) \\right\\}
        """
        ...

    @abstractmethod
    def locateOrderingsInvertedWithOpChangeGroundtruthClass(self) -> Conic:
        """
        Locates the set of performance orderings induced by ranking scores
        that are inverted when the operation that consists in changing the
        groundtruth class is applied to all performances.
        :math:`Y=c_-` becomes :math:`Y=c_+` and vice-versa.
        A performance :math:`P` becomes a performance :math:`P'` such that:

        - :math:`P'(\\{tn\\}) = P(\\{fn\\})`
        - :math:`P'(\\{fp\\}) = P(\\{tp\\})`
        - :math:`P'(\\{fn\\}) = P(\\{tn\\})`
        - :math:`P'(\\{tp\\}) = P(\\{fp\\})`

        As demonstrated in Theorem 2 of :cite:t:`Pierard2025TheManifold`,
        the set is

        .. math::
            \\left\\{ I: I(tp) I(fn) = I(tn) I(fp) \\right\\}
        """
        ...

    @abstractmethod
    def locateRelativeImportanceSatisfying(self, itn: float, itp: float) -> Line:
        """
        Locates the set of performance orderings induced by the ranking scores
        corresponding to some given values of importance for the satisfying samples
        (the elements :math:`\\omega` of the sample space :math:`\\Omega` such that
        :math:`S(\\omega)=1` are :math:`S^{-1}(1)=\\{tn, tp\\}`). The importance
        values :math:`I(tn)` and :math:`I(tp)` are provided up to a positive
        scale factor. This is related to the first parameter (the horizontal
        coordinate, :math:`x`, in Tiles).

        Args:
            itn (float): The (relative) importance given to the true negatives, :math:`I(tn) \\ge 0`
            itp (float): The (relative) importance given to the true positives, :math:`I(tp) \\ge 0`

        Returns:
            AbstractGeometricObject2D: The locus on the Tile.
        """
        ...

    @abstractmethod
    def locateRelativeImportanceUnsatisfying(self, ifp: float, ifn: float) -> Line:
        """
        Locates the set of performance orderings induced by the ranking scores
        corresponding to some given values of importance for the unsatisfying samples
        (the elements :math:`\\omega` of the sample space :math:`\\Omega` such that
        :math:`S(\\omega)=0` are :math:`S^{-1}(0)=\\{fp, fn\\}`). The importance
        values :math:`I(fp)` and :math:`I(fn)` are provided up to a positive
        scale factor. This is related to the second parameter (the vertical
        coordinate, :math:`y`, in Tiles).

        Args:
            ifp (float): The (relative) importance given to the true negatives, :math:`I(fp) \\ge 0`
            ifn (float): The (relative) importance given to the true positives, :math:`I(fn) \\ge 0`

        Returns:
            AbstractGeometricObject2D: The locus on the Tile.
        """
        ...

    @abstractmethod
    def getName(self):
        # TODO make it a property?
        pass

    def __str__(self):
        return 'parameterization "{}"'.format(self.getName())

    def unitTest(self):
        import math
        import random

        # TODO move this to a proper test suite

        for trial in range(1000):
            param1 = random.random()
            param2 = random.random()
            rankingScore = self.getCanonicalRankingScore(param1, param2)
            assert isinstance(rankingScore, RankingScore)
            importance = rankingScore.importance
            itn = importance.itn
            ifp = importance.ifp
            ifn = importance.ifn
            itp = importance.itp
            assert itn >= 0
            assert ifp >= 0
            assert ifn >= 0
            assert itp >= 0
            assert math.isclose(itn + itp, 1)
            assert math.isclose(ifp + ifn, 1)
            assert math.isclose(param1, self.getValueParameter1(rankingScore))
            assert math.isclose(param2, self.getValueParameter2(rankingScore))
