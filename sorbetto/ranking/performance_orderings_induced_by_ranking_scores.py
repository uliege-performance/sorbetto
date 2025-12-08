from typing import Any

from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)
from sorbetto.performance.constraint_fixed_prediction_rates import (
    ConstraintFixedPredictionRates,
)
from sorbetto.performance.performance_ordering_induced_by_one_score import (
    PerformanceOrderingInducedByOneScore,
)
from sorbetto.ranking.importance import Importance
from sorbetto.ranking.ranking_score import RankingScore

# FIXME: for many of the scores listed here, the behavior is different from ranking scores !!!!


class PerformanceOrderingsInducedByRankingScores:
    @staticmethod
    def _copyPerformanceOrdering(
        to_mimic: PerformanceOrderingInducedByOneScore | RankingScore,
        name: str | None,
        abbreviation: str | None,
        symbol: str | None,
        additional_constraint: Any = None,
    ) -> PerformanceOrderingInducedByOneScore:
        if isinstance(to_mimic, PerformanceOrderingInducedByOneScore):
            score = to_mimic.score
        elif isinstance(to_mimic, RankingScore):
            score = to_mimic
        else:
            assert False
        importance = score.importance
        constraint = score.constraint
        if constraint is None:
            if additional_constraint is None:
                pass  # nothing to do
            else:
                constraint = additional_constraint
        else:
            if additional_constraint is None:
                pass  # nothing to do
            else:
                assert False  # not supported !
        new_score = RankingScore(importance=importance, constraint=constraint)
        # FIXME: We have a ranking score that leads to the same performance ordering
        # as the score we want. This is far from the best idea, but we just lie here
        # and rename the ranking score. This is risky because the library user can
        # retrieve this score: he would then be mistaken if he used it to obtain values!
        new_score.rename(name, abbreviation, symbol)
        return PerformanceOrderingInducedByOneScore(new_score)

    @staticmethod
    def getTrueNegativeRate() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *True Negative Rate*.
        See :meth:`sorbetto.ranking.RankingScore.getTrueNegativeRate`
        """
        score = RankingScore.getTrueNegativeRate()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getTruePositiveRate() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *True Positive Rate*.
        See :meth:`sorbetto.ranking.RankingScore.getTruePositiveRate`
        """
        score = RankingScore.getTruePositiveRate()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getSpecificity() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Specificity*.
        See :meth:`sorbetto.ranking.RankingScore.getSpecificity`
        """
        score = RankingScore.getSpecificity()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getSelectivity() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Selectivity*.
        See :meth:`sorbetto.ranking.RankingScore.getSelectivity`
        """
        score = RankingScore.getSelectivity()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getSensitivity() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Sensitivity*.
        See :meth:`sorbetto.ranking.RankingScore.getSensitivity`
        """
        score = RankingScore.getSensitivity()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getNegativePredictiveValue() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Negative Predictive Value*.
        See :meth:`sorbetto.ranking.RankingScore.getNegativePredictiveValue`
        """
        score = RankingScore.getNegativePredictiveValue()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getPositivePredictiveValue() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Positive Predictive Value*.
        See :meth:`sorbetto.ranking.RankingScore.getPositivePredictiveValue`
        """
        score = RankingScore.getPositivePredictiveValue()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getPrecision() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Precision*.
        See :meth:`sorbetto.ranking.RankingScore.getPrecision`
        """
        score = RankingScore.getPrecision()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getInversePrecision() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Inverse Precision*.
        See :meth:`sorbetto.ranking.RankingScore.getInversePrecision`
        """
        score = RankingScore.getInversePrecision()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getRecall() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Recall*.
        See :meth:`sorbetto.ranking.RankingScore.getRecall`
        """
        score = RankingScore.getRecall()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getInverseRecall() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Inverse Recall*.
        See :meth:`sorbetto.ranking.RankingScore.getInverseRecall`
        """
        score = RankingScore.getInverseRecall()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getIntersectionOverUnion() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Intersection over Union*.
        See :meth:`sorbetto.ranking.RankingScore.getIntersectionOverUnion`
        """
        score = RankingScore.getIntersectionOverUnion()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getInverseIntersectionOverUnion() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Inverse Intersection over Union*.
        See :meth:`sorbetto.ranking.RankingScore.getInverseIntersectionOverUnion`
        """
        score = RankingScore.getInverseIntersectionOverUnion()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getJaccard() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Jaccard*.
        See :meth:`sorbetto.ranking.RankingScore.getJaccard`
        """
        score = RankingScore.getJaccard()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getInverseJaccard() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Inverse Jaccard*.
        See :meth:`sorbetto.ranking.RankingScore.getInverseJaccard`
        """
        score = RankingScore.getInverseJaccard()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getTanimotoCoefficient() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Tanimoto Coefficient*.
        See :meth:`sorbetto.ranking.RankingScore.getTanimotoCoefficient`
        """
        score = RankingScore.getTanimotoCoefficient()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getSimilarity() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Similarity*.
        See :meth:`sorbetto.ranking.RankingScore.getSimilarity`
        """
        score = RankingScore.getSimilarity()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getCriticalSuccessIndex() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Critical Success Index*.
        See :meth:`sorbetto.ranking.RankingScore.getCriticalSuccessIndex`
        """
        score = RankingScore.getCriticalSuccessIndex()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getF(beta=1.0) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *F*.
        See :meth:`sorbetto.ranking.RankingScore.getF`
        """
        score = RankingScore.getF(beta=beta)
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getInverseF(beta=1.0) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Inverse F*.
        See :meth:`sorbetto.ranking.RankingScore.getInverseF`
        """
        score = RankingScore.getInverseF(beta=beta)
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getDiceSorensenCoefficient() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Dice-Sørensen Coefficient*.
        See :meth:`sorbetto.ranking.RankingScore.getDiceSorensenCoefficient`
        """
        score = RankingScore.getDiceSorensenCoefficient()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getZijdenbosSimilarityIndex() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Zijdenbos Similarity Index*.
        See :meth:`sorbetto.ranking.RankingScore.getZijdenbosSimilarityIndex`
        """
        score = RankingScore.getZijdenbosSimilarityIndex()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getCzekanowskiBinaryIndex() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Czekanowski Binary Index*.
        See :meth:`sorbetto.ranking.RankingScore.getCzekanowskiBinaryIndex`
        """
        score = RankingScore.getCzekanowskiBinaryIndex()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getAccuracy() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Accuracy*.
        See :meth:`sorbetto.ranking.RankingScore.getAccuracy`
        """
        score = RankingScore.getAccuracy()
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getBennettS() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score Bennett's :math:`S`.
        This score is related to the accuracy :math:`A` by :math:`S=2A-1`.

        Reference: :cite:t:`Warrens2012TheEffect`.
        """
        to_mimic = RankingScore.getAccuracy()
        name = "Bennett S"
        abbreviation = None
        symbol = "$B_S$"
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getSimilarityCoefficientsS() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by all the scores *Similarity Coefficients S*.
        Similarity coefficients of the family :math:`S_\\theta`, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        to_mimic = RankingScore.getAccuracy()
        name = "Similarity Coefficients S"
        abbreviation = None
        symbol = "$S_\\theta$"
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getSimilarityCoefficientsT() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by all the scores *Similarity Coefficients T*.
        Similarity coefficients of the family :math:`T_\\theta`, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        to_mimic = RankingScore.getJaccard()
        name = "Similarity Coefficients T"
        abbreviation = None
        symbol = "$T_\\theta$"
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    # @staticmethod
    # def getSimilarityCoefficients() -> Conic:
    #     """
    #     Returns the performance ordering induced by the scores *Similarity Coefficients*.
    #     Similarity coefficients, as defined in :cite:t:`Batyrshin2016Visualization`.
    #     See :cite:t:`Batyrshin2016Visualization` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
    #     """
    #     raise NotImplementedError()  # TODO: Implement this!

    @staticmethod
    def getStandardizedNegativePredictiveValue(
        priorPos,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Standardized Negative Predictive Value*.
        The Standardized Negative Predictive Value (SNPV) is defined in :cite:t:`Heston2011Standardizing` as

        .. math::
            SNPV=\\frac{TNR}{TNR+FNR}=\\frac{NPV \\pi_+ }{NPV( \\pi_+ - \\pi_- )+ \\pi_- }

        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0

        to_mimic = RankingScore.getNegativePredictiveValue()
        name = "Standardized Negative Predictive Value"
        abbreviation = "SNPV"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )
        # FIXME: We should add a constraint to the result: this is correct if and
        # only if the priors are fixed, but no matter what these priors are. But,
        # we do not have yet any mechanism to encode it in the library ...

    @staticmethod
    def getStandardizedPositivePredictiveValue(
        priorPos,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Standardized Positive Predictive Value*.
        Standardized Positive Predictive Value (SPPV) is defined in :cite:t:`Heston2011Standardizing` as

        .. math::
            SPPV=\\frac{ TPR }{ FPR + TPR }=\\frac{ PPV  \\pi_- }{ PPV ( \\pi_- - \\pi_+ )+ \\pi_+ }

        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0

        to_mimic = RankingScore.getPositivePredictiveValue()
        name = "Standardized Positive Predictive Value"
        abbreviation = "SPPV"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )
        # FIXME: We should add a constraint to the result: this is correct if and
        # only if the priors are fixed, but no matter what these priors are. But,
        # we do not have yet any mechanism to encode it in the library ...

    @staticmethod
    def getNegativeLikelihoodRatioComplement(
        priorPos,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Negative Likelihood Ratio Complement*.
        Negative Likelihood Ratio.
        References: :cite:t:`Gardner2006Receiver‐operating,Glas2003TheDiagnosticOddsRatio,Powers2020Evaluation-arxiv,Brown2006ROC`
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0

        to_mimic = RankingScore.getNegativePredictiveValue()
        name = "Complement of the Negative Likelihood Ratio"
        abbreviation = "-NLR"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )
        # FIXME: We should add a constraint to the result: this is correct if and
        # only if the priors are fixed, but no matter what these priors are. But,
        # we do not have yet any mechanism to encode it in the library ...

    @staticmethod
    def getPositiveLikelihoodRatio(priorPos) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Positive Likelihood Ratio*.
        Positive Likelihood Ratio.
        References: :cite:t:`Gardner2006Receiver-operating,Glas2003TheDiagnosticOddsRatio,Powers2020Evaluation-arxiv,Brown2006ROC,Altman1994Diagnostic`
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0

        to_mimic = RankingScore.getPositivePredictiveValue()
        name = "Positive Likelihood Ratio"
        abbreviation = "PLR"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )
        # FIXME: We should add a constraint to the result: this is correct if and
        # only if the priors are fixed, but no matter what these priors are. But,
        # we do not have yet any mechanism to encode it in the library ...

    @staticmethod
    def getSkewInsensitiveVersionOfF1(
        priorPos,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Skew-Insensitive Version of F1*.
        The skew-insensitive version of :math:`F_1`.
        Defined in cite:t:`Flach2003TheGeometry`.
        """
        score = RankingScore.getSkewInsensitiveVersionOfF1(priorPos)
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getWeightedAccuracy(
        priorPos: float, weightPos: float
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Weighted Accuracy*.
        See :meth:`sorbetto.ranking.RankingScore.getWeightedAccuracy`
        """
        score = RankingScore.getWeightedAccuracy(priorPos, weightPos)
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getMacroAveragedRecall(
        priorPos: float,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *(Arithmetically) Macro-Averaged Recall*.
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedRecall`
        """
        score = RankingScore.getMacroAveragedRecall(priorPos)
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getBalancedAccuracy(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Balanced Accuracy*.
        See :meth:`sorbetto.ranking.RankingScore.getBalancedAccuracy`
        """
        score = RankingScore.getBalancedAccuracy(priorPos)
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getYoudenJ(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Youden*.
        Youden's index or Youden's :math:`Y_J` statistic.
        Defined in :cite:t:`Youden1950Index`
        References: :cite:t:`Fluss2005Estimation`.
        Related to the balanced accuracy by :math:`Y_J = TNR + TPR - 1 = 2 BA - 1`.
        Synonyms: informedness and Peirce Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        to_mimic = RankingScore.getBalancedAccuracy(priorPos)
        name = "Youden J"
        abbreviation = None
        symbol = "$Y_J$"
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getTrueSkillStatistic(
        priorPos: float,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *True Skill Statistic*.
        See :cite:t:`Armistead2013Wagner`.
        """
        to_mimic = RankingScore.getBalancedAccuracy(priorPos)
        name = "True Skill Statistic"
        abbreviation = "TSS"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getPeirceSkillScore(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Peirce Skill Score*.
        See :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        """
        to_mimic = RankingScore.getBalancedAccuracy(priorPos)
        name = "Peirce Skill Score"
        abbreviation = "PSS"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getInformedness(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Informedness*.
        See :cite:t:`Pierard2025Foundations`, Section A.7.4
        """
        to_mimic = RankingScore.getBalancedAccuracy(priorPos)
        name = "Informedness"
        abbreviation = "INFO"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getCohenCorrected(
        rankingScore: RankingScore, priorPos: float
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        When correcting a ranking score :math:`R_I` in the same way as Cohen did with
        the accuracy in :cite:t:`Cohen1960ACoefficient`, we obtain the score

        .. math::
            X = \\frac{ R_I - R_I \\circ noskill }{ 1 - R_I \\circ noskill }

        where :math:`noskill` denotes the operation that transforms a performance
        :math:`P` into :math:`P'` such that :math:`P'(Y, \\hat{Y}) = P(Y) P(\\hat{Y})`.

        The score :math:`X` is not a ranking score. However, when
        used on performances with the class priors, for the negative and positive
        classes of :math:`P(Y=c_-)=\\pi_-` and :math:`P(Y=c_+)=\\pi_+`, respectively,
        the performance ordering induced by :math:`X` is the same as the one
        induced by the ranking score :math:`R_{I'}` with the importance
        :math:`I'` proportional to

        * :math:`I'(tn) = \\pi_+^2 I(fn)`,
        * :math:`I'(fp) = I(fp)`,
        * :math:`I'(fn) = I(fn)`,
        * and :math:`I'(tp) = \\pi_-^2 I(fp)`.

        See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.4.

        Args:
            rankingScore (RankingScore): a ranking score :math:`R_I`
            priorPos (float): the prior of the positive class, :math:`\\pi_+ \\in [0, 1]`

        Returns:
            PerformanceOrderingInducedByOneScore: the performance ordering induced by the Cohen-corrected version of :math:`R_I`, :math:`X`.
        """
        # TODO: Implement Cohen's correction also in the case of fixed prediction rates
        assert isinstance(rankingScore, RankingScore)
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0
        priorNeg = 1.0 - priorPos

        importance = rankingScore.importance
        ifp = importance.ifp
        ifn = importance.ifn

        itn_corrected = priorPos * priorPos * ifn
        itp_corrected = priorNeg * priorNeg * ifp
        importance = Importance(itn_corrected, ifp, ifn, itp_corrected)
        constraint = ConstraintFixedClassPriors(priorPos=priorPos)
        score = RankingScore(importance, constraint=constraint)

        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getCohenKappa(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Cohen Kappa*
        (:math:`\\kappa`), also called *Kappa statistic*. It is defined in
        :cite:t:`Cohen1960ACoefficient` as

        .. math::
            \\kappa = \\frac{ A - A \\circ noskill }{ 1 - A \\circ noskill }

        where :math:`noskill` denotes the operation that transforms a performance
        :math:`P` into :math:`P'` such that :math:`P'(Y, \\hat{Y}) = P(Y) P(\\hat{Y})`.

        The score :math:`\\kappa` is not a ranking score. However, when
        used on performances with the class priors, for the negative and positive
        classes of :math:`P(Y=c_-)=\\pi_-` and :math:`P(Y=c_+)=\\pi_+`, respectively,
        the performance ordering induced by :math:`\\kappa` is the same as the one
        induced by the ranking score :math:`R_{I}` with the importance
        :math:`I` proportional to

        * :math:`I(tn) = \\pi_+^2`,
        * :math:`I(fp) = 1`,
        * :math:`I(fn) = 1`,
        * and :math:`I(tp) = \\pi_-^2`.

        See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.4.

        References: :cite:t:`Kaymak2012TheAUK`
        Synonyms: Heidke Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.3.
        """
        # TODO: Implement Cohen's kappa also in the case of fixed prediction rates
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0
        priorNeg = 1.0 - priorPos

        itn = priorPos * priorPos
        ifp = 1.0
        ifn = 1.0
        itp = priorNeg * priorNeg
        importance = Importance(itn, ifp, ifn, itp)
        constraint = ConstraintFixedClassPriors(priorPos=priorPos)
        to_mimic = RankingScore(importance, constraint=constraint)
        name = "Cohen's kappa"
        abbreviation = "Cohen"
        symbol = "$\\kappa$"
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getHeidkeSkillScore(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Heidke Skill Score".
        See :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        """
        to_mimic = PerformanceOrderingsInducedByRankingScores.getCohenKappa(priorPos)
        name = "Heidke Skill Score"
        abbreviation = "HSS"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getProbabilityTrueNegative(
        *, priorPos: float | None = None, ratePos: float | None = None
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Probability of True Negative".
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
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ = P(\\hat{Y}=c_+) \\in (0,1)`. Defaults to None.

        Returns:
            PerformanceOrderingInducedByOneScore: the performance ordering induced
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
                to_mimic = RankingScore.getNegativePredictiveValue()
                name = "Probability of a True Negative"
                abbreviation = "PTN"
                symbol = None
                additional_constraint = ConstraintFixedPredictionRates(ratePos=ratePos)
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol, additional_constraint
                    )
                )
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                to_mimic = RankingScore.getTrueNegativeRate()
                name = "Probability of a True Negative"
                abbreviation = "PTN"
                symbol = None
                additional_constraint = ConstraintFixedClassPriors(priorPos=priorPos)
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol, additional_constraint
                    )
                )
            else:
                raise RuntimeError("You should not specify both ratePos and priorPos.")

    @staticmethod
    def getRejectionRate(
        *, priorPos: float | None = None, ratePos: float | None = None
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Rejection Rate".
        See :meth:`getProbabilityTrueNegative`.
        """
        to_mimic = (
            PerformanceOrderingsInducedByRankingScores.getProbabilityTrueNegative(
                priorPos=priorPos, ratePos=ratePos
            )
        )
        name = "Rejection Rate"
        abbreviation = "RR"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getProbabilityFalsePositiveComplement(
        *, priorPos: float | None = None, ratePos: float | None = None
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Complement of the Probability of False Positive".
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
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ = P(\\hat{Y}=c_+) \\in (0,1)`. Defaults to None.

        Returns:
            PerformanceOrderingInducedByOneScore: the performance ordering induced
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
                to_mimic = RankingScore.getPositivePredictiveValue()
                name = "Complement of the Probability of a False Positive"
                abbreviation = "-PFP"
                symbol = None
                additional_constraint = ConstraintFixedPredictionRates(ratePos=ratePos)
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol, additional_constraint
                    )
                )
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                to_mimic = RankingScore.getTrueNegativeRate()
                name = "Complement of the Probability of a False Positive"
                abbreviation = "-PFP"
                symbol = None
                additional_constraint = ConstraintFixedClassPriors(priorPos=priorPos)
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol, additional_constraint
                    )
                )
            else:
                raise RuntimeError("You should not specify both ratePos and priorPos.")

    @staticmethod
    def getProbabilityFalseNegativeComplement(
        *, priorPos: float | None = None, ratePos: float | None = None
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Complement of the Probability of False Negative".
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
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ = P(\\hat{Y}=c_+) \\in (0,1)`. Defaults to None.

        Returns:
            PerformanceOrderingInducedByOneScore: the performance ordering induced
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
                to_mimic = RankingScore.getNegativePredictiveValue()
                name = "Complement of the Probability of a False Negative"
                abbreviation = "-PFN"
                symbol = None
                additional_constraint = ConstraintFixedPredictionRates(ratePos=ratePos)
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol, additional_constraint
                    )
                )
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                to_mimic = RankingScore.getTruePositiveRate()
                name = "Complement of the Probability of a False Negative"
                abbreviation = "-PFN"
                symbol = None
                additional_constraint = ConstraintFixedClassPriors(priorPos=priorPos)
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol, additional_constraint
                    )
                )
            else:
                raise RuntimeError("You should not specify both ratePos and priorPos.")

    @staticmethod
    def getProbabilityTruePositive(
        *, priorPos: float | None = None, ratePos: float | None = None
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Probability of True Positive".
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
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ = P(\\hat{Y}=c_+) \\in (0,1)`. Defaults to None.

        Returns:
            PerformanceOrderingInducedByOneScore: the performance ordering induced
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
                to_mimic = RankingScore.getPositivePredictiveValue()
                name = "Probability of a True Positive"
                abbreviation = "PTP"
                symbol = None
                additional_constraint = ConstraintFixedPredictionRates(ratePos=ratePos)
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol, additional_constraint
                    )
                )
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                to_mimic = RankingScore.getTruePositiveRate()
                name = "Probability of a True Positive"
                abbreviation = "PTP"
                symbol = None
                additional_constraint = ConstraintFixedClassPriors(priorPos=priorPos)
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol, additional_constraint
                    )
                )
            else:
                raise RuntimeError("You should not specify both ratePos and priorPos.")

    @staticmethod
    def getDetectionRate(
        *, priorPos: float | None = None, ratePos: float | None = None
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Detection Rate".
        See :meth:`getProbabilityTruePositive`.
        """
        to_mimic = (
            PerformanceOrderingsInducedByRankingScores.getProbabilityTruePositive(
                priorPos=priorPos, ratePos=ratePos
            )
        )
        name = "Detection Rate"
        abbreviation = "DR"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getMacroAveragedPrecision(
        ratePos: float,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *(Arithmetically) Macro-Averaged Precision*.
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedPrecision`
        """
        score = RankingScore.getMacroAveragedPrecision(ratePos)
        return PerformanceOrderingInducedByOneScore(score)

    @staticmethod
    def getMarkedness(ratePos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Markedness".
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedPrecision`
        Defined in :cite:t:`Powers2020Evaluation-arxiv` as :math:`NPV+ PPV -1`.
        Synonyms: Clayton Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        """
        to_mimic = RankingScore.getMacroAveragedPrecision(ratePos)
        name = "Markedness"
        abbreviation = "MARK"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getClaytonSkillScore(ratePos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Clayton Skill Score".
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedPrecision`
        """
        to_mimic = RankingScore.getMacroAveragedPrecision(ratePos)
        name = "Clayton Skill Score"
        abbreviation = "CSS"
        symbol = None
        return PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
            to_mimic, name, abbreviation, symbol
        )

    @staticmethod
    def getNormalizedConfusionMatrixDeterminant(
        *, priorPos: float | None = None, ratePos: float | None = None
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the determinant of the normalized
        confusion matrix.

        .. math::
            |\\mathcal{C}| = PTN \\, PTP - PFP \\, PFN

        This score is a skill score in the sense that:

        * it takes the zero value for all no-skill performances
         (:math:`P(Y,\\hat{Y}) = P(Y) P(\\hat{Y}) \\Rightarrow |\\mathcal{C}| = 0`);
        * a negative value for the worst performances
         (:math:`P(S=0)=1 \\Rightarrow |\\mathcal{C}|<0`);
        * and a positive value for the best performances
         (:math:`P(S=1)=1 \\Rightarrow |\\mathcal{C}|>0`).

        Denoting the class priors by :math:`\\pi_- = P(Y=c_-)` and :math:`\\pi_+ = P(Y=c_+)`,
        and assuming none of these two quantities is zero, we have

        .. math::
            |\\mathcal{C}| = \\pi_- \\pi_+ ( TNR + TPR - 1 ) = \\pi_- \\pi_+ ( 2 mRe - 1 )

        Thus, when the class priors are fixed, the performance ordering induced
        by the determinant of the confusion matrix is the same as the one induced
        by the macro-averaged recall :math:`mRe` (a.k.a. Peirce Skill Score).

        Denoting the prediction rates by :math:`\\tau_- = P(\\hat{Y}=c_-)` and :math:`\\tau_+ = P(\\hat{Y}=c_+)`,
        and assuming none of these two quantities is zero, we have

        .. math::
            |\\mathcal{C}| = \\tau_- \\tau_+ ( NPV + PPV - 1 ) = \\tau_- \\tau_+ ( 2 mPr - 1 )

        Thus, when the prediction rates are fixed, the performance ordering induced
        by the determinant of the confusion matrix is the same as the one induced
        by the macro-averaged precision :math:`mPr` (a.k.a. Clayton Skill Score).

        Some works using this score: :cite:t:`Wimmer2006APerson`.

        See https://en.wikipedia.org/wiki/Confusion_matrix

        See https://en.wikipedia.org/wiki/Determinant
        """
        if priorPos is None:
            if ratePos is None:
                raise RuntimeError("You should specify either ratePos or priorPos.")
            else:
                assert isinstance(ratePos, float)
                assert ratePos > 0.0  # not >=, see doc here-above
                assert ratePos < 1.0  # not <=, see doc here-above
                to_mimic = RankingScore.getMacroAveragedPrecision(ratePos=ratePos)
                name = "Normalized Confusion Matrix Determinant"
                abbreviation = None
                symbol = "$|\\mathcal{C}|$"
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol
                    )
                )
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                to_mimic = RankingScore.getMacroAveragedRecall(priorPos=priorPos)
                name = "Normalized Confusion Matrix Determinant"
                abbreviation = None
                symbol = "$|\\mathcal{C}|$"
                return (
                    PerformanceOrderingsInducedByRankingScores._copyPerformanceOrdering(
                        to_mimic, name, abbreviation, symbol
                    )
                )
            else:
                raise RuntimeError("You should not specify both ratePos and priorPos.")
