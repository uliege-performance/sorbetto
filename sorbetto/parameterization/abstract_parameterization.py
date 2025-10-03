# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod

import numpy as np

from sorbetto.geometry.abstract_geometric_object_2d import AbstractGeometricObject2D
from sorbetto.geometry.conic import Conic
from sorbetto.geometry.line import Line
from sorbetto.geometry.point import Point
from sorbetto.performance.performance_ordering_induced_by_one_score import (
    PerformanceOrderingInducedByOneScore,
)
from sorbetto.ranking.importance import Importance
from sorbetto.ranking.ranking_score import RankingScore


class AbstractParameterization(ABC):
    """
    This is the base class for all possible ways of mapping all (or a subset of)
    4D importances (that is some application-related preferences) onto 2D Tiles.
    This mechanism allows to map ranking scores, importance values, performance
    orderings, and rankings onto Tiles.

    All ranking scores inducing the same performance ordering should be mapped
    to the same point. It is recommended that the subclasses implement continuous
    mappings between the four importance values and the two parameters.

    Also, it is recommended that:
    (1) the ranking scores giving no importance at all to the true positives are
    mapped to points on the left border (minimal value for the first parameter);
    (2) the ranking scores giving no importance at all to the true negatives are
    mapped to points on the right border (maximal value for the first parameter);
    (3) the ranking scores giving no importance at all to the false positives are
    mapped to points on the lower border (minimal value for the second parameter);
    and (4) the ranking scores giving no importance at all to the false negatives
    are mapped to points on the upper border (minimal value for the second parameter).

    An example of parameterization is the "default" parameterization
    :math:`(x, y)=(a(I), b(I))` that has been defined in :cite:t:`Pierard2024TheTile-arxiv`.
    """

    def __init__(self):
        """
        Constructor.
        """
        ABC.__init__(self)

    @abstractmethod
    def getNameParameter1(self) -> str:
        """
        Returns the name of the first parameter (the horizontal coordinate, :math:`x`, in Tiles)

        Returns:
            str: The name of the first parameter.
        """
        ...

    @abstractmethod
    def getNameParameter2(self) -> str:
        """
        Returns the name of the second parameter (the vertical coordinate, :math:`y`, in Tiles)

        Returns:
            str: The name of the second parameter.
        """
        ...

    @abstractmethod
    def getBoundsParameter1(self) -> tuple[float, float]:
        """
        Returns the bounds for the first parameter (the horizontal coordinate, :math:`x`, in Tiles)

        Returns:
            tuple[float, float]: The bounds :math:`(\\min_x, \\max_x)` for the first parameter, with :math:`\\min_x < \\max_x`.
        """
        ...

    @abstractmethod
    def getBoundsParameter2(self) -> tuple[float, float]:
        """
        Returns the bounds for the second parameter (the vertical coordinate, :math:`y`, in Tiles)

        Returns:
            tuple[float, float]: The bounds :math:`(\\min_y, \\max_y)` for the second parameter, with :math:`\\min_y < \\max_y`.
        """
        ...

    def getExtent(self) -> tuple[float, float, float, float]:
        """
        The axis-aligned bounding box, :math:`(\\min_x, \\max_x, \\min_y, \\max_y)`,
        of Tiles with this parameterization :math:`(x, y)`. This bounding box is
        such that :math:`\\min_x < \\max_x` and :math:`\\min_y < \\max_y`.

        Returns:
            tuple[float, float, float, float]: The axis-aligned bounding box.
        """
        min_x, max_x = self.getBoundsParameter1()
        assert min_x < max_x
        min_y, max_y = self.getBoundsParameter2()
        assert min_y < max_y
        return (min_x, max_x, min_y, max_y)

    def getCanonicalImportance(self, param1: float, param2: float) -> Importance:
        """Returns the canonical importance corresponding to the given parameters.

        Default implementation calls the getCanonicalImportanceVectorized (abstract)
        method.

        Args:
            param1 (float): The first parameter.
            param2 (float): The second parameter.

        Returns:
            The canonical importance.
        """
        assert isinstance(param1, float)
        assert isinstance(param2, float)

        return Importance(
            *self.getCanonicalImportanceVectorized(
                np.array([param1]),
                np.array([param2]),
            )
        )

    @abstractmethod
    def getCanonicalImportanceVectorized(
        self, param1: np.ndarray, param2: np.ndarray
    ) -> np.ndarray:
        """Computes an array of canonical importance values corresponding to
        the given parameters.

        This needs to be implemented by subclasses.

        Args:
            param1 (np.ndarray): The first parameter array.
            param2 (np.ndarray): The second parameter array.

        Returns:
            an array of shape (N, 4) where N is the number of elements in param1 and param2.
        """
        ...

    def getCanonicalRankingScore(self, param1: float, param2: float) -> RankingScore:
        importance = self.getCanonicalImportance(param1, param2)
        return RankingScore(importance)

    @abstractmethod
    def getValueParameter1(self, rankingScore: RankingScore) -> float:
        """
        Returns the value of the first parameter (the horizontal coordinate, :math:`x`, in Tiles)
        corresponding to the given ranking score.

        Args:
            rankingScore (RankingScore): The ranking score.

        Returns:
            float: The value of the first parameter.
        """
        ...

    @abstractmethod
    def getValueParameter2(self, rankingScore) -> float:
        """
        Returns the value of the second parameter (the vertical coordinate, :math:`y`, in Tiles)
        corresponding to the given ranking score.

        Args:
            rankingScore (RankingScore): The ranking score.

        Returns:
            float: The value of the second parameter.
        """
        ...

    def locateRankingScore(self, rankingScore: RankingScore) -> Point:
        """
        Locates any *Ranking Score*.
        """
        assert isinstance(rankingScore, RankingScore)
        param1 = self.getValueParameter1(rankingScore)
        param2 = self.getValueParameter2(rankingScore)
        assumption = rankingScore.constraint
        if assumption is not None:
            return Point(param1, param2, assumption)
        else:
            return Point(param1, param2)

    def locateOrdering(self, ordering: PerformanceOrderingInducedByOneScore) -> Point:
        assert isinstance(ordering, PerformanceOrderingInducedByOneScore)
        score = ordering.score
        assert isinstance(score, RankingScore)
        param1 = self.getValueParameter1(score)
        param2 = self.getValueParameter2(score)
        assumption = score.constraint
        if assumption is not None:
            return Point(param1, param2, assumption)
        else:
            return Point(param1, param2)

    @abstractmethod
    def locateOrderingsPuttingNoSkillPerformancesOnAnEqualFootingForFixedClassPriors(
        self, priorPos: float
    ) -> AbstractGeometricObject2D:
        """
        Locates the set of performance orderings induced by ranking scores that put all no-skill
        performances, for given class priors :math:`(\\pi_-, \\pi_+)`, on an equal footing is given by

        .. math::
            \\left\\{ \\pi_+^2 I(tp) I(fn) = \\pi_-^2 I(tn) I(fp) \\right\\}


        See :cite:t:`Pierard2024TheTile-arxiv`, Figure 6, left.
        # See Theorem 3 of :cite:t:`Pierard2025TheManifold`.
        # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 8.

        Args:
            priorPos (float): the prior of the positive class, :math:`\\pi_+`

        Returns:
            AbstractGeometricObject2D: The locus (a curve).
        """
        ...

    @abstractmethod
    def locateOrderingsPuttingNoSkillPerformancesOnAnEqualFootingForFixedPredictionRates(
        self, ratePos: float
    ) -> AbstractGeometricObject2D:
        """
        Locates the set of performance orderings induced by ranking scores that put all no-skill
        performances, for given prediction rates :math:`(\\tau_-, \\tau_+)`, on an equal footing is given by

        .. math::
            \\left\\{ \\tau_+^2 I(tp) I(fp) = \\tau_-^2 I(tn) I(fn) \\right\\}

        See :cite:t:`Pierard2024TheTile-arxiv`, Figure 6, right.
        # See Theorem 4 of :cite:t:`Pierard2025TheManifold`.

        Args:
            ratePos (float): the prediction rate for the positive class, :math:`\\tau_+`

        Returns:
            AbstractGeometricObject2D: The locus (a curve).
        """
        ...

    @abstractmethod
    def locateOrderingsInvertedWithOpChangePredictedClass(self) -> Conic:
        """
        Locates the set of performance orderings induced by ranking scores
        that are inverted when the operation that consists in changing the
        predicted class is applied to all performances.
        :math:`\\hat{Y}=c_-` becomes :math:`\\hat{Y}=c_+` and vice-versa.
        A performance :math:`P` becomes a performance :math:`P'` such that:

        - :math:`P'(\\{tn\\}) = P(\\{fp\\})`
        - :math:`P'(\\{fp\\}) = P(\\{tn\\})`
        - :math:`P'(\\{fn\\}) = P(\\{tp\\})`
        - :math:`P'(\\{tp\\}) = P(\\{fn\\})`

        As demonstrated in Theorem 1 of :cite:t:`Pierard2025TheManifold`,
        the set is

        .. math::
            \\left\\{ I: I(tp) I(fp) = I(tn) I(fn) \\right\\}
        """
        ...

    @abstractmethod
    def locateOrderingsInvertedWithOpChangeGroundtruthClass(self) -> Conic:
        """
        Locates the set of performance orderings induced by ranking scores
        that are inverted when the operation that consists in changing the
        groundtruth class is applied to all performances.
        :math:`Y=c_-` becomes :math:`Y=c_+` and vice-versa.
        A performance :math:`P` becomes a performance :math:`P'` such that:

        - :math:`P'(\\{tn\\}) = P(\\{fn\\})`
        - :math:`P'(\\{fp\\}) = P(\\{tp\\})`
        - :math:`P'(\\{fn\\}) = P(\\{tn\\})`
        - :math:`P'(\\{tp\\}) = P(\\{fp\\})`

        As demonstrated in Theorem 2 of :cite:t:`Pierard2025TheManifold`,
        the set is

        .. math::
            \\left\\{ I: I(tp) I(fn) = I(tn) I(fp) \\right\\}
        """
        ...

    @abstractmethod
    def locateRelativeImportanceSatisfying(self, itn: float, itp: float) -> Line:
        """
        Locates the set of performance orderings induced by the ranking scores
        corresponding to some given values of importance for the satisfying samples
        (the elements :math:`\\omega` of the sample space :math:`\\Omega` such that
        :math:`S(\\omega)=1` are :math:`S^{-1}(1)=\\{tn, tp\\}`). The importance
        values :math:`I(tn)` and :math:`I(tp)` are provided up to a positive
        scale factor. This is related to the first parameter (the horizontal
        coordinate, :math:`x`, in Tiles).

        Args:
            itn (float): The (relative) importance given to the true negatives, :math:`I(tn) \\ge 0`
            itp (float): The (relative) importance given to the true positives, :math:`I(tp) \\ge 0`

        Returns:
            AbstractGeometricObject2D: The locus on the Tile.
        """
        ...

    @abstractmethod
    def locateRelativeImportanceUnsatisfying(self, ifp: float, ifn: float) -> Line:
        """
        Locates the set of performance orderings induced by the ranking scores
        corresponding to some given values of importance for the unsatisfying samples
        (the elements :math:`\\omega` of the sample space :math:`\\Omega` such that
        :math:`S(\\omega)=0` are :math:`S^{-1}(0)=\\{fp, fn\\}`). The importance
        values :math:`I(fp)` and :math:`I(fn)` are provided up to a positive
        scale factor. This is related to the second parameter (the vertical
        coordinate, :math:`y`, in Tiles).

        Args:
            ifp (float): The (relative) importance given to the true negatives, :math:`I(fp) \\ge 0`
            ifn (float): The (relative) importance given to the true positives, :math:`I(fn) \\ge 0`

        Returns:
            AbstractGeometricObject2D: The locus on the Tile.
        """
        ...

    @abstractmethod
    def getName(self):
        # TODO make it a property?
        pass

    def __str__(self):
        return 'parameterization "{}"'.format(self.getName())

    def unitTest(self):
        import math
        import random

        # TODO move this to a proper test suite

        for trial in range(1000):
            param1 = random.random()
            param2 = random.random()
            rankingScore = self.getCanonicalRankingScore(param1, param2)
            assert isinstance(rankingScore, RankingScore)
            importance = rankingScore.importance
            itn = importance.itn
            ifp = importance.ifp
            ifn = importance.ifn
            itp = importance.itp
            assert itn >= 0
            assert ifp >= 0
            assert ifn >= 0
            assert itp >= 0
            assert math.isclose(itn + itp, 1)
            assert math.isclose(ifp + ifn, 1)
            assert math.isclose(param1, self.getValueParameter1(rankingScore))
            assert math.isclose(param2, self.getValueParameter2(rankingScore))
