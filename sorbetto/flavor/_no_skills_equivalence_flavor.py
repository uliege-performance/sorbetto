# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Literal

import numpy as np

from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
    Importance,
)

from ._abstract_numeric_flavor import AbstractNumericFlavor


class NoSkillsEquivalenceFlavor(AbstractNumericFlavor):
    r"""
    The "No-Skill Equivalence Flavor" is a Numeric Flavor that, for any given
    importance values, gives the value of a parameter controling a parametric
    set of performances such that all no-skill performances in this set are put
    on an equal footing (ie, are considered equivalent because the ranking score
    gives the same value to all of them), for any given importance values.
    The no-skill performances are the ones such that

    .. math::
        P(Y, \hat{Y}) = P(Y) P(\hat{Y})

    This Flavor can be used with the set of performances that corresponds to
    some fixed prediction rates (the parameter controling the parametric set).
    The set of performance orderings induced by ranking scores that put all
    no-skill performances, for given prediction rates
    :math:`(P(\hat{Y}=c_-), P(\hat{Y}=c_+))=(\tau_-, \tau_+)`,
    on an equal footing is given by

    .. math::
        \tau_+^2 I(tp) I(fp) = \tau_-^2 I(tn) I(fn)

    See Theorem 4 of :cite:t:`Pierard2025TheManifold`.
    See :cite:t:`Pierard2024TheTile-arxiv`, Fig. 6, right.

    This Flavor can also be used with the set of performances that corresponds to
    some fixed class priors (the parameter controling the parametric set).
    The set of performance orderings induced by ranking scores that put all
    no-skill performances, for given class priors
    :math:`(P(Y=c_-), P(Y=c_+)) = (\pi_-, \pi_+)`,
    on an equal footing is given

    .. math::
        \pi_+^2 I(tp) I(fn) = \pi_-^2 I(tn) I(fp)

    See Theorem 3 of :cite:t:`Pierard2025TheManifold`.
    See :cite:t:`Pierard2024TheTile-arxiv`, Fig. 6, left.
    """

    RATE_NEG = "negative prediction rate"
    RATE_POS = "positive prediction rate"
    PRIOR_NEG = "prior of the negative class"
    PRIOR_POS = "prior of the positive class"

    def __init__(
        self,
        parameter_name: Literal[
            "negative prediction rate",
            "positive prediction rate",
            "prior of the negative class",
            "prior of the positive class",
        ],
        name: str | None = None,
        colormap: Any = None,
    ):
        r"""
        Constructs a new NoSkillsEquivalenceFlavor.

        If `parameter_name` is "negative prediction rate", the Flavor gives the
        value :math:`\tau_-` such that all performances :math:`P` satisfying
        :math:`P(\hat{Y}=c_-)=\tau_-` and :math:`P(Y, \hat{Y}) = P(Y) P(\hat{Y})`
        are put on an equal footing by the ranking scores.

        If `parameter_name` is "positive prediction rate", the Flavor gives the
        value :math:`\tau_+` such that all performances :math:`P` satisfying
        :math:`P(\hat{Y}=c_+)=\tau_+` and :math:`P(Y, \hat{Y}) = P(Y) P(\hat{Y})`
        are put on an equal footing by the ranking scores.

        If `parameter_name` is "prior of the negative class", the Flavor gives the
        value :math:`\pi_-` such that all performances :math:`P` satisfying
        :math:`P(Y=c_-)=\pi_-` and :math:`P(Y, \hat{Y}) = P(Y) P(\hat{Y})`
        are put on an equal footing by the ranking scores.

        If `parameter_name` is "prior of the negative class", the Flavor gives the
        value :math:`\pi_+` such that all performances :math:`P` satisfying
        :math:`P(Y=c_+)=\pi_+` and :math:`P(Y, \hat{Y}) = P(Y) P(\hat{Y})`
        are put on an equal footing by the ranking scores.

        Args:
            parameter_name (str): The parameter controling the parametric set.
            name (str, optional): The Flavor name. Defaults to "No-Skill Equivalence Flavor".
            colormap (Any, optional): The colormap. Defaults to None.
        """
        c = self.__class__
        assert parameter_name in {c.RATE_NEG, c.RATE_POS, c.PRIOR_NEG, c.PRIOR_POS}
        self._parameter_name = parameter_name
        if name is None:
            match self._parameter_name:
                case self.RATE_NEG:
                    name = r"No-Skill Equivalence Flavor ($\tau_-$)"
                case self.RATE_POS:
                    name = r"No-Skill Equivalence Flavor ($\tau_+$)"
                case self.PRIOR_NEG:
                    name = r"No-Skill Equivalence Flavor ($\pi_-$)"
                case self.PRIOR_POS:
                    name = r"No-Skill Equivalence Flavor ($\pi_+$)"
                case _:
                    assert False
        super().__init__(name=name, colormap=colormap)

    def __call__(
        self,
        importance: Importance | np.ndarray,
    ) -> float | np.ndarray:
        assert (
            isinstance(importance, Importance)
            or isinstance(importance, np.ndarray)
            and importance.shape[-1] == 4
        )  # TODO: RankingScore also supports list[Importance]. Why not here?

        # See how it is done in RankingScore._parse_importance
        if isinstance(importance, Importance):
            itn = importance.itn
            ifp = importance.ifp
            ifn = importance.ifn
            itp = importance.itp
        elif isinstance(importance, np.ndarray):
            assert importance.shape[-1] == 4
            itn = importance[..., 0]
            ifp = importance[..., 1]
            ifn = importance[..., 2]
            itp = importance[..., 3]
        else:
            assert False

        match self._parameter_name:
            case self.RATE_NEG:
                # x : rate of negative predictions, tau_-
                # I(tn) I(fn) x^2 = I(tp) I(fp) (1-x)^2
                a = itn * ifn
                b = itp * ifp
            case self.RATE_POS:
                # x : rate of positive predictions, tau_+
                # I(tp) I(fp) x^2 = I(tn) I(fn) (1-x)^2
                a = itp * ifp
                b = itn * ifn
            case self.PRIOR_NEG:
                # x : prior of the negative class, pi_-
                # I(tn) I(fp) x^2 = I(tp) I(fn) (1-x)^2
                a = itn * ifp
                b = itp * ifn
            case self.PRIOR_POS:
                # x : prior of the positive class, pi_+
                # I(tp) I(fn) x^2 = I(tn) I(fp) (1-x)^2
                a = itp * ifn
                b = itn * ifp
            case _:
                assert False

        #     a x^2 = b (1-x)^2, x in [0, 1], a >= 0, b >= 0
        # <=> x = sqrt(b) / [ sqrt(a) + sqrt(b) ]
        sqrt_a = np.sqrt(a)
        sqrt_b = np.sqrt(b)
        with np.errstate(invalid="ignore"):
            return sqrt_b / (sqrt_a + sqrt_b)
        # Note that this should return "NaN" when a == 0 and b == 0,
        # because no matter what the value of the parameter is, all
        # no-skill performances of the parametric set are equivalent.

    def getDefaultColormap(self):
        """
        The default colormap to use with this Flavor.

        Returns:
            _type_: the colormap.
        """
        return "gray"

    def getLowerBound(self) -> float:
        """
        No matter if the parameter is a class prior or a prediction rate,
        # the lower bound for the parameter value is 0.

        Returns:
            float: the lower bound for the parameter value
        """
        return 0.0

    def getUpperBound(self) -> float:
        """
        No matter if the parameter is a class prior or a prediction rate,
        # the upper bound for the parameter value is 1.

        Returns:
            float: the upper bound for the parameter value
        """
        return 1.0

    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintRelativeImportanceSatisfyingUnsatisfying): a constraint on importances.

        Returns:
            bool: True
        """
        assert isinstance(
            constraint, ConstraintRelativeImportanceSatisfyingUnsatisfying
        )
        return True

    def isCompatibleWithConstraintOnClassPriors(
        self, constraint: ConstraintFixedClassPriors
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintFixedClassPriors): a constraint on performances.

        Returns:
            bool: True
        """
        assert isinstance(constraint, ConstraintFixedClassPriors)
        return True

    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        """
        There is no known compatibility issues.

        Args:
            constraint (ConstraintFixedPredictionRates): a constraint on performances.

        Returns:
            bool: True
        """
        assert isinstance(constraint, ConstraintFixedPredictionRates)
        return True
