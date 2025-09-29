# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import numpy as np

from sorbetto.geometry.bilinear_curve import BilinearCurve
from sorbetto.geometry.line import Line
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.ranking.importance import Importance
from sorbetto.ranking.ranking_score import RankingScore


class ParameterizationDefault(AbstractParameterization):
    """
    This is the parameterization described in :cite:t:`Pierard2024TheTile-arxiv`.
    """

    def __init__(self):
        AbstractParameterization.__init__(self)

    def getNameParameter1(self):
        return "a(I)"

    def getNameParameter2(self):
        return "b(I)"

    def getBoundsParameter1(self) -> tuple[float, float]:
        return 0.0, 1.0

    def getBoundsParameter2(self) -> tuple[float, float]:
        return 0.0, 1.0

    def getCanonicalImportance(self, param1, param2) -> Importance:
        assert isinstance(param1, float)
        assert param1 >= 0.0
        assert param1 <= 1.0

        assert isinstance(param2, float)
        assert param2 >= 0.0
        assert param2 <= 1.0

        a = param1
        b = param2

        itn = 1.0 - a
        ifp = 1.0 - b
        ifn = b
        itp = a

        return Importance(itn, ifp, ifn, itp)

    def getCanonicalImportanceVectorized(
        self, param1: np.ndarray, param2: np.ndarray
    ) -> np.ndarray:
        assert isinstance(param1, np.ndarray)
        assert isinstance(param2, np.ndarray)
        assert np.all(param1 >= 0.0)
        assert np.all(param1 <= 1.0)
        assert np.all(param2 >= 0.0)
        assert np.all(param2 <= 1.0)
        assert param1.shape == param2.shape

        a = param1
        b = param2

        itn = 1.0 - a
        ifp = 1.0 - b
        ifn = b
        itp = a

        return np.stack([itn, ifp, ifn, itp], axis=-1)

    def getValueParameter1(self, rankingScore) -> float:
        assert isinstance(rankingScore, RankingScore)
        importance = rankingScore.importance
        itn = importance.itn
        # ifp = importance.ifp ()
        # ifn = importance.ifn ()
        itp = importance.itp
        a = itp / (itn + itp)
        return a

    def getValueParameter2(self, rankingScore) -> float:
        assert isinstance(rankingScore, RankingScore)
        importance = rankingScore.importance
        # itn = importance.itn ()
        ifp = importance.ifp
        ifn = importance.ifn
        # itp = importance.itp ()
        b = ifn / (ifp + ifn)
        return b

    def locateOrderingsPuttingNoSkillPerformancesOnAnEqualFootingForFixedClassPriors(
        self, priorPos: float
    ) -> BilinearCurve:
        """
        The set of performance orderings induced by ranking scores that put all no-skill
        performances, for given class priors :math:`(\\pi_-, \\pi_+)`, on an equal footing is given by

        .. math:
             \\left\\{ \\pi_+^2 I(tp) I(fn) = \\pi_-^2 I(tn) I(fp) \\right\\}

        See :cite:t:`Pierard2024TheTile-arxiv`, Figure 6, left.
        See Theorem 3 of :cite:t:`Pierard2025TheManifold`.
        See :cite:t:`Pierard2024TheTile-arxiv`, Figure 8.

        Args:
            priorPos (float): the prior of the positive class, :math:`\\pi_+`

        Returns:
            BilinearCurve: The locus (a curve).
        """
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        priorNeg = 1.0 - priorPos

        priorPosSq = priorPos * priorPos
        priorNegSq = priorNeg * priorNeg

        #     pi_pos^2 itp ifn = pi_neg^2 itn ifp
        # <=> pi_pos^2 a b = pi_neg^2 (1-a) (1-b)
        # <=> ( pi_pos^2 - pi_neg^2 ) a b + ( pi_neg^2 ) a + ( pi_neg^2 ) b + ( - pi_neg^2 ) = 0

        Kab = priorPosSq - priorNegSq
        Ka = priorNegSq
        Kb = priorNegSq
        K = -priorNegSq

        name = "locus of performance orderings putting all no-skill performances with the class priors ({:g}, {:g}) on an equal footing".format(
            priorNeg, priorPos
        )
        return BilinearCurve(Kab, Ka, Kb, K, name)

    def locateOrderingsPuttingNoSkillPerformancesOnAnEqualFootingForFixedPredictionRates(
        self, ratePos: float
    ) -> BilinearCurve:
        """
        The set of performance orderings induced by ranking scores that put all no-skill
        performances, for given prediction rates :math:`(\\tau_-, \\tau_+)`, on an equal footing is given by

        .. math:
            \\left\\{ \\tau_+^2 I(tp) I(fp) = \\tau_-^2 I(tn) I(fn) \\right\\}

        See :cite:t:`Pierard2024TheTile-arxiv`, Figure 6, right.
        See Theorem 4 of :cite:t:`Pierard2025TheManifold`.

        Args:
            ratePos (float): the prediction rate for the positive class, :math:`\\tau_+`

        Returns:
            AbstractGeometricObject2D: The locus (a curve).
        """
        assert isinstance(ratePos, float)
        assert ratePos > 0.0
        assert ratePos < 1.0
        rateNeg = 1.0 - ratePos

        ratePosSq = ratePos * ratePos
        rateNegSq = rateNeg * rateNeg

        #     tau_pos^2 itp ifp = tau_neg^2 itn ifn
        # <=> tau_pos^2 a (1-b) = tau_neg^2 (1-a) b
        # <=> ( tau_neg^2 - tau_pos^2 ) a b + ( tau_pos^2 ) a + ( - tau_neg^2 ) b + ( 0 ) = 0

        Kab = rateNegSq - ratePosSq
        Ka = ratePosSq
        Kb = -rateNegSq
        K = 0.0

        name = "locus of performance orderings putting all no-skill performances with the prediction rates ({:g}, {:g}) on an equal footing".format(
            rateNeg, ratePos
        )
        return BilinearCurve(Kab, Ka, Kb, K, name)

    def locateOrderingsInvertedWithOpChangePredictedClass(self) -> Line:
        # Solution:
        #     I(tp) I(fp) = I(tn) I(fn)
        #  => x (1-y) = (1-x) y
        # <=> x = y
        #
        # Equation of geometric object:
        # a x + b y + c = 0
        a = 1.0
        b = -1.0
        c = 0.0
        name = "orderings that are inverted when the predicted class changes"
        return Line(a, b, c, name=name)

    def locateOrderingsInvertedWithOpChangeGroundtruthClass(self) -> Line:
        # Solution:
        #     I(tp) I(fn) = I(tn) I(fp)
        #  => x y = (1-x) (1-y)
        # <=> x + y - 1 = 0
        #
        # Equation of geometric object:
        # a x + b y + c = 0
        a = 1.0
        b = 1.0
        c = -1.0
        name = "orderings that are inverted when the groundtruth class changes"
        return Line(a, b, c, name=name)

    def locateRelativeImportanceSatisfying(self, itn: float, itp: float) -> Line:
        # Solution:
        # x = itp / ( itn + itp )
        #
        # Equation of geometric object:
        # a x + b y + c = 0
        a = -1.0
        b = 0.0
        c = itp / (itn + itp)
        name = "relative importance of satisfying"
        return Line(a, b, c, name=name)

    def locateRelativeImportanceUnsatisfying(self, ifp: float, ifn: float) -> Line:
        # Solution:
        # y = ifn / ( ifp + ifn )
        #
        # Equation of geometric object:
        # a x + b y + c = 0
        a = 0.0
        b = -1.0
        c = ifn / (ifp + ifn)
        name = "relative importance of unsatisfying"
        return Line(a, b, c, name=name)

    def getName(self):
        return "default"

    def __str__(self):
        return "default parameterization"
