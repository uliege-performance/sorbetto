from sorbetto.core.importance import Importance
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization


class ParameterizationAdaptedToPredictionRates(AbstractParameterization):
    """
    Not yet published. Experimental. In Sébastien's mind.

    Using the parameterization adapted to prediction rates with performances corresponding
    to the prediction rates $(\tau_-,\tau_+)$ is equivalent to using the default
    parameterization after applying a target shift operation
    :cite:t:`Sipka2022TheHitchhikerGuide` on all performances in order to balance the
    prediction rates.

    See Theorem 6 of future "paper 6".
    """

    def __init__(self, ratePos):
        assert isinstance(ratePos, float)
        assert ratePos >= 0.0
        assert ratePos <= 1.0
        self._ratePos = ratePos
        self._rateNeg = 1 - ratePos
        AbstractParameterization.__init__(self)

    def getRateOfNegativePredictions(self) -> float:
        return self._rateNeg

    def getRateOfPositivePredictions(self) -> float:
        return self._ratePos

    def getNameParameter1(self): ...

    def getNameParameter2(self): ...

    def getBoundsParameter1(self) -> tuple[float, float]:
        return 0.0, 1.0

    def getBoundsParameter2(self) -> tuple[float, float]:
        return 0.0, 1.0

    def getCanonicalImportance(self, param1, param2) -> Importance: ...

    def getValueParameter1(self, rankingScore) -> float: ...

    def getValueParameter2(self, rankingScore) -> float: ...

    def getName(self):
        return "adapted to prediction rates (pos: {:g})".format(self._ratePos)
