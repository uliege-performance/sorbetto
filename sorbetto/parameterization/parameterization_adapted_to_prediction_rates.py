# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from sorbetto.geometry.conic import Conic
from sorbetto.geometry.line import Line
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.ranking.importance import Importance


class ParameterizationAdaptedToPredictionRates(AbstractParameterization):
    """
    Not yet published. Experimental. In Sébastien's mind.

    Using the parameterization adapted to prediction rates with performances corresponding
    to the prediction rates :math:`(\\tau_-,\\tau_+)` is equivalent to using the default
    parameterization after applying a target shift operation
    :cite:t:`Sipka2022TheHitchhikerGuide` on all performances in order to balance the
    prediction rates.

    See Theorem 6 of :cite:t:`Pierard2025TheManifold`.
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

    def getNameParameter1(self):
        raise NotImplementedError()  # TODO: implement this!

    def getNameParameter2(self):
        raise NotImplementedError()  # TODO: implement this!

    def getBoundsParameter1(self) -> tuple[float, float]:
        return 0.0, 1.0

    def getBoundsParameter2(self) -> tuple[float, float]:
        return 0.0, 1.0

    def getCanonicalImportance(self, param1, param2) -> Importance:
        raise NotImplementedError()  # TODO: implement this!

    def getValueParameter1(self, rankingScore) -> float:
        raise NotImplementedError()  # TODO: implement this!

    def getValueParameter2(self, rankingScore) -> float:
        raise NotImplementedError()  # TODO: implement this!

    def locateOrderingsInvertedWithOpChangePredictedClass(self) -> Conic:
        raise NotImplementedError()  # TODO: Implement this!

    def locateOrderingsInvertedWithOpChangeGroundtruthClass(self) -> Conic:
        raise NotImplementedError()  # TODO: Implement this!

    def locateRelativeImportanceSatisfying(self, itn: float, itp: float) -> Line:
        raise NotImplementedError()  # TODO

    def locateRelativeImportanceUnsatisfying(self, ifp: float, ifn: float) -> Line:
        raise NotImplementedError()  # TODO

    def getName(self):
        return "adapted to prediction rates (pos: {:g})".format(self._ratePos)
