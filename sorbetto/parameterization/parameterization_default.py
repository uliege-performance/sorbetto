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

    def getName(self):
        return "default"

    def __str__(self):
        return "default parameterization"
