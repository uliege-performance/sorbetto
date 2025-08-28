from abc import ABC, abstractmethod

from sorbetto.geometry.curve_in_tile import CurveInTile
from sorbetto.geometry.point_in_tile import PointInTile
from sorbetto.ranking.ranking_score import RankingScore


class AbstractParameterization(ABC):
    """This is the base class for all possible ways of mapping ranking scores (or, equivalently, importance values, tha is some application-related preferences) onto Tiles. All ranking scores inducing the same performance ordering should be mapped to the same point. It is recommended that the subclasses implement continuous mappings between the four importance values and the two parameters. Also, it is recommended that (1) the ranking scores giving no importance at all to the true positives are mapped to points on the left border (minimal value for the first parameter), (2) the ranking scores giving no importance at all to the true negatives are mapped to points on the right border (maximal value for the first parameter), (3) the ranking scores giving no importance at all to the false positives are mapped to points on the lower border (minimal value for the second parameter), and (4) the ranking scores giving no importance at all to the false negatives are mapped to points on the upper border (minimal value for the second parameter)."""

    def __init__(self):
        pass

    @abstractmethod
    def getNameParameter1(self):
        pass

    @abstractmethod
    def getNameParameter2(self):
        pass

    @abstractmethod
    def getBoundsParameter1(self) -> tuple[float, float]:
        pass

    @abstractmethod
    def getBoundsParameter2(self) -> tuple[float, float]:
        pass

    @abstractmethod
    def getCanonicalRankingScore(self, param1, param2) -> RankingScore:
        pass

    @abstractmethod
    def getValueParameter1(self, rankingScore) -> float:
        pass

    @abstractmethod
    def getValueParameter2(self, rankingScore) -> float:
        pass

    def locateRankingScore(self, rankingScore) -> PointInTile:
        assert isinstance(rankingScore, RankingScore)
        param1 = self.getValueParameter1(rankingScore)
        param2 = self.getValueParameter2(rankingScore)
        return PointInTile(self, param1, param2)

    def locateCohenCorrected(self, score: RankingScore) -> PointInTile:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.4.
        """
        raise NotImplementedError()  # TODO

    def locateTrueNegativeRate(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getTrueNegativeRate())

    def locateTruePositiveRate(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getTruePositiveRate())

    def locateSpecificity(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getSpecificity())

    def locateSelectivity(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getSelectivity())

    def locateSensitivity(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getSensitivity())

    def locateNegativePredictiveValue(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getNegativePredictiveValue())

    def locatePositivePredictiveValue(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getPositivePredictiveValue())

    def locatePrecision(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getPrecision())

    def locateInversePrecision(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getInversePrecision())

    def locateRecall(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getRecall())

    def locateInverseRecall(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getInverseRecall())

    def locateIntersectionOverUnion(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getIntersectionOverUnion())

    def locateInverseIntersectionOverUnion(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getInverseIntersectionOverUnion())

    def locateJaccard(self) -> PointInTile:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        return self.locateRankingScore(RankingScore.getJaccard())

    def locateInverseJaccard(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getInverseJaccard())

    def locateTanimotoCoefficient(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getTanimotoCoefficient())

    def locateSimilarity(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getSimilarity())

    def locateCriticalSuccessIndex(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getCriticalSuccessIndex())

    def locateF(self, beta=1.0) -> PointInTile:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        return self.locateRankingScore(RankingScore.getF(beta=beta))

    def locateInverseF(self, beta=1.0) -> PointInTile:
        return self.locateRankingScore(RankingScore.getInverseF(beta=beta))

    def locateDiceSorensenCoefficient(self) -> PointInTile:
        """
        Dice-Sørensen coefficient.
        Synonym: F-one $\scoreFOne$.
        $\scoreFOne=\nicefrac{2\scoreJaccardPos}{\scoreJaccardPos+1}$
        """
        return self.locateRankingScore(RankingScore.getDiceSorensenCoefficient())

    def locateZijdenbosSimilarityIndex(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getZijdenbosSimilarityIndex())

    def locateCzekanowskiBinaryIndex(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getCzekanowskiBinaryIndex())

    def locateAccuracy(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getAccuracy())

    def locateMatchingCoefficient(self) -> PointInTile:
        return self.locateRankingScore(RankingScore.getMatchingCoefficient())

    def locateBennettS(self) -> PointInTile:
        """
        Bennett's $S$.
        This score is related to the accuracy $A$ by $S=2A-1$.
        Reference: :cite:t:`Warrens2012TheEffect`.
        """
        raise NotImplementedError()  # TODO

    def locateSimilarityCoefficientsT(self) -> PointInTile:
        """
        Similarity coefficients of the family $T_\theta$, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO

    def locateSimilarityCoefficientsS(self) -> PointInTile:
        """
        Similarity coefficients of the family $S_\theta$, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO

    def locateSimilarityCoefficients(self) -> CurveInTile:
        """
        Similarity coefficients, as defined in :cite:t:`Batyrshin2016Visualization`.
        See :cite:t:`Batyrshin2016Visualization` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO

    def locateStandardizedNegativePredictiveValue(self, priorPos) -> PointInTile:
        """
        Standardized Negative Predictive Value (SNPV).
        Defined in :cite:t:`Heston2011Standardizing`.
        $\scoreSNPV=\frac{\scoreTNR}{\scoreTNR+\scoreFNR}=\frac{\scoreNPV\priorpos}{\scoreNPV(\priorpos-\priorneg)+\priorneg}$
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO

    def locateStandardizedPositivePredictiveValue(self, priorPos) -> PointInTile:
        """
        Standardized Positive Predictive Value (SPPV).
        Defined in :cite:t:`Heston2011Standardizing`.
        $\scoreSPPV=\frac{\scoreTPR}{\scoreFPR+\scoreTPR}=\frac{\scorePPV\priorneg}{\scorePPV(\priorneg-\priorpos)+\priorpos}$
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO

    def locateNegativeLikelihoodRatioComplement(self, priorPos) -> PointInTile:
        """
        Negative Likelihood Ratio.
        References: :cite:t:`Gardner2006Receiver‐operating,Glas2003TheDiagnosticOddsRatio,Powers2020Evaluation-arxiv,Brown2006ROC`
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO

    def locatePositiveLikelihoodRatio(self, priorPos) -> PointInTile:
        """
        Positive Likelihood Ratio.
        References: :cite:t:`Gardner2006Receiver‐operating,Glas2003TheDiagnosticOddsRatio,Powers2020Evaluation-arxiv,Brown2006ROC,Altman1994Diagnostic`
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO

    def locateSkewInsensitiveVersionOfF(self, priorPos) -> PointInTile:
        """
        The skew-insensitive version of $\scoreFOne$.
        Defined in cite:t:`Flach2003TheGeometry`.
        """
        return self.locateRankingScore(RankingScore.getSkewInsensitiveVersionOfF())

    def locateWeightedAccuracy(self, priorPos, weightPos) -> PointInTile:
        return self.locateRankingScore(
            RankingScore.getWeightedAccuracy(priorPos, weightPos)
        )

    def locateBalancedAccuracy(self, priorPos) -> PointInTile:
        return self.locateRankingScore(RankingScore.getBalancedAccuracy(priorPos))

    def locateYoudenJ(self, priorPos) -> PointInTile:
        """
        Youden's index or Youden's $\scoreYoudenJ$ statistic.
        Defined in :cite:t:`Youden1950Index`
        References: :cite:t:`Fluss2005Estimation`.
        Related to the balanced accuracy by $\scoreYoudenJ=\scoreTNR+\scoreTPR-1=2\scoreBalancedAccuracy-1$.
        Synonyms: informedness and Peirce Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO

    def locatePeirceSkillScore(self, priorPos) -> PointInTile:
        raise NotImplementedError()  # TODO

    def locateInformedness(self, priorPos) -> PointInTile:
        """
        See :cite:t:`Pierard2025Foundations`, Section A.7.4
        """
        raise NotImplementedError()  # TODO

    def locateCohenKappa(self, priorPos) -> PointInTile:
        """
        Cohen's $\scoreCohenKappa$ statistic.
        Defined in :cite:t:`Cohen1960ACoefficient`
        References: :cite:t:`Kaymak2012TheAUK`
        Synonyms: Heidke Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.3.
        """
        raise NotImplementedError()  # TODO

    def locateHeidkeSkillScore(self, priorPos) -> PointInTile:
        raise NotImplementedError()  # TODO

    def locateProbabilityTrueNegative(self, priorPos) -> PointInTile:
        return self.locateRankingScore(RankingScore.getProbabilityTrueNegative())

    def locateProbabilityFalsePositiveComplenent(self, priorPos) -> PointInTile:
        return self.locateRankingScore(
            RankingScore.getProbabilityFalsePositiveComplenent()
        )

    def locateProbabilityFalseNegativeComplenent(self, priorPos) -> PointInTile:
        return self.locateRankingScore(
            RankingScore.getProbabilityFalseNegativeComplenent()
        )

    def locateProbabilityTruePositive(self, priorPos) -> PointInTile:
        return self.locateRankingScore(RankingScore.getProbabilityTruePositive())

    def locateDetectionRate(self, priorPos) -> PointInTile:
        return self.locateRankingScore(RankingScore.getDetectionRate())

    def locateRejectionRate(self, priorPos) -> PointInTile:
        return self.locateRankingScore(RankingScore.getRejectionRate())

    def locateNormalizedConfusionMatrixDeterminent(self, priorPos) -> PointInTile:
        """
        The determinant of the normalized confusion matrix is $\scoreConfusionMatrixDeterminant=\priorneg\priorpos\scoreYoudenJ$.
        Some works using this score: :cite:t:`Wimmer2006APerson`.
        """
        raise NotImplementedError()  # TODO

    def locateMarkedness(self, ratePos) -> PointInTile:
        """
        Markedness.
        Defined in :cite:t:`Powers2020Evaluation-arxiv` as $\scoreNPV+\scorePPV-1$.
        Synonyms: Clayton Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        """
        raise NotImplementedError()  # TODO

    def locateClaytonSkillScore(self, ratePos) -> PointInTile:
        raise NotImplementedError()  # TODO

    # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 6.
    def locateOrderingsPuttingNoSkillPerformancesOnAnEqualFooting(
        self, priorPos, ratePos
    ) -> PointInTile | CurveInTile:
        # See Theorem 3 of future "paper 6".
        # See Theorem 4 of future "paper 6".
        # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 8
        raise NotImplementedError()  # TODO

    def locateOrderingsInveredWithOpChangePredictedClass(self) -> CurveInTile:
        """
        $$\left{ R_I : I(tp) I(fp) = I(tn) I(fn) \right}
        = \left{ R_I : a(I) = b(I) \right}$$
        """
        # See Theorem 1 of future "paper 6".
        raise NotImplementedError()  # TODO

    def locateOrderingsInveredWithOpChangeGroundtruthClass(self) -> CurveInTile:
        """
        $$\left{ R_I : I(tp) I(fn) = I(tn) I(fp) \right}
        = \left{ R_I : a(I) + b(I) = 1 \right}$$
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
            rankingScore = self.getCanonicalImportances(param1, param2)
            assert isinstance(rankingScore, RankingScore)
            importance = rankingScore.importance
            itn = importance.itn()
            ifp = importance.ifp()
            ifn = importance.ifn()
            itp = importance.itp()
            assert itn >= 0
            assert ifp >= 0
            assert ifn >= 0
            assert itp >= 0
            assert math.isclose(itn + itp, 1)
            assert math.isclose(ifp + ifn, 1)
            assert math.isclose(param1, self.getValueParam1(rankingScore))
            assert math.isclose(param2, self.getValueParam2(rankingScore))
