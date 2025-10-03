# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
import math
from collections.abc import Callable
from typing import cast, overload

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

from sorbetto.geometry.bilinear_curve import BilinearCurve
from sorbetto.geometry.conic import Conic
from sorbetto.geometry.line import Line
from sorbetto.geometry.pencil_of_lines import PencilOfLines
from sorbetto.performance.abstract_score import AbstractScore
from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)
from sorbetto.performance.constraint_fixed_prediction_rates import (
    ConstraintFixedPredictionRates,
)
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
    _parse_performance,
)
from sorbetto.performance.roc import _setupROC
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.ranking.importance import Importance, _parse_importance


class RankingScore(AbstractScore):
    """
    Implementation of the family of scores named *ranking scores* (:math:`R_I`)
    in the particular case of problems assimilated to two-class crisp classification.
    More precisely, this is when the sample space contains four elements
    (:math:`\\Omega=\\{tn,fp,fn,tp\\}`) and the random variable satisfaction is
    0.0 for two of them and 1.0 for the other two:

    * :math:`S(tn)=1`;
    * :math:`S(fp)=0`;
    * :math:`S(fn)=0`;
    * :math:`S(tp)=1`.

    The formula for the scores of this family is:

    .. math::
        R_I(P) = \\frac{E_P[SI]}{E_P[I]} = \\frac{ I(tn) P(\\{tn\\}) + I(tp) P(\\{tp\\}) }{ I(tn) P(\\{tn\\}) + I(fp) P(\\{fp\\}) + I(fn) P(\\{fn\\}) + I(tp) P(\\{tp\\}) }
    """

    def __init__(
        self,
        importance: Importance,
        constraint: Callable[[TwoClassClassificationPerformance], bool] | None = None,
        name: str | None = None,
        abbreviation: str | None = None,
        symbol: str | None = None,
    ):
        """
        Args:
            importance (Importance): _description_
            constraint (_type_, optional): _description_. Defaults to None.
            name (str | None, optional): _description_. Defaults to None.
            abbreviation (str | None, optional): _description_. Defaults to None.
            symbol (str | None, optional): _description_. Defaults to None.

        Raises:
            TypeError: _description_
        """
        if not isinstance(importance, Importance):
            raise TypeError(
                f"importance must be an instance of Importance, got {type(importance)}"
            )
        self._importance = importance

        if constraint is not None:
            if not callable(constraint):
                raise TypeError(
                    f"constraint must be a callable, got {type(constraint)}"
                )
        self._constraint = constraint

        default_name = "Ranking Score R_I for I(tn)={:g}, I(fp)={:g}, I(fn)={:g}, I(tp)={:g}".format(
            importance.itn, importance.ifp, importance.ifn, importance.itp
        )
        default_abbreviation = "RS"
        default_symbol = "$R_I$"

        AbstractScore.__init__(
            self,
            default_name,
            default_abbreviation,
            default_symbol,
            name,
            abbreviation,
            symbol,
        )

    @property
    def importance(self) -> Importance:
        """
        A random variable Importance corresponding to this ranking score. The
        importance is defined up to a positive scaling.

        Returns:
            Importance: A random variable Importance corresponding to this ranking score.
        """
        return self._importance

    @property
    def constraint(self) -> Callable[[TwoClassClassificationPerformance], bool] | None:
        return self._constraint

    # TODO: this method might not be in the right class. Should we move it in ParameterizationDefault ?
    @staticmethod
    def equivalent(
        p1: TwoClassClassificationPerformance,
        p2: TwoClassClassificationPerformance,
    ) -> Conic:
        """
        Computes, on the Tile with the default parameterization, the locus of performance orderings for which
        the performances `p1` and `p2` are equivalent. This locus is a curve, a conic section.

        Args:
            p1 (TwoClassClassificationPerformance): _description_
            p2 (TwoClassClassificationPerformance): _description_

        Returns:
            Conic: the conic section.
        """

        # ( itn ptn1 + itp ptp1 ) / ( itn ptn1 + ifp pfp1 + ifn pfn1 + itp ptp1 ) = ( itn ptn2 + itp ptp2 ) / ( itn ptn2 + ifp pfp2 + ifn pfn2 + itp ptp2 )
        # ( itn ptn1 + itp ptp1 ) ( itn ptn2 + ifp pfp2 + ifn pfn2 + itp ptp2 ) = ( itn ptn2 + itp ptp2 ) ( itn ptn1 + ifp pfp1 + ifn pfn1 + itp ptp1 )
        # ( itn ptn1 + itp ptp1 ) ( ifp pfp2 + ifn pfn2 ) = ( itn ptn2 + itp ptp2 ) ( ifp pfp1 + ifn pfn1 )
        # ( itn ptn1 + itp ptp1 ) ( ifp pfp2 + ifn pfn2 ) - ( itn ptn2 + itp ptp2 ) ( ifp pfp1 + ifn pfn1 ) = 0
        # ( (1-a) ptn1 + a ptp1 ) ( (1-b) pfp2 + b pfn2 ) - ( (1-a) ptn2 + a ptp2 ) ( (1-b) pfp1 + b pfn1 ) = 0
        # ( ptn1 + a (ptp1-ptn1) ) ( pfp2 + b (pfn2-pfp2) ) - ( ptn2 + a (ptp2-ptn2) ) ( pfp1 + b (pfn1-pfp1) ) = 0
        #
        # K + Ka a + Kb b + Kab a b = 0
        #
        # With:
        # K = ptn1 pfp2 - ptn2 pfp1
        # Ka = (ptp1-ptn1)pfp2 - (ptp2-ptn2)pfp1
        # Kb = ptn1(pfn2-pfp2) - ptn2(pfn1-pfp1)
        # Kab = (ptp1-ptn1)(pfn2-pfp2) - (ptp2-ptn2)(pfn1-pfp1)

        ptn1 = p1.ptn
        pfp1 = p1.pfp
        pfn1 = p1.pfn
        ptp1 = p1.ptp

        ptn2 = p2.ptn
        pfp2 = p2.pfp
        pfn2 = p2.pfn
        ptp2 = p2.ptp

        K = ptn1 * pfp2 - ptn2 * pfp1
        Ka = (ptp1 - ptn1) * pfp2 - (ptp2 - ptn2) * pfp1
        Kb = ptn1 * (pfn2 - pfp2) - ptn2 * (pfn1 - pfp1)
        Kab = (ptp1 - ptn1) * (pfn2 - pfp2) - (ptp2 - ptn2) * (pfn1 - pfp1)

        # return Conic(0.0, Kab, 0.0, Ka, Kb, K, "equivalent")
        return BilinearCurve(Kab, Ka, Kb, K, "equivalent")

    def isCanonical(self, abs_tol: float = 1e-8) -> bool:
        """
        Tests if this Ranking Score is canonical. This property is related to
        the performance ordering induced by these scores: the ordering is
        insensitive to the relative importance given to the satisfying samples
        :math:`\\{tn,tp\\}` with respect to the unsatisfying samples
        :math:`\\{fp,fn\\}`. Therefore, a Ranking Score is said canonical if
        and only if

        .. math::
            I(tn)+I(tp) = I(fp)+I(fn)

        See :cite:t:`Pierard2024TheTile-arxiv`, Definition 1.

        Args:
            abs_tol (float, optional): The absolute tolerance to use for the comparison of :math:`I(tn)+I(tp)` with :math:`I(fp)+I(fn)`. Defaults to 1e-8.

        Returns:
            bool: True if the Ranking Score is canonical, False otherwise.
        """
        return self._importance.isCanonical()

    def drawInROC(
        self,
        fig: Figure,
        ax: Axes,
        priorPos: float,
        show_values_map: bool = True,
        show_iso_value_lines: bool = True,
        show_colorbar: bool = True,
        show_no_skills: bool = True,
        show_priors: bool = True,
        show_unbiased: bool = True,
        show_opposite_unbiased: bool = True,
    ) -> None:
        """
        Displays the ranking score in the ROC space.
        See https://en.wikipedia.org/wiki/Receiver_operating_characteristic

        Args:
            fig (Figure): The matplotlib.pyplot Figure to use for drawing.
            ax (Axes): The matplotlib.pyplot Axes to use for drawing.
            priorPos (float): prior of the positive class :math:`\\pi_+ \\in (0,1)`
            show_values_map (bool, optional): _description_. Defaults to True.
            show_iso_value_lines (bool, optional): _description_. Defaults to True.
            show_colorbar (bool, optional): _description_. Defaults to True.
            show_no_skills (bool, optional): _description_. Defaults to True.
            show_priors (bool, optional): _description_. Defaults to True.
            show_unbiased (bool, optional): _description_. Defaults to True.
            show_opposite_unbiased (bool, optional): _description_. Defaults to True.
        """

        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)

        assert isinstance(show_values_map, bool)
        assert isinstance(show_iso_value_lines, bool)
        assert isinstance(show_colorbar, bool)
        assert isinstance(show_no_skills, bool)
        assert isinstance(show_priors, bool)
        assert isinstance(show_unbiased, bool)
        assert isinstance(show_opposite_unbiased, bool)

        # Check priors
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        priorNeg = 1.0 - priorPos

        # TNR, FPR, FNR, TPR
        grid_size = 1001
        vec_fpr = vec_tpr = np.linspace(0, 1, num=grid_size)
        mat_fpr, mat_tpr = np.meshgrid(vec_fpr, vec_tpr, indexing="xy")
        mat_tnr = 1 - mat_fpr
        mat_fnr = 1 - mat_tpr

        # PTN, PFP, PFN, PTP
        mat_ptn = mat_tnr * priorNeg
        mat_pfp = mat_fpr * priorNeg
        mat_pfn = mat_fnr * priorPos
        mat_ptp = mat_tpr * priorPos

        # ITN, IFP, IFN, ITP
        itn = self._importance.itn
        ifp = self._importance.ifp
        ifn = self._importance.ifn
        itp = self._importance.itp

        # Values taken by the scores
        mat_satisfying = itn * mat_ptn + itp * mat_ptp
        mat_unsatisfying = ifp * mat_pfp + ifn * mat_pfn
        with np.errstate(invalid="ignore"):
            mat_values = mat_satisfying / (mat_satisfying + mat_unsatisfying)

        if show_values_map:
            extent = 0, 1, 0, 1
            cmap = plt.cm.bone  # type: ignore
            im = ax.imshow(
                mat_values,
                extent=extent,
                origin="lower",
                interpolation="bilinear",
                cmap=cmap,
            )

            if show_colorbar:
                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size="5%", pad="5%")
                fig.colorbar(im, cax)

        if show_iso_value_lines:
            cs = ax.contour(
                vec_fpr,
                vec_tpr,
                mat_values,
                levels=np.linspace(0, 1, 21),
                colors="cornflowerblue",
            )
            ax.clabel(cs, inline=True, fontsize=8)

        _setupROC(
            fig,
            ax,
            priorPos=priorPos,
            show_no_skills=show_no_skills,
            show_priors=show_priors,
            show_unbiased=show_unbiased,
            show_opposite_unbiased=show_opposite_unbiased,
        )

    def getPencilInROC(self, priorPos: float) -> PencilOfLines:
        """
        For given class priors :math:`(\\pi_-,\\pi_+)`, the locus of points in
        ROC where the ranking score takes a given value is a line, and all these
        lines form a pencil.

        Args:
            priorPos (_type_): the prior of the positive class, :math:`pi_+\\in[0.0,1.0]`

        Returns:
            PencilOfLines: The pencil of lines.
        """
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        priorNeg = 1.0 - priorPos

        itn = self._importance.itn
        ifp = self._importance.ifp
        ifn = self._importance.ifn
        itp = self._importance.itp

        # TODO: generalize what we do here:
        # it could be useful to be able to find the line for any value

        # When the score takes the value 0:
        #     itn ptn + itp ptp = 0
        # <=> itn ( (1-fpr) priorNeg ) + itp ( tpr priorPos ) = 0
        # <=> fpr ( - itn priorNeg ) + tpr ( itp priorPos ) + ( itn priorNeg ) = 0
        a = -itn * priorNeg
        b = itp * priorPos
        c = itn * priorNeg
        line_0 = Line(a, b, c, "line for value 0")

        # When the score takes the value 1:
        #     ifp pfp + ifn pfn = 0
        # <=> ifp ( fpr priorNeg ) + ifn ( (1-tpr) priorPos ) = 0
        # <=> fpr ( ifp priorNeg ) + tpr ( - ifn priorPos ) + ( ifn priorPos ) = 0
        a = ifp * priorNeg
        b = -ifn * priorPos
        c = ifn * priorPos
        line_1 = Line(a, b, c, "line for value 1")

        name = "pencil in ROC for score {} and a prior of positive class of {}".format(
            self.name, priorPos
        )
        return PencilOfLines(line_0, line_1, name)

    @overload
    @staticmethod
    def _compute(
        importance: Importance,
        performance: TwoClassClassificationPerformance,
    ) -> float: ...

    # Importance + Performance mixed
    @overload
    @staticmethod
    def _compute(
        importance: Importance,
        performance: FiniteSetOfTwoClassClassificationPerformances | np.ndarray,
    ) -> np.ndarray: ...

    @overload
    @staticmethod
    def _compute(
        importance: list[Importance] | np.ndarray,
        performance: TwoClassClassificationPerformance,
    ) -> np.ndarray: ...

    # Importance + Performance array mode
    @overload
    @staticmethod
    def _compute(
        importance: list[Importance] | np.ndarray,
        performance: FiniteSetOfTwoClassClassificationPerformances | np.ndarray,
    ) -> np.ndarray: ...

    # I=float, P=float → float
    @overload
    @staticmethod
    def _compute(
        *,
        itn: float,
        ifp: float,
        ifn: float,
        itp: float,
        ptn: float,
        pfp: float,
        pfn: float,
        ptp: float,
    ) -> float: ...

    # I=float, P=np.ndarray → ndarray
    @overload
    @staticmethod
    def _compute(
        *,
        itn: float,
        ifp: float,
        ifn: float,
        itp: float,
        ptn: np.ndarray,
        pfp: np.ndarray,
        pfn: np.ndarray,
        ptp: np.ndarray,
    ) -> np.ndarray: ...

    # I=np.ndarray, P=float → ndarray
    @overload
    @staticmethod
    def _compute(
        *,
        itn: np.ndarray,
        ifp: np.ndarray,
        ifn: np.ndarray,
        itp: np.ndarray,
        ptn: float,
        pfp: float,
        pfn: float,
        ptp: float,
    ) -> np.ndarray: ...

    # I=np.ndarray, P=np.ndarray → ndarray
    @overload
    @staticmethod
    def _compute(
        *,
        itn: np.ndarray,
        ifp: np.ndarray,
        ifn: np.ndarray,
        itp: np.ndarray,
        ptn: np.ndarray,
        pfp: np.ndarray,
        pfn: np.ndarray,
        ptp: np.ndarray,
    ) -> np.ndarray: ...

    @staticmethod
    def _compute(
        importance: Importance | list[Importance] | np.ndarray | None = None,
        performance: TwoClassClassificationPerformance
        | FiniteSetOfTwoClassClassificationPerformances
        | np.ndarray
        | None = None,
        itn: float | np.ndarray | None = None,
        ifp: float | np.ndarray | None = None,
        ifn: float | np.ndarray | None = None,
        itp: float | np.ndarray | None = None,
        ptn: float | np.ndarray | None = None,
        pfp: float | np.ndarray | None = None,
        pfn: float | np.ndarray | None = None,
        ptp: float | np.ndarray | None = None,
    ):
        itn, ifp, ifn, itp = _parse_importance(
            importance=importance, itn=itn, ifp=ifp, ifn=ifn, itp=itp
        )
        ptn, pfp, pfn, ptp = _parse_performance(
            performance=performance, ptn=ptn, pfp=pfp, pfn=pfn, ptp=ptp
        )
        satisfying = ptn * itn + ptp * itp
        unsatisfying = pfp * ifp + pfn * ifn
        if (
            isinstance(satisfying, float)
            and satisfying == 0.0
            and isinstance(unsatisfying, float)
            and unsatisfying == 0.0
        ):
            return math.nan
        else:
            with np.errstate(invalid="ignore"):
                return satisfying / (satisfying + unsatisfying)

    def __call__(self, performance: TwoClassClassificationPerformance) -> float:
        if self._constraint and not self._constraint(performance):
            logging.warning(
                f"Performance {performance} does not satisfy the constraint of "
                f"the ranking score {self.name}"
            )
        return cast(
            float,
            RankingScore._compute(
                itn=self._importance.itn,
                ifp=self._importance.ifp,
                ifn=self._importance.ifn,
                itp=self._importance.itp,
                ptn=performance.ptn,
                pfp=performance.pfp,
                pfn=performance.pfn,
                ptp=performance.ptp,
            ),
        )

    @staticmethod
    def getTrueNegativeRate() -> "RankingScore":
        """
        True Negative Rate (TNR).

        .. math::
            TNR = P(\\{tn\\} | \\{tn, fp\\}) = P(S=1 | Y=c_-)

        This score is a particular case of canonical ranking score with the importance
        proportional to

        * :math:`I(tn)=1`,
        * :math:`I(fp)=1`,
        * :math:`I(fn)=0`,
        * and :math:`I(tp)=0`
        (see :cite:t:`Pierard2025Foundations`, Section A.7.3).

        The behavior of this score, in ROC, is as follows.

        .. image:: /figures/TrueNegativeRate_in_ROC.svg

        Synonyms: specificity, selectivity, inverse recall.

        Returns:
            RankingScore: the score as a RankingScore object
        """
        # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        importance = Importance(itn=1, ifp=1, ifn=0, itp=0)
        name = "True Negative Rate"
        abbreviation = "TNR"
        return RankingScore(importance, name=name, abbreviation=abbreviation)

    @staticmethod
    def getSpecificity() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getTrueNegativeRate`.
        """
        rs = RankingScore.getTrueNegativeRate()
        rs.rename("Specificity", "Sp")
        return rs

    @staticmethod
    def getSelectivity() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getTrueNegativeRate`.
        """
        rs = RankingScore.getTrueNegativeRate()
        rs.rename("Selectivity")
        return rs

    @staticmethod
    def getInverseRecall() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getTrueNegativeRate`.
        """
        rs = RankingScore.getTrueNegativeRate()
        rs.rename("Inverse Recall", "Re-Inv")
        return rs

    @staticmethod
    def getTruePositiveRate() -> "RankingScore":
        """
        True Positive Rate (TPR).

        .. math::
            TPR = P(\\{tp\\} | \\{fn, tp\\}) = P(S=1 | Y=c_+)

        This score is a particular case of canonical ranking score with the importance
        proportional to

        * :math:`I(tn)=0`,
        * :math:`I(fp)=0`,
        * :math:`I(fn)=1`,
        and :math:`I(tp)=1`
        (see :cite:t:`Pierard2025Foundations`, Section A.7.3).

        The behavior of this score, in ROC, is as follows.

        .. image:: /figures/TruePositiveRate_in_ROC.svg

        Synonyms: sensitivity, recall.

        Returns:
            RankingScore: the score as a RankingScore object
        """
        # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        importance = Importance(itn=0, ifp=0, ifn=1, itp=1)
        name = "True Positive Rate"
        abbreviation = "TPR"
        return RankingScore(importance, name=name, abbreviation=abbreviation)

    @staticmethod
    def getSensitivity() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getTruePositiveRate`.
        """
        rs = RankingScore.getTruePositiveRate()
        rs.rename("Sensitivity")
        return rs

    @staticmethod
    def getRecall() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getTruePositiveRate`.
        """
        rs = RankingScore.getTruePositiveRate()
        rs.rename("Recall", "Re")
        return rs

    @staticmethod
    def getNegativePredictiveValue() -> "RankingScore":
        """
        Negative Predictive Value (NPV).

        .. math::
            NPV = P(\\{tn\\} | \\{tn, fn\\}) = P(S=1 | \\hat{Y}=c_-)

        This score is a particular case of canonical ranking score with the importance
        proportional to

        * :math:`I(tn)=1`,
        * :math:`I(fp)=0`,
        * :math:`I(fn)=1`,
        * and :math:`I(tp)=0`
        (see :cite:t:`Pierard2025Foundations`, Section A.7.3).

        The behavior of this score, in ROC, is as follows.

        .. image:: /figures/NegativePredictiveValue_in_ROC.svg

        Synonym: inverse precision

        Returns:
            RankingScore: the score as a RankingScore object
        """
        # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        importance = Importance(itn=1, ifp=0, ifn=1, itp=0)
        name = "Negative Predictive Value"
        abbreviation = "NPV"
        return RankingScore(importance, name=name, abbreviation=abbreviation)

    @staticmethod
    def getInversePrecision() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getNegativePredictiveValue`.
        """
        rs = RankingScore.getNegativePredictiveValue()
        rs.rename("Inverse Precision", "Pr-Inv")
        return rs

    @staticmethod
    def getPositivePredictiveValue() -> "RankingScore":
        """
        Positive Predictive Value (PPV).

        .. math::
            PPV = P(\\{tp\\} | \\{fp, tp\\}) = P(S=1 | \\hat{Y}=c_+)

        This score is a particular case of canonical ranking score with the importance
        proportional to

        * :math:`I(tn)=0`,
        * :math:`I(fp)=1`,
        * :math:`I(fn)=0`,
        * and :math:`I(tp)=1`
        (see :cite:t:`Pierard2025Foundations`, Section A.7.3).

        The behavior of this score, in ROC, is as follows.

        .. image:: /figures/PositivePredictiveValue_in_ROC.svg

        Synonym: precision

        Returns:
            RankingScore: the score as a RankingScore object
        """
        # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        importance = Importance(itn=0, ifp=1, ifn=0, itp=1)
        name = "Positive Predictive Value"
        abbreviation = "PPV"
        return RankingScore(importance, name=name, abbreviation=abbreviation)

    @staticmethod
    def getPrecision() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getPositivePredictiveValue`.
        """
        rs = RankingScore.getPositivePredictiveValue()
        rs.rename("Precision", "Pr")
        return rs

    @staticmethod
    def getIntersectionOverUnion() -> "RankingScore":
        """
        Intersection over Union (IoU).

        .. math::
            IoU = P(\\{tp\\} | \\{fp, fn, tp\\}) = P(S=1 | Y=c_+ \\vee \\hat{Y}=c_+)

        This score is a particular case of (non-canonical) ranking score with the importance
        proportional to

        * :math:`I(tn)=0`,
        * :math:`I(fp)=1`,
        * :math:`I(fn)=1`,
        * and :math:`I(tp)=1`.

        The behavior of this score, in ROC, is as follows.

        .. image:: /figures/IntersectionOverUnion_in_ROC.svg

        Synonyms: Jaccard index, Jaccard similarity coefficient, Tanimoto coefficient, similarity, critical success index (CSI), threat score.

        Returns:
            RankingScore: the score as a RankingScore object
        """
        importance = Importance(itn=0, ifp=1, ifn=1, itp=1)
        name = "Intersection over Union"
        abbreviation = "IoU"
        return RankingScore(importance, name=name, abbreviation=abbreviation)

    @staticmethod
    def getJaccard() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getIntersectionOverUnion`.
        """
        rs = RankingScore.getIntersectionOverUnion()
        rs.rename("Jaccard", "J")
        return rs

    @staticmethod
    def getTanimotoCoefficient() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getIntersectionOverUnion`.
        """
        rs = RankingScore.getIntersectionOverUnion()
        rs.rename("Tanimoto Coefficient", "TC")
        return rs

    @staticmethod
    def getSimilarity() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getIntersectionOverUnion`.
        """
        rs = RankingScore.getIntersectionOverUnion()
        rs.rename("Similarity")
        return rs

    @staticmethod
    def getCriticalSuccessIndex() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getIntersectionOverUnion`.
        """
        rs = RankingScore.getIntersectionOverUnion()
        rs.rename("Critical Success Index", "CSI")
        return rs

    @staticmethod
    def getThreatScore() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getIntersectionOverUnion`.
        """
        rs = RankingScore.getIntersectionOverUnion()
        rs.rename("Threat Score")
        return rs

    @staticmethod
    def getInverseIntersectionOverUnion() -> "RankingScore":
        """
        Inverse Intersection over Union (IoU).

        .. math::
            IoU-Inv = P(\\{tn\\} | \\{tn, fp, fn\\}) = P(S=1 | Y=c_- \\vee \\hat{Y}=c_-)

        This score is a particular case of (non-canonical) ranking score with the importance
        proportional to

        * :math:`I(tn)=1`,
        * :math:`I(fp)=1`,
        * :math:`I(fn)=1`,
        * and :math:`I(tp)=0`.

        The behavior of this score, in ROC, is as follows.

        .. image:: /figures/InverseIntersectionOverUnion_in_ROC.svg

        Synonyms: inverse Jaccard index, inverse Jaccard similarity coefficient, inverse Tanimoto coefficient, inverse similarity, inverse critical success index, inverse threat score.

        Returns:
            RankingScore: the score as a RankingScore object
        """
        importance = Importance(itn=1, ifp=1, ifn=1, itp=0)
        name = "Inverse Intersection over Union"
        abbreviation = "IoU-Inv"
        return RankingScore(importance, name=name, abbreviation=abbreviation)

    @staticmethod
    def getInverseJaccard() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getInverseIntersectionOverUnion`.
        """
        rs = RankingScore.getInverseIntersectionOverUnion()
        rs.rename("Inverse Jaccard", "J-Inv")
        return rs

    @staticmethod
    def getF(beta=1.0) -> "RankingScore":
        """
        The F-score. See https://en.wikipedia.org/wiki/F-score

        .. math::
            F_\\beta = \\frac{ (1+\\beta^2) P(\\{tp\\} }{ 1 P(\\{fp\\} + \\beta^2 P(\\{fn\\} + (1+\\beta^2) P(\\{tp\\} }

        This score is a particular case of canonical ranking score with the importance
        proportional to

        * :math:`I(tn)=0`,
        * :math:`I(fp)=1`,
        * :math:`I(fn)=beta**2`,
        * and :math:`I(tp)=1 + beta**2`.

        Args:
            beta (float, optional): :math:`\\beta \\ge 0`. Defaults to 1.0.

        Returns:
            RankingScore: the score as a RankingScore object
        """
        if not isinstance(beta, float):
            raise ValueError(f"beta must be a real number, got {beta}")
        if math.isnan(beta) or beta < 0:
            raise ValueError(f"beta must be positive, got {beta}")
        # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        if math.isinf(beta):
            itn = 0
            ifp = 0
            ifn = 1
            itp = 1
            importance = Importance(itn=itn, ifp=ifp, ifn=ifn, itp=itp)
            name = "F-score for β=∞"
            abbreviation = "F∞"
            symbol = "$F_{\\infty}$"
        else:
            itn = 0
            ifp = 1
            ifn = beta**2
            itp = 1 + beta**2
            importance = Importance(itn=itn, ifp=ifp, ifn=ifn, itp=itp)
            name = "F-score for β={:g}".format(beta)
            abbreviation = "F{:g}".format(beta)
            symbol = "$F_{" + "{:g}".format(beta) + "}$"
        return RankingScore(
            importance, name=name, abbreviation=abbreviation, symbol=symbol
        )

    @staticmethod
    def getDiceSorensenCoefficient() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getF` with :math:`\\beta=1`.
        """
        rs = RankingScore.getF(beta=1.0)
        rs.rename("Dice-Sørensen coefficient", "DSC")
        return rs

    @staticmethod
    def getZijdenbosSimilarityIndex() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getF` with :math:`\\beta=1`.
        """
        rs = RankingScore.getF(beta=1.0)
        rs.rename("Zijdenbos Similarity Index", "ZSI")
        return rs

    @staticmethod
    def getCzekanowskiBinaryIndex() -> "RankingScore":
        """
        See :meth:`sorbetto.ranking.RankingScore.getF` with :math:`\\beta=1`.
        """
        rs = RankingScore.getF(beta=1.0)
        rs.rename("Czekanowski Binary Index", "CBI")
        return rs

    @staticmethod
    def getInverseF(beta=1.0) -> "RankingScore":
        """
        The inverse F-score.

        .. math::
            F_\\beta-inv = \\frac{ (1+\\beta^2) P(\\{tn\\} }{ 1 P(\\{fn\\} + \\beta^2 P(\\{fp\\} + (1+\\beta^2) P(\\{tn\\} }

        This score is a particular case of canonical ranking score with the importance
        proportional to

        * :math:`I(tn)=1 + beta**2`,
        * :math:`I(fp)=beta**2`,
        * :math:`I(fn)=1`,
        * and :math:`I(tp)=0`.

        Args:
            beta (float, optional): :math:`\\beta`. Defaults to 1.0.

        Returns:
            RankingScore: the score as a RankingScore object
        """
        if not isinstance(beta, float):
            raise ValueError(f"beta must be a real number, got {beta}")
        if math.isnan(beta) or beta < 0:
            raise ValueError(f"beta must be positive, got {beta}")

        if math.isinf(beta):
            itn = 1
            ifp = 1
            ifn = 0
            itp = 0
            importance = Importance(itn=itn, ifp=ifp, ifn=ifn, itp=itp)
            name = "Inverse F-score for β=∞"
            abbreviation = "F∞-Inv"
            symbol = "$F_{\\infty}$-Inv"
        else:
            itn = 1 + beta**2
            ifp = beta**2
            ifn = 1
            itp = 0
            importance = Importance(itn=itn, ifp=ifp, ifn=ifn, itp=itp)
            name = "Inverse F-score for β={:g}".format(beta)
            abbreviation = "F{:g}-Inv".format(beta)
            symbol = "$F_{" + "{:g}".format(beta) + "}$-Inv"
        return RankingScore(
            importance, name=name, abbreviation=abbreviation, symbol=symbol
        )

    @staticmethod
    def getAccuracy() -> "RankingScore":
        """
        Accuracy (A).

        .. math::
            A = P(\\{tn, tp\\}) = P(S=1)

        This score is a particular case of canonical ranking score with the importance
        proportional to

        * :math:`I(tn)=1`,
        * :math:`I(fp)=1`,
        * :math:`I(fn)=1`,
        * and :math:`I(tp)=1` (see :cite:t:`Pierard2025Foundations`, Section A.7.3).

        The behavior of this score, in ROC, is as follows.

        .. image:: /figures/Accuracy_in_ROC.svg

        Returns:
            RankingScore: the score as a RankingScore object
        """
        # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        importance = Importance(itn=1, ifp=1, ifn=1, itp=1)
        name = "Accuracy"
        abbreviation = "A"
        return RankingScore(importance, name=name, abbreviation=abbreviation)

    # @staticmethod
    # def getMatchingCoefficient() -> "RankingScore":
    #     # SimpleMatchingCoefficient ??? Same as Jaccard ???
    #     rs = RankingScore.getAccuracy()
    #     rs.rename("MC")
    #     return rs

    # WARNING: In Flach2003TheGeometry, the skew-insensitive version has been
    # established only for beta=1. We could do it also for any beta, but in
    # that case, it is not anymore ( 2 TPR ) / ( TPR + FPR + 1 ), and not
    # anymore a score introduced in cite:t:`Flach2003TheGeometry`. So,
    # for now, we implement only the beta=1 case.
    @staticmethod
    def getSkewInsensitiveVersionOfF1(priorPos: float) -> "RankingScore":
        """
        The skew-insensitive version of :math:`F_1`,
        defined in cite:t:`Flach2003TheGeometry`.

        .. math::
            SIVF = \\frac{ 2 TPR }{ TPR + FPR + 1 }
        This score is clearly undefined when one of the class priors is zero,
        as in this case either FPR or TPR is undefined.

        When used on performances with the class priors, for the negative and positive
        classes of :math:`P(Y=c_-)=\\pi_-` and :math:`P(Y=c_+)=\\pi_+`, respectively,
        this score becomes a particular case of (non-canonical) ranking score with the
        importance proportional to

        * :math:`I(tn)=0`,
        * :math:`I(fp)=\\pi_+`,
        * :math:`I(fn)=\\pi_-`,
        * and :math:`I(tp)=2 \\pi_-`.

        Args:
            priorPos (float): The prior of the positive class, :math:`\\pi_+\\in(0,1)`.

        Returns:
            RankingScore: the score as a RankingScore object that can be used only
              on performances satisfying the constraint of fixed priors.
        """
        # The argument `priorPos` is checked in the constructor of the constraint.
        constraint = ConstraintFixedClassPriors(priorPos=priorPos)
        # But the check performed over there allows priors to be zero.
        # So we need more checks.
        priorNeg = 1.0 - priorPos
        assert priorNeg != 0.0
        assert priorPos != 0.0

        # SIVF = ( 2 TPR ) / ( TPR + FPR + 1 )
        #      = ( 2 TPR ) / ( FPR + FNR + 2 TPR )
        #      = ( 2 PTP/priorPos ) / ( PFP/priorNeg + PFN/priorPos + 2 PTP/priorPos )
        #      = ( 2 PTP*priorNeg ) / ( PFP*priorPos + PFN*priorNeg + 2 PTP*priorNeg )

        itn = 0.0
        ifp = priorPos
        ifn = priorNeg
        itp = 2.0 * priorNeg
        importance = Importance(itn=itn, ifp=ifp, ifn=ifn, itp=itp)
        name = "Skew-Insensitive Version of F"
        abbreviation = "SIVF"
        return RankingScore(
            importance, constraint=constraint, name=name, abbreviation=abbreviation
        )

    @staticmethod
    def getMacroAveragedRecall(
        priorPos: float, weightClassPos: float = 0.5
    ) -> "RankingScore":
        """
        The macro-averaged recall, with a weighted arithmetic mean, is defined as

        .. math::
            m-Re = \\lambda_- Re_- + \\lambda_+ Re_+
        where :math:`Re_-` is the recall of the negative class (:math:`Re_- = TNR`),
        :math:`Re_+` is the recall of the positive class (:math:`Re_+ = TPR`),
        and :math:`(\\lambda_-, \\lambda_+)` are the class weights such that
        :math:`\\lambda_- \\ge 0`, :math:`\\lambda_+ \\ge 0`, :math:`\\lambda_- + \\lambda_+ = 1`.
        This score is clearly undefined when one of the class priors is zero,
        as in this case either :math:`Re_-` or :math:`Re_+` is undefined.

        When used on performances with the class priors, for the negative and positive
        classes of :math:`P(Y=c_-)=\\pi_-` and :math:`P(Y=c_+)=\\pi_+`, respectively,
        this score becomes a particular case of canonical ranking score with the
        importance proportional to

        * :math:`I(tn) = I(fp) = \\frac{ \\lambda_- }{ \\pi_- }`
        * and :math:`I(fn) = I(tp) = \\frac{ \\lambda_+ }{ \\pi_+ }`.

        Args:
            priorPos (float): The prior of the positive class, :math:`\\pi_+\\in(0,1)`.
            weightClassPos (float, optional): The weight for the positive class, :math:`\\lambda_+\\in[0,1]`. Defaults to 0.5.

        Returns:
            RankingScore: the score as a RankingScore object that can be used only
              on performances satisfying the constraint of fixed priors.
        """
        # The argument `priorPos` is checked in the constructor of the constraint.
        constraint = ConstraintFixedClassPriors(priorPos=priorPos)
        # But the check performed over there allows priors to be zero.
        # So we need more checks.
        priorNeg = 1.0 - priorPos
        assert priorNeg != 0.0
        assert priorPos != 0.0

        assert isinstance(weightClassPos, float)
        assert weightClassPos >= 0.0
        assert weightClassPos <= 1.0
        weightClassNeg = 1.0 - weightClassPos

        # macroRecall
        #    = wNeg TNR + wPos TPR
        #    = wNeg PTN/priorNeg + wPos PTP/priorPos
        #    = (wNeg/priorNeg) PTN + (wPos/priorPos) PTP
        #    = [ (wNeg/priorNeg) PTN + (wPos/priorPos) PTP ] / [ wNeg + wPos ]
        #    = [ (wNeg/priorNeg) PTN + (wPos/priorPos) PTP ] / [ wNeg (PTN+PFP)/priorNeg + wPos (PFN+PTP)/priorPos ]
        #    = [ (wNeg/priorNeg) PTN + (wPos/priorPos) PTP ] / [ (wNeg/priorNeg) PTN + (wNeg/priorNeg) PFP + (wPos/priorPos) PFN + (wPos/priorPos) PTP ]

        itn = ifp = weightClassNeg / priorNeg
        ifn = itp = weightClassPos / priorPos
        importance = Importance(itn=itn, ifp=ifp, ifn=ifn, itp=itp)
        if weightClassPos == 0.5:
            name = "Arithmetically Macro-Averaged Recall"
            abbreviation = "m-Re"
        else:
            name = "{:g} Re_- + {:g} Re_+".format(weightClassNeg, weightClassPos)
            abbreviation = "wm-Re"
        return RankingScore(
            importance, constraint=constraint, name=name, abbreviation=abbreviation
        )

    @staticmethod
    def getWeightedAccuracy(priorPos: float, weightClassPos: float) -> "RankingScore":
        """
        The weighted accuracy is defined as

        .. math::
            WA = \\lambda_- TNR + \\lambda_+ TPR
        with :math:`\\lambda_- \\ge 0`, :math:`\\lambda_+ \\ge 0`, :math:`\\lambda_- + \\lambda_+ = 1`.
        This score is clearly undefined when one of the class priors is zero,
        as in this case either TNR or TPR is undefined.

        When used on performances with the class priors, for the negative and positive
        classes of :math:`P(Y=c_-)=\\pi_-` and :math:`P(Y=c_+)=\\pi_+`, respectively,
        this score becomes a particular case of canonical ranking score with the
        importance proportional to

        * :math:`I(tn) = I(fp) = \\frac{ \\lambda_- }{ \\pi_- }`
        * and :math:`I(fn) = I(tp) = \\frac{ \\lambda_+ }{ \\pi_+ }`.
        See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.4.

        Args:
            priorPos (float): The prior of the positive class, :math:`\\pi_+\\in(0,1)`.
            weightClassPos (float): The weight for the positive class, :math:`\\lambda_+\\in[0,1]`.

        Returns:
            RankingScore: the score as a RankingScore object that can be used only
              on performances satisfying the constraint of fixed priors.
        """
        rs = RankingScore.getMacroAveragedRecall(priorPos, weightClassPos)
        if weightClassPos == priorPos:
            name = "Accuracy"
            abbreviation = "A"
        else:
            name = "Weighted Accuracy ({:g})".format(weightClassPos)
            abbreviation = "WA"
        rs.rename(name, abbreviation)
        return rs

    @staticmethod
    def getBalancedAccuracy(priorPos: float) -> "RankingScore":
        """
        The balanced accuracy (:math:`BA`).

        .. math::
            BA = \\frac12 TNR + \\frac12 TPR

        See :meth:`sorbetto.ranking.RankingScore.getMacroAveragedRecall`

        Args:
            priorPos (float): The prior of the positive class, :math:`\\pi_+\\in(0,1)`.

        Returns:
            RankingScore: the score as a RankingScore object that can be used only
              on performances satisfying the constraint of fixed priors.
        """
        # See :cite:t:`Pierard2025Foundations`, Section A.7.4
        rs = RankingScore.getMacroAveragedRecall(priorPos, weightClassPos=0.5)
        if priorPos == 0.5:
            name = "Accuracy"
            abbreviation = "A"
        else:
            name = "Balanced Accuracy"
            abbreviation = "BA"
        rs.rename(name, abbreviation)
        return rs

    @staticmethod
    def getMacroAveragedPrecision(
        ratePos: float, weightClassPos: float = 0.5
    ) -> "RankingScore":
        """
        The macro-averaged precision, with a weighted arithmetic mean, is defined as

        .. math::
            m-Pr = \\lambda_- Pr_- + \\lambda_+ Pr_+
        where :math:`Pr_-` is the precision of the negative class (:math:`Pr_- = NPV`),
        :math:`Pr_+` is the precision of the positive class (:math:`Pr_+ = PPV`),
        and :math:`(\\lambda_-, \\lambda_+)` are the class weights such that
        :math:`\\lambda_- \\ge 0`, :math:`\\lambda_+ \\ge 0`, :math:`\\lambda_- + \\lambda_+ = 1`.
        This score is clearly undefined when one of the class prediction rates is zero,
        as in this case either :math:`Pr_-` or :math:`Pr_+` is undefined.

        When used on performances with the class prediction rates, for the negative and positive
        classes of :math:`P(\\hat{Y}=c_-)=\\tau_-` and :math:`P(\\hat{Y}=c_+)=\\tau_+`, respectively,
        this score becomes a particular case of canonical ranking score with the
        importance proportional to

        * :math:`I(tn) = I(fn) = \\frac{ \\lambda_- }{ \\tau_- }`
        * and :math:`I(fp) = I(tp) = \\frac{ \\lambda_+ }{ \\tau_+ }`.

        Args:
            ratePos (float): The prediction rate of the positive class, :math:`\\tau_+\\in(0,1)`.
            weightClassPos (float, optional): The weight for the positive class, :math:`\\lambda_+\\in[0,1]`. Defaults to 0.5.

        Returns:
            RankingScore: the score as a RankingScore object that can be used only
              on performances satisfying the constraint of fixed prediction rates.
        """
        # The argument `ratePos` is checked in the constructor of the constraint.
        constraint = ConstraintFixedPredictionRates(ratePos=ratePos)
        # But the check performed over there allows prediction rates to be zero.
        # So we need more checks.
        rateNeg = 1.0 - ratePos
        assert rateNeg != 0.0
        assert ratePos != 0.0

        assert isinstance(weightClassPos, float)
        assert weightClassPos >= 0.0
        assert weightClassPos <= 1.0
        weightClassNeg = 1.0 - weightClassPos

        # macroPrecision
        #    = wNeg NPV + wPos PPV
        #    = wNeg PTN/rateNeg + wPos PTP/ratePos
        #    = (wNeg/rateNeg) PTN + (wPos/ratePos) PTP
        #    = [ (wNeg/rateNeg) PTN + (wPos/ratePos) PTP ] / [ wNeg + wPos ]
        #    = [ (wNeg/rateNeg) PTN + (wPos/ratePos) PTP ] / [ wNeg (PTN+PFN)/rateNeg + wPos (PFP+PTP)/ratePos ]
        #    = [ (wNeg/rateNeg) PTN + (wPos/ratePos) PTP ] / [ (wNeg/rateNeg) PTN + (wPos/ratePos) PFP + (wNeg/rateNeg) PFN + (wPos/ratePos) PTP ]

        itn = ifn = weightClassNeg / rateNeg
        ifp = itp = weightClassPos / ratePos
        importance = Importance(itn=itn, ifp=ifp, ifn=ifn, itp=itp)
        if weightClassPos == 0.5:
            name = "Arithmetically Macro-Averaged Precision"
            abbreviation = "m-Pr"
        else:
            name = "{:g} Pr_- + {:g} Pr_+".format(weightClassNeg, weightClassPos)
            abbreviation = "wm-Pr"
        return RankingScore(
            importance, constraint=constraint, name=name, abbreviation=abbreviation
        )

    def __str__(self) -> str:
        return (
            f"Ranking Score: {self.longLabel} with importance {str(self._importance)}"
        )

    def __eq__(self, other):
        """
        Two ranking scores are equal if and only if the importance values
        associated to both are proportional.
        """
        if isinstance(other, RankingScore):
            self_itn = self._importance.itn
            self_ifp = self._importance.ifp
            self_ifn = self._importance.ifn
            self_itp = self._importance.itp
            sum = self_itn + self_ifp + self_ifn + self_itp
            self_itn /= sum
            self_ifp /= sum
            self_ifn /= sum
            self_itp /= sum

            other_itn = other._importance.itn
            other_ifp = other._importance.ifp
            other_ifn = other._importance.ifn
            other_itp = other._importance.itp
            sum = other_itn + other_ifp + other_ifn + other_itp
            other_itn /= sum
            other_ifp /= sum
            other_ifn /= sum
            other_itp /= sum

            if not math.isclose(self_itn, other_itn, abs_tol=1e-8):
                return False

            if not math.isclose(self_ifp, other_ifp, abs_tol=1e-8):
                return False

            if not math.isclose(self_ifn, other_ifn, abs_tol=1e-8):
                return False

            if not math.isclose(self_itp, other_itp, abs_tol=1e-8):
                return False

            return True

        else:
            return NotImplemented
