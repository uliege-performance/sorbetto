from sorbetto.performance.performance_ordering_induced_by_one_score import (
    PerformanceOrderingInducedByOneScore,
)
from sorbetto.ranking.ranking_score import RankingScore


class PerformanceOrderingsInducedByRankingScores:
    @staticmethod
    def getCohenCorrected(
        rankingScore: RankingScore,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the Cohen-corrected version of the provided ranking score.
        See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.4.
        """
        assert isinstance(rankingScore, RankingScore)
        raise NotImplementedError()  # TODO

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
        Returns the performance ordering induced by the score *Bennett's :math:`S`*.
        This score is related to the accuracy :math:`A` by :math:`S=2A-1`.

        Reference: :cite:t:`Warrens2012TheEffect`.
        """
        return PerformanceOrderingInducedByOneScore.getAccuracy()

    @staticmethod
    def getSimilarityCoefficientsT() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the scores *Similarity Coefficients T*.
        Similarity coefficients of the family :math:`T_\\theta`, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO: Implement this!

    @staticmethod
    def getSimilarityCoefficientsS() -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the scores *Similarity Coefficients S*.
        Similarity coefficients of the family :math:`S_\\theta`, as defined in :cite:t:`Gower1986Metric`.
        See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
        """
        raise NotImplementedError()  # TODO: Implement this!

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
        raise NotImplementedError()  # TODO: Implement this!

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
        raise NotImplementedError()  # TODO: Implement this!

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
        raise NotImplementedError()  # TODO: Implement this!

    @staticmethod
    def getPositiveLikelihoodRatio(priorPos) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Positive Likelihood Ratio*.
        Positive Likelihood Ratio.
        References: :cite:t:`Gardner2006Receiver-operating,Glas2003TheDiagnosticOddsRatio,Powers2020Evaluation-arxiv,Brown2006ROC,Altman1994Diagnostic`
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO: Implement this!

    @staticmethod
    def getSkewInsensitiveVersionOfF(
        priorPos,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Skew-Insensitive Version of F1*.
        The skew-insensitive version of :math:`F_1`.
        Defined in cite:t:`Flach2003TheGeometry`.
        """
        return PerformanceOrderingInducedByOneScore(
            RankingScore.getSkewInsensitiveVersionOfF1()
        )

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
        Youden's index or Youden's :math:` Y_J ` statistic.
        Defined in :cite:t:`Youden1950Index`
        References: :cite:t:`Fluss2005Estimation`.
        Related to the balanced accuracy by :math:` Y_J =TNR+ TPR -1=2 BA -1`.
        Synonyms: informedness and Peirce Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.5.
        """
        raise NotImplementedError()  # TODO: Implement this!

    @staticmethod
    def getPeirceSkillScore(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Peirce Skill Score*.
        """
        raise NotImplementedError()  # TODO: Implement this!

    @staticmethod
    def getInformedness(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Informedness*.
        """
        """
        See :cite:t:`Pierard2025Foundations`, Section A.7.4
        """
        raise NotImplementedError()  # TODO: Implement this!

    @staticmethod
    def getCohenKappa(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *Cohen Kappa*.
        """
        """
        Cohen's :math:`\\scoreCohenKappa` statistic.
        Defined in :cite:t:`Cohen1960ACoefficient`
        References: :cite:t:`Kaymak2012TheAUK`
        Synonyms: Heidke Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        See :cite:t:`Pierard2025Foundations`, Section A.7.4, and :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.3.
        """
        raise NotImplementedError()  # TODO: Implement this!

    @staticmethod
    def getHeidkeSkillScore(priorPos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Heidke Skill Score".
        """
        raise NotImplementedError()  # TODO: Implement this!

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
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ \\in (0,1) `. Defaults to None.

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
                return PerformanceOrderingInducedByOneScore.getNegativePredictiveValue()
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                return PerformanceOrderingInducedByOneScore.getTrueNegativeRate()
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
        return PerformanceOrderingInducedByOneScore.getProbabilityTrueNegative(
            priorPos=priorPos, ratePos=ratePos
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
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ \\in (0,1)`. Defaults to None.

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
                return PerformanceOrderingInducedByOneScore.getPositivePredictiveValue()
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                return PerformanceOrderingInducedByOneScore.getTrueNegativeRate()
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
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ \\in (0,1)`. Defaults to None.

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
                return PerformanceOrderingInducedByOneScore.getNegativePredictiveValue()
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                return PerformanceOrderingInducedByOneScore.getTruePositiveRate()
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
            ratePos (float | None): The prediction rate of the positive class, :math:`\\tau_+ \\in (0,1) `. Defaults to None.

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
                return PerformanceOrderingInducedByOneScore.getPositivePredictiveValue()
        else:
            if ratePos is None:
                assert isinstance(priorPos, float)
                assert priorPos > 0.0  # not >=, see doc here-above
                assert priorPos < 1.0  # not <=, see doc here-above
                return PerformanceOrderingInducedByOneScore.getTruePositiveRate()
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
        return PerformanceOrderingInducedByOneScore.getProbabilityTruePositive(
            priorPos=priorPos, ratePos=ratePos
        )

    @staticmethod
    def getNormalizedConfusionMatrixDeterminant(
        priorPos: float,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the determinant of the normalized
        confusion matrix is :math:`|\\mathcal{C}|= \\pi_-  \\pi_+  Y_J `.
        Some works using this score: :cite:t:`Wimmer2006APerson`.

        See https://en.wikipedia.org/wiki/Confusion_matrix
        See https://en.wikipedia.org/wiki/Determinant
        """
        raise NotImplementedError()  # TODO: Implement this!

    @staticmethod
    def getMacroAveragedPrecision(
        ratePos: float,
    ) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score *(Arithmetically) Macro-Averaged Precision*.
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedPrecision`
        """
        return PerformanceOrderingInducedByOneScore(
            RankingScore.getMacroAveragedPrecision(ratePos)
        )

    @staticmethod
    def getMarkedness(ratePos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Markedness".
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedPrecision`
        Defined in :cite:t:`Powers2020Evaluation-arxiv` as :math:`NPV+ PPV -1`.
        Synonyms: Clayton Skill Score :cite:t:`Canbek2017Binary,Wilks2020Statistical`.
        """
        return PerformanceOrderingInducedByOneScore(
            RankingScore.getMacroAveragedPrecision(ratePos)
        )

    @staticmethod
    def getClaytonSkillScore(ratePos: float) -> "PerformanceOrderingInducedByOneScore":
        """
        Returns the performance ordering induced by the score "Clayton Skill Score".
        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedPrecision`
        """
        return PerformanceOrderingInducedByOneScore(
            RankingScore.getMacroAveragedPrecision(ratePos)
        )
