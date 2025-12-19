# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import numpy as np

from sorbetto.geometry import (
    BilinearCurve,
    Line,
    LinearFractionalTransformationTwoVariables,
    PencilOfLines,
)
from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking import Importance, RankingScore

from ._abstract_parameterization import (
    AbstractParameterization,
)


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
        assumption = ConstraintFixedClassPriors(priorPos=priorPos)
        return BilinearCurve(Kab, Ka, Kb, K, name, assumption)

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
        assumption = ConstraintFixedPredictionRates(ratePos=ratePos)
        return BilinearCurve(Kab, Ka, Kb, K, name, assumption)

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

    @staticmethod
    def getParameter1ForValueZeroInROC(
        priorPos: float,
    ) -> LinearFractionalTransformationTwoVariables:
        """
        Returns the function :math:`f : \\mathbb{R}^2 \\rightarrow [0,1] : (fpr, tpr) \\mapsto a(I)`,
        under the assumptions that :math:`R_I(P)=0`, :math:`P(Y=c_+)=\\pi_+`, :math:`FPR(P)=fpr`, and
        :math:`TPR(P)=tpr`. Note that this function is extended to allow :math:`fpr` and :math:`tpr`
        to be out of the :math:`[0,1]` range.

        It turns out that all ranking scores :math:`R_I` achieve their minimal value (:math:`0`) when

        .. math::
            R_I ( P ) = 0
            \\Leftrightarrow
            I(tn) P(\\{tn\\}) + I(tp) P(\\{tp\\}) = 0

        so that

        .. math::
            \\underbrace{
                \\frac{
                    I(tp)
                }{
                    I(tn) + I(tp)
                }
            }_{=a(I)}
            = \\underbrace{
                \\frac{
                    P(\\{tn\\})
                }{
                    P(\\{tn\\}) - P(\\{tp\\})
                }
            }_{=f(P)}

        Note that the left hand side depends only on the importance :math:`I`
        and the right hand side depends only on the performance :math:`P` and
        is an expected value ratio score.

        When the class priors are fixed and given by :math:`(\\pi_-, \\pi_+)`,

        .. math::
            f(P) = \\frac{ (1-fpr) \\, \\pi_- }{ (1-fpr) \\, \\pi_- - tpr \\, \\pi_+}

        which is the returned function. When :math:`a` is known, one can use this
        function to retrieve the line in ROC where :math:`R_I(P)=0`.

        Args:
            priorPos (float): The prior of the positive class, :math:`\\pi_+\\in(0,1)`.

        Returns:
            LinearFractionalTransformationTwoVariables: The function :math:`f`.
        """
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        priorNeg = 1.0 - priorPos

        a = -priorNeg
        b = 0.0
        c = priorNeg
        d = -priorNeg
        e = -priorPos
        f = priorNeg

        return LinearFractionalTransformationTwoVariables(a, b, c, d, e, f)

    def getPencilParameter1ForValueZeroInROC(
        self,
        priorPos: float,
    ) -> PencilOfLines:
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        priorNeg = 1.0 - priorPos

        parameter_name = self.getNameParameter1()

        # Let us take a look at the case in which the score takes the value 0:
        #     itn ptn + itp ptp = 0
        # <=> itn ( (1-fpr) priorNeg ) + itp ( tpr priorPos ) = 0
        # <=> fpr ( - itn priorNeg ) + tpr ( itp priorPos ) + ( itn priorNeg ) = 0
        # The coefficients of this line depend only on the importance values
        # given to the true negatives and to the true positives. So, only the
        # first parameter (i.e., a) is responsible for moving this line.

        # When the first parameter (a) takes the value 0, it means that
        # itn = 1 and itp = 0:
        # => fpr ( - priorNeg ) + tpr ( 0 ) + ( priorNeg ) = 0
        a = -priorNeg
        b = 0.0
        c = priorNeg
        line_0 = Line(a, b, c, "line for value {}=0".format(parameter_name))

        # When the first parameter (a) takes the value 1, it means that
        # itn = 0 and itp = 1:
        # => fpr ( 0 ) + tpr ( priorPos ) + ( 0 ) = 0
        a = 0.0
        b = priorPos
        c = 0.0
        line_1 = Line(a, b, c, "line for value {}=1".format(parameter_name))

        # For canonical ranking scores, itn=1-a and itp=a. Thus,
        #     fpr ( - itn priorNeg ) + tpr ( itp priorPos ) + ( itn priorNeg ) = 0
        #  => fpr ( - (1-a) priorNeg ) + tpr ( a priorPos ) + ( (1-a) priorNeg ) = 0
        # <=> (1-a) [ fpr ( - priorNeg ) + tpr ( 0 ) + ( priorNeg ) ] + a [ fpr ( 0 ) + tpr ( priorPos ) + ( 0 ) ] = 0
        # <=> (1-a) line_0 + a line_1 = 0
        # This gives the meaning of the pencil's parameters: (1-a) and a for,
        # respectively, line_0 and line_1.

        name = (
            "pencil in ROC for parameter {} and a prior of positive class of {}".format(
                parameter_name, priorPos
            )
        )
        return PencilOfLines(line_0, line_1, name)

    @staticmethod
    def getParameter2ForValueOneInROC(
        priorPos: float,
    ) -> LinearFractionalTransformationTwoVariables:
        """
        Returns the function :math:`f : \\mathbb{R}^2 \\rightarrow [0,1] : (fpr, tpr) \\mapsto b(I)`,
        under the assumptions that :math:`R_I(P)=1`, :math:`P(Y=c_+)=\\pi_+`, :math:`FPR(P)=fpr`, and
        :math:`TPR(P)=tpr`. Note that this function is extended to allow :math:`fpr` and :math:`tpr`
        to be out of the :math:`[0,1]` range.

        It turns out that all ranking scores :math:`R_I` achieve their maximal value (:math:`1`) when

        .. math::
            R_I ( P ) = 1
            \\Leftrightarrow
            I(fp) P(\\{fp\\}) + I(fn) P(\\{fn\\}) = 0

        so that

        .. math::
            \\underbrace{
                \\frac{
                    I(fn)
                }{
                    I(fp) + I(fn)
                }
            }_{=b(I)}
            = \\underbrace{
                \\frac{
                    P(\\{fp\\})
                }{
                    P(\\{fp\\}) - P(\\{fn\\})
                }
            }_{=f(P)}

        Note that the left hand side depends only on the importance :math:`I`
        and the right hand side depends only on the performance :math:`P` and
        is an expected value ratio score.

        When the class priors are fixed and given by :math:`(\\pi_-, \\pi_+)`,

        .. math::
            f(P) = \\frac{ fpr \\, \\pi_- }{ fpr \\, \\pi_- - (1-tpr) \\, \\pi_+}

        which is the returned function. When :math:`b` is known, one can use this
        function to retrieve the line in ROC where :math:`R_I(P)=1`.

        Args:
            priorPos (float): The prior of the positive class, :math:`\\pi_+\\in(0,1)`.

        Returns:
            LinearFractionalTransformationTwoVariables: The function :math:`f`.
        """
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        priorNeg = 1.0 - priorPos

        a = priorNeg
        b = 0.0
        c = 0.0
        d = priorNeg
        e = priorPos
        f = -priorPos

        return LinearFractionalTransformationTwoVariables(a, b, c, d, e, f)

    def getPencilParameter2ForValueOneInROC(
        self,
        priorPos: float,
    ) -> PencilOfLines:
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        priorNeg = 1.0 - priorPos

        parameter_name = self.getNameParameter2()

        # Let us take a look at the case in which the score takes the value 1:
        #     ifp pfp + ifn pfn = 0
        # <=> ifp ( fpr priorNeg ) + ifn ( (1-tpr) priorPos ) = 0
        # <=> fpr ( ifp priorNeg ) + tpr ( - ifn priorPos ) + ( ifn priorPos ) = 0
        # The coefficients of this line depend only on the importance values
        # given to the false positives and to the false negatives. So, only the
        # second parameter (i.e., b) is responsible for moving this line.

        # When the second parameter (b) takes the value 0, it means that
        # ifp = 1 and ifn = 0:
        # => fpr ( priorNeg ) + tpr ( 0 ) + ( 0 ) = 0
        a = priorNeg
        b = 0.0
        c = 0.0
        line_0 = Line(a, b, c, "line for value {}=0".format(parameter_name))

        # When the second parameter (b) takes the value 1, it means that
        # ifp = 0 and ifn = 1:
        # => fpr ( 0 ) + tpr ( - priorPos ) + ( priorPos ) = 0
        a = 0.0
        b = -priorPos
        c = priorPos
        line_1 = Line(a, b, c, "line for value {}=1".format(parameter_name))

        # For canonical ranking scores, ifp=1-b and ifn=b. Thus,
        #     fpr ( ifp priorNeg ) + tpr ( - ifn priorPos ) + ( ifn priorPos ) = 0
        #  => fpr ( (1-b) priorNeg ) + tpr ( - b priorPos ) + ( b priorPos ) = 0
        # <=> (1-b) [ fpr ( priorNeg ) + tpr ( 0 ) + ( 0 ) ] + b [ fpr ( 0 ) + tpr ( - priorPos ) + ( priorPos ) ] = 0
        # <=> (1-b) line_0 + b line_1 = 0
        # This gives the meaning of the pencil's parameters: (1-b) and b for,
        # respectively, line_0 and line_1.

        name = (
            "pencil in ROC for parameter {} and a prior of positive class of {}".format(
                parameter_name, priorPos
            )
        )
        return PencilOfLines(line_0, line_1, name)

    def getName(self):
        return "default"

    def __str__(self):
        return "default parameterization"
