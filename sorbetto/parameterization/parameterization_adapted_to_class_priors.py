from sorbetto.core.importance import Importance
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization


class ParameterizationAdaptedToClassPriors(AbstractParameterization):
    """
    Not yet published. Experimental. In Sébastien's mind.


    Using the parameterization adapted to class priors with performances corresponding to
    the class priors :math:`(\\pi_-,\\pi_+)` is equivalent to using the default parameterization
    after applying a target shift operation :cite:t:`Sipka2022TheHitchhikerGuide` on all
    performances in order to balance the class priors.

    See Theorem 5 of future "paper 6".
    """

    def __init__(self, priorPos):
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0
        self._priorPos = priorPos
        self._priorNeg = 1 - priorPos
        AbstractParameterization.__init__(self)

    def getNegativeClassPrior(self) -> float:
        return self._priorNeg

    def getPositiveClassPrior(self) -> float:
        return self._priorPos

    def getNameParameter1(self):
        return "a^{(\\pi)}(I)"

    def getNameParameter2(self):
        return "b^{(\\pi)}(I)"

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

    def getName(self):
        return "adapted to class priors (pos: {:g})".format(self._priorPos)

    def _from_a_b_to_itn_ifp_ifn_itp(self, a, b):
        itn = 1 - a
        ifp = 1 - b
        ifn = b
        itp = a
        return itn, ifp, ifn, itp

    def _from_itn_ifp_ifn_itp_to_a_b(self, itn, ifp, ifn, itp):
        a = itp / (itn + itp)
        b = ifn / (ifp + ifn)
        return a, b

    def _adapt_a_b(self, old_prior_pos, new_prior_pos, old_a, old_b):
        old_I_tn, old_I_fp, old_I_fn, old_I_tp = self._from_a_b_to_itn_ifp_ifn_itp(
            old_a, old_b
        )

        old_prior_neg = 1 - old_prior_pos
        new_prior_neg = 1 - new_prior_pos

        new_I_tn = (
            old_I_tn * old_prior_neg / new_prior_neg
        )  # to be insensitive to the prior change
        new_I_fp = (
            old_I_fp * old_prior_neg / new_prior_neg
        )  # to be insensitive to the prior change
        new_I_fn = (
            old_I_fn * old_prior_pos / new_prior_pos
        )  # to be insensitive to the prior change
        new_I_tp = (
            old_I_tp * old_prior_pos / new_prior_pos
        )  # to be insensitive to the prior change

        new_a, new_b = self._from_itn_ifp_ifn_itp_to_a_b(
            new_I_tn, new_I_fp, new_I_fn, new_I_tp
        )

        return new_a, new_b

    def getImportances(self, param1, param2):
        new_a, new_b = param1, param2
        old_a, old_b = self._adapt_a_b(0.5, self._prior_pos, new_a, new_b)
        return self._from_a_b_to_itn_ifp_ifn_itp(old_a, old_b)

    def getValueParam1(self, itn, ifp, ifn, itp):
        old_a, old_b = self._from_itn_ifp_ifn_itp_to_a_b(itn, ifp, ifn, itp)
        new_a, new_b = self._adapt_a_b(self._prior_pos, 0.5, old_a, old_b)
        return new_a

    def getValueParam2(self, itn, ifp, ifn, itp):
        old_a, old_b = self._from_itn_ifp_ifn_itp_to_a_b(itn, ifp, ifn, itp)
        new_a, new_b = self._adapt_a_b(self._prior_pos, 0.5, old_a, old_b)
        return new_b
