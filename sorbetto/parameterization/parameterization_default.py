import math

import numpy as np

from sorbetto.core.importance import Importance
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
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

        itn = 1 - a
        ifp = 1 - b
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

        itn = 1 - a
        ifp = 1 - b
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

    @staticmethod  # TODO: is this implemented in the right class?
    def getPriorNegForIsoValuedNoSkillPerformances(
        param1: float, param2: float
    ) -> float:
        """
        Returns the prior of the negative class $\\pi_-$ such that the performance ordering
        located at (param1, param2) puts all the performances corresponding to the priors
        $(P(Y=c_-), P(Y=c_+))=(\\pi_-, 1-\\pi_-)$ on an equal footing.

        See :cite:t:`Pierard2024TheTile-arxiv`, Fig. 6, left.

        Args:
            param1 (float): the value of the first parameter, $a$
            param2 (float): the value of the second parameter, $b$

        Returns:
            float: $\\pi_-$
        """
        a = param1
        b = param2

        assert a >= 0.0 and a <= 1.0
        assert b >= 0.0 and b <= 1.0
        if a == 0.0 and b == 1.0:
            return math.nan
        if a == 1.0 and b == 0.0:
            return math.nan
        quadratic_term = a + b - 1.0
        if quadratic_term == 0.0:
            return 0.5
        else:
            delta = a * b * (1.0 - a) * (1.0 - b)
            sol_1 = (a * b - math.sqrt(delta)) / quadratic_term
            ok_1 = sol_1 >= 0.0 and sol_1 <= 1.0
            sol_2 = (a * b + math.sqrt(delta)) / quadratic_term
            ok_2 = sol_2 >= 0.0 and sol_2 <= 1.0
            if ok_1 and not ok_2:
                return sol_1
            if ok_2 and not ok_1:
                return sol_2
            assert False

    @staticmethod  # TODO: is this implemented in the right class?
    def getPriorPosForIsoValuedNoSkillPerformances(
        param1: float, param2: float
    ) -> float:
        """
        Returns the prior of the positive class $\\pi_+$ such that the performance ordering
        located at (param1, param2) puts all the performances corresponding to the priors
        $(P(Y=c_-), P(Y=c_+))=(1-\\pi_+, \\pi_+)$ on an equal footing.

        See :cite:t:`Pierard2024TheTile-arxiv`, Fig. 6, left.

        Args:
            param1 (float): the value of the first parameter, $a$
            param2 (float): the value of the second parameter, $b$

        Returns:
            float: $\\pi_+$
        """
        f = ParameterizationDefault.getPriorNegForIsoValuedNoSkillPerformances
        return 1.0 - f(param1, param2)

    @staticmethod  # TODO: is this implemented in the right class?
    def getRateNegPredictionsForIsoValuedNoSkillPerformances(
        param1: float, param2: float
    ) -> float:
        """
        Returns the rate of predictions for the negative class $\\tau_-$ such that the performance ordering
        located at (param1, param2) puts all the performances corresponding to the prediction rates
        $(P(\\hat{Y}=c_-), P(\\hat{Y}=c_+))=(\\tau_-, 1-\\tau_-)$ on an equal footing.

        See :cite:t:`Pierard2024TheTile-arxiv`, Fig. 6, right.

        Args:
            param1 (float): the value of the first parameter, $a$
            param2 (float): the value of the second parameter, $b$

        Returns:
            float: $\\tau_-$
        """
        f = ParameterizationDefault.getPriorNegForIsoValuedNoSkillPerformances
        return f(param1, 1 - param2)

    @staticmethod  # TODO: is this implemented in the right class?
    def getRatePosPredictionsForIsoValuedNoSkillPerformances(
        param1: float, param2: float
    ) -> float:
        """
        Returns the rate of predictions for the positive class $\\tau_+$ such that the performance ordering
        located at (param1, param2) puts all the performances corresponding to the prediction rates
        $(P(\\hat{Y}=c_-), P(\\hat{Y}=c_+))=(1-\\tau_+, \\tau_+)$ on an equal footing.

        See :cite:t:`Pierard2024TheTile-arxiv`, Fig. 6, right.

        Args:
            param1 (float): the value of the first parameter, $a$
            param2 (float): the value of the second parameter, $b$

        Returns:
            float: $\\tau_+$
        """
        f = ParameterizationDefault.getRateNegPredictionsForIsoValuedNoSkillPerformances
        return 1.0 - f(param1, param2)

    def getName(self):
        return "default"

    def __str__(self):
        return "default parameterization"
