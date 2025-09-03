from abc import ABC, abstractmethod

import numpy as np

from sorbetto.core.importance import Importance
from sorbetto.geometry.conic import Conic
from sorbetto.geometry.point import Point
from sorbetto.ranking.ranking_score import RankingScore


class AbstractParameterization(ABC):
    """This is the base class for all possible ways of mapping ranking scores (or, equivalently, importance values, tha is some application-related preferences) onto Tiles. All ranking scores inducing the same performance ordering should be mapped to the same point. It is recommended that the subclasses implement continuous mappings between the four importance values and the two parameters. Also, it is recommended that (1) the ranking scores giving no importance at all to the true positives are mapped to points on the left border (minimal value for the first parameter), (2) the ranking scores giving no importance at all to the true negatives are mapped to points on the right border (maximal value for the first parameter), (3) the ranking scores giving no importance at all to the false positives are mapped to points on the lower border (minimal value for the second parameter), and (4) the ranking scores giving no importance at all to the false negatives are mapped to points on the upper border (minimal value for the second parameter)."""

    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def getNameParameter1(self) -> str: ...

    @abstractmethod
    def getNameParameter2(self) -> str: ...

    @abstractmethod
    def getBoundsParameter1(self) -> tuple[float, float]:
        pass

    @abstractmethod
    def getBoundsParameter2(self) -> tuple[float, float]:
        pass

    def getExtent(self) -> tuple[float, float, float, float]:
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
        """Computes a array of canonical importances values corresponding to
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
    def getValueParameter1(self, rankingScore) -> float:
        pass

    @abstractmethod
    def getValueParameter2(self, rankingScore) -> float:
        pass

    def locateRankingScore(self, rankingScore) -> Point:
        assert isinstance(rankingScore, RankingScore)
        param1 = self.getValueParameter1(rankingScore)
        param2 = self.getValueParameter2(rankingScore)
        return Point(param1, param2)

    def locateCohenCorrected(self, score: RankingScore) -> Point:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.4.
        """
        raise NotImplementedError()  # TODO

    def locateTrueNegativeRate(self) -> Point:
        return self.locateRankingScore(RankingScore.getTrueNegativeRate())

    def locateTruePositiveRate(self) -> Point:
        return self.locateRankingScore(RankingScore.getTruePositiveRate())

    def locateSpecificity(self) -> Point:
        return self.locateRankingScore(RankingScore.getSpecificity())

    def locateSelectivity(self) -> Point:
        return self.locateRankingScore(RankingScore.getSelectivity())

    def locateSensitivity(self) -> Point:
        return self.locateRankingScore(RankingScore.getSensitivity())

    def locateNegativePredictiveValue(self) -> Point:
        return self.locateRankingScore(RankingScore.getNegativePredictiveValue())

    def locatePositivePredictiveValue(self) -> Point:
        return self.locateRankingScore(RankingScore.getPositivePredictiveValue())

    def locatePrecision(self) -> Point:
        return self.locateRankingScore(RankingScore.getPrecision())

    def locateInversePrecision(self) -> Point:
        return self.locateRankingScore(RankingScore.getInversePrecision())

    def locateRecall(self) -> Point:
        return self.locateRankingScore(RankingScore.getRecall())

    def locateInverseRecall(self) -> Point:
        return self.locateRankingScore(RankingScore.getInverseRecall())

    def locateIntersectionOverUnion(self) -> Point:
        return self.locateRankingScore(RankingScore.getIntersectionOverUnion())

    def locateInverseIntersectionOverUnion(self) -> Point:
        return self.locateRankingScore(RankingScore.getInverseIntersectionOverUnion())

    def locateJaccard(self) -> Point:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        return self.locateRankingScore(RankingScore.getJaccard())

    def locateInverseJaccard(self) -> Point:
        return self.locateRankingScore(RankingScore.getInverseJaccard())

    def locateTanimotoCoefficient(self) -> Point:
        return self.locateRankingScore(RankingScore.getTanimotoCoefficient())

    def locateSimilarity(self) -> Point:
        return self.locateRankingScore(RankingScore.getSimilarity())

    def locateCriticalSuccessIndex(self) -> Point:
        return self.locateRankingScore(RankingScore.getCriticalSuccessIndex())

    def locateF(self, beta=1.0) -> Point:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        return self.locateRankingScore(RankingScore.getF(beta=beta))

    def locateInverseF(self, beta=1.0) -> Point:
        return self.locateRankingScore(RankingScore.getInverseF(beta=beta))

    def locateDiceSorensenCoefficient(self) -> Point:
        """
        Dice-Sørensen coefficient.
        Synonym: F-one $\\scoreFOne$.
        $\\scoreFOne=\\nicefrac{2\\scoreJaccardPos}{\\scoreJaccardPos+1}$
        """
        return self.locateRankingScore(RankingScore.getDiceSorensenCoefficient())

    def locateZijdenbosSimilarityIndex(self) -> Point:
        return self.locateRankingScore(RankingScore.getZijdenbosSimilarityIndex())

    def locateCzekanowskiBinaryIndex(self) -> Point:
        return self.locateRankingScore(RankingScore.getCzekanowskiBinaryIndex())

    def locateAccuracy(self) -> Point:
        return self.locateRankingScore(RankingScore.getAccuracy())

    def locateMatchingCoefficient(self) -> Point:
        return self.locateRankingScore(RankingScore.getMatchingCoefficient())

    def locateBennettS(self) -> Point:
        """
        Bennett's $S$.
        This score is related to the accuracy $A$ by $S=2A-1$.
        Reference: :cite:t:`Warrens2012TheEffect`.
        """
        raise NotImplementedError()  # TODO

    def locateSimilarityCoefficientsT(self) -> Point:
        """
        Similarity coefficients of the family $T_\\theta$, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO

    def locateSimilarityCoefficientsS(self) -> Point:
        """
        Similarity coefficients of the family $S_\\theta$, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO

    def locateSimilarityCoefficients(self) -> Conic:
        """
        Similarity coefficients, as defined in :cite:t:`Batyrshin2016Visualization`.
        See :cite:t:`Batyrshin2016Visualization` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO

    def locateStandardizedNegativePredictiveValue(self, priorPos) -> Point:
        """
        Standardized Negative Predictive Value (SNPV).
        Defined in :cite:t:`Heston2011Standardizing`.
        $\\scoreSNPV=\\frac{\\scoreTNR}{\\scoreTNR+\\scoreFNR}=\\frac{\\scoreNPV\\priorpos}{\\scoreNPV(\\priorpos-\\priorneg)+\\priorneg}$
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO

    def locateStandardizedPositivePredictiveValue(self, priorPos) -> Point:
        """
        Standardized Positive Predictive Value (SPPV).
        Defined in :cite:t:`Heston2011Standardizing`.
        $\\scoreSPPV=\\frac{\\scoreTPR}{\\scoreFPR+\\scoreTPR}=\\frac{\\scorePPV\\priorneg}{\\scorePPV(\\priorneg-\\priorpos)+\\priorpos}$
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO

    def locateNegativeLikelihoodRatioComplement(self, priorPos) -> Point:
        """
        Negative Likelihood Ratio.
        References: :cite:t:`Gardner2006Receiver-operating,Glas2003TheDiagnosticOddsRatio,Powers2020Evaluation-arxiv,Brown2006ROC`
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        # TODO add Gardner2006Receiver-operating to the bib
        raise NotImplementedError()  # TODO

    def locatePositiveLikelihoodRatio(self, priorPos) -> Point:
        """
        Positive Likelihood Ratio.
        References: :cite:t:`Gardner2006Receiver-operating,Glas2003TheDiagnosticOddsRatio,Powers2020Evaluation-arxiv,Brown2006ROC,Altman1994Diagnostic`
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO

    def locateSkewInsensitiveVersionOfF(self, priorPos) -> Point:
        """
        The skew-insensitive version of $\\scoreFOne$.
        Defined in cite:t:`Flach2003TheGeometry`.
        """
        return self.locateRankingScore(RankingScore.getSkewInsensitiveVersionOfF())

    def locateWeightedAccuracy(self, priorPos, weightPos) -> Point:
        return self.locateRankingScore(
            RankingScore.getWeightedAccuracy(priorPos, weightPos)
        )

    def locateBalancedAccuracy(self, priorPos) -> Point:
        return self.locateRankingScore(RankingScore.getBalancedAccuracy(priorPos))

    def locateYoudenJ(self, priorPos) -> Point:
        """
        Youden's index or Youden's $\\scoreYoudenJ$ statistic.
        Defined in :cite:t:`Youden1950Index`
        References: :cite:t:`Fluss2005Estimation`.
        Related to the balanced accuracy by $\\scoreYoudenJ=\\scoreTNR+\\scoreTPR-1=2\\scoreBalancedAccuracy-1$.
        Synonyms: informedness and Peirce Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO

    def locatePeirceSkillScore(self, priorPos) -> Point:
        raise NotImplementedError()  # TODO

    def locateInformedness(self, priorPos) -> Point:
        """
        See :cite:t:`Pierard2025Foundations`, Section A.7.4
        """
        raise NotImplementedError()  # TODO

    def locateCohenKappa(self, priorPos) -> Point:
        """
        Cohen's $\\scoreCohenKappa$ statistic.
        Defined in :cite:t:`Cohen1960ACoefficient`
        References: :cite:t:`Kaymak2012TheAUK`
        Synonyms: Heidke Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.3.
        """
        raise NotImplementedError()  # TODO

    def locateHeidkeSkillScore(self, priorPos) -> Point:
        raise NotImplementedError()  # TODO

    def locateProbabilityTrueNegative(self, priorPos) -> Point:
        return self.locateRankingScore(RankingScore.getProbabilityTrueNegative())

    def locateProbabilityFalsePositiveComplenent(self, priorPos) -> Point:
        return self.locateRankingScore(
            RankingScore.getProbabilityFalsePositiveComplenent()
        )

    def locateProbabilityFalseNegativeComplenent(self, priorPos) -> Point:
        return self.locateRankingScore(
            RankingScore.getProbabilityFalseNegativeComplenent()
        )

    def locateProbabilityTruePositive(self, priorPos) -> Point:
        return self.locateRankingScore(RankingScore.getProbabilityTruePositive())

    def locateDetectionRate(self, priorPos) -> Point:
        return self.locateRankingScore(RankingScore.getDetectionRate())

    def locateRejectionRate(self, priorPos) -> Point:
        return self.locateRankingScore(RankingScore.getRejectionRate())

    def locateNormalizedConfusionMatrixDeterminent(self, priorPos) -> Point:
        """
        The determinant of the normalized confusion matrix is $\\scoreConfusionMatrixDeterminant=\\priorneg\\priorpos\\scoreYoudenJ$.
        Some works using this score: :cite:t:`Wimmer2006APerson`.
        """
        raise NotImplementedError()  # TODO

    def locateMarkedness(self, ratePos) -> Point:
        """
        Markedness.
        Defined in :cite:t:`Powers2020Evaluation-arxiv` as $\\scoreNPV+\\scorePPV-1$.
        Synonyms: Clayton Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        """
        raise NotImplementedError()  # TODO

    def locateClaytonSkillScore(self, ratePos) -> Point:
        raise NotImplementedError()  # TODO

    # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 6.
    def locateOrderingsPuttingNoSkillPerformancesOnAnEqualFooting(
        self, priorPos, ratePos
    ) -> Point | Conic:
        # See Theorem 3 of future "paper 6".
        # See Theorem 4 of future "paper 6".
        # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 8
        raise NotImplementedError()  # TODO

    def locateOrderingsInveredWithOpChangePredictedClass(self) -> Conic:
        """
        $$\\left\\{ R_I : I(tp) I(fp) = I(tn) I(fn) \\right\\}
        = \\left\\{ R_I : a(I) = b(I) \\right\\}$$
        """
        # See Theorem 1 of future "paper 6".
        raise NotImplementedError()  # TODO

    def locateOrderingsInveredWithOpChangeGroundtruthClass(self) -> Conic:
        """
        $$\\left\\{ R_I : I(tp) I(fn) = I(tn) I(fp) \\right\\}
        = \\left\\{ R_I : a(I) + b(I) = 1 \\right\\}$$
        """
        # See Theorem 2 of future "paper 6".
        raise NotImplementedError()  # TODO

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
