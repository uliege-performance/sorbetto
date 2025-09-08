# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
import math

import numpy as np

from sorbetto.flavor.value_flavor import ValueFlavor
from sorbetto.geometry.line import Line
from sorbetto.geometry.pencil_of_lines import PencilOfLines
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.parameterization.parameterization_default import ParameterizationDefault
from sorbetto.performance.two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.ranking.ranking_score import RankingScore
from sorbetto.tile.numeric_tile import NumericTile


def _vut_default_param(ptn, pfp, pfn, ptp):
    def x_log_x(x):
        if x == 0:
            return 0.0
        else:
            return x * np.log(x)

    if ptn + pfp == 0.0:
        return math.nan  # The code below does not compute the right value, perhaps should we use the limit ?
    if pfn + ptp == 0.0:
        return math.nan  # The code below does not compute the right value, perhaps should we use the limit ?
    if ptn + pfn == 0.0:
        return math.nan  # The code below does not compute the right value, perhaps should we use the limit ?
    if ptp + pfp == 0.0:
        return math.nan  # The code below does not compute the right value, perhaps should we use the limit ?

    same_TN_TP = math.isclose(ptn, ptp)
    same_FN_FP = math.isclose(pfn, pfp)
    if same_TN_TP and same_FN_FP:
        return ptn + ptp
    elif same_TN_TP:
        return ptn / (pfn - pfp) * (np.log(ptn + pfn) - np.log(ptn + pfp))
    elif same_FN_FP:
        return 1.0 - pfn / (ptp - ptn) * (np.log(ptp + pfn) - np.log(ptn + pfn))
    else:
        # The analytical solution implemented here is due to Anthony Cioppa; many thanks to him.
        num = (
            (pfn - ptp) * x_log_x(pfn + ptp)
            + (ptn - pfn) * x_log_x(ptn + pfn)
            + (ptp - pfp) * x_log_x(pfp + ptp)
            + (pfp - ptn) * x_log_x(ptn + pfp)
        )
        den = (ptp - pfn) * (pfn - pfp)
        return 0.5 - 0.5 * num / den


class ValueTile(NumericTile):
    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: ValueFlavor,
        name: str = "Value Tile",
        resolution: int = 1001,
        disable_colorbar: bool = False,
    ):
        assert isinstance(parameterization, AbstractParameterization)
        assert isinstance(flavor, ValueFlavor)
        assert isinstance(name, str)
        assert isinstance(resolution, int)
        assert resolution > 0

        super().__init__(
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
            disable_colorbar=disable_colorbar,
        )
        self._performance = self.flavor.performance

    @property
    def flavor(self) -> ValueFlavor:
        # We override the property's getter to ensure the right type of flavor.
        flavor = super().flavor
        assert isinstance(flavor, ValueFlavor)
        return flavor

    @property
    def performance(self) -> TwoClassClassificationPerformance:
        return self._performance

    def getVUT(self) -> float:
        """
        Computes the volume

        See :cite:t:`Pierard2024TheTile-arxiv`, Section 3.1. (with default parameterization)
        """
        if isinstance(self.parameterization, ParameterizationDefault):
            return _vut_default_param(
                self._performance.ptn,
                self._performance.pfp,
                self._performance.pfn,
                self._performance.ptp,
            )
        else:
            raise NotImplementedError(
                "VUT is not implemented for other parameterization for now."
            )

    def getLineForValue(self, value) -> Line:
        if not isinstance(self.parameterization, ParameterizationDefault):
            raise NotImplementedError(
                "VUT is not implemented for other parameterization for now."
            )

        ptn = self._performance.ptn
        pfp = self._performance.pfp
        pfn = self._performance.pfn
        ptp = self._performance.ptp

        # The value taken by the ranking scores is v if and only if
        #     ( itn ptn + itp ptp ) / ( itn ptn + ifp pfp + ifn pfn + itp ptp ) = v
        # <=> ( itn ptn + itp ptp ) - v ( itn ptn + ifp pfp + ifn pfn + itp ptp ) = 0
        # <=> itn ptn(1-v) + ifp pfp(0-v) + ifn pfn(0-v) + itp ptp(1-v) = 0
        # <=> (1-a) ptn(1-v) + (1-b) pfp(0-v) + b pfn(0-v) + a ptp(1-v) = 0
        # <=> a [ (ptp-ptn) (1-v) ] + b [ (pfp-pfn) v ] + [ ptn(1-v) + pfp(0-v) ] = 0

        Ka = (ptp - ptn) * (1.0 - value)
        Kb = (pfp - pfn) * value
        K = ptn * (1.0 - value) + pfp * (0.0 - value)

        name = "Line where the rankings scores take the value {:g} for the performance {}".format(
            value, self._performance
        )
        return Line(Ka, Kb, K, name)

    def getPencil(self) -> PencilOfLines:
        if not isinstance(self.parameterization, ParameterizationDefault):
            raise NotImplementedError(
                "VUT is not implemented for other parameterization for now."
            )

        line_1 = self.getLineForValue(0.0)
        line_2 = self.getLineForValue(1.0)
        pencil = PencilOfLines(
            line_1, line_2, "pencil for performance {}".format(self._performance)
        )
        return pencil

    def minimize(self, precision: float = 1e-6) -> tuple[float, float, float]:
        parameterization = self.parameterization
        if isinstance(parameterization, ParameterizationDefault):
            # With the default parameterization, it has been demonstrated in
            # :cite:t:`Pierard2024TheTile-arxiv` that the values taken by the
            # canonical ranking scores on horizontal and vertical lines
            # correspond to some f-means. So, at the extremities, on has the
            # minimal and maximal values. As a consequence, to find a point
            # of the Tile at which the value is minimal or maximal, it suffices
            # to look at the four corners. This can be generalized to all
            # parameterizations: the value taken by any canonical ranking score
            # is bounded by TNR, TPR, NPV, and PPV.

            best_x = math.nan
            best_y = math.nan
            best_val = math.inf

            def update_for_min(ranking_score):
                x = parameterization.getValueParameter1(ranking_score)
                y = parameterization.getValueParameter2(ranking_score)
                val = ranking_score(self._performance)

                nonlocal best_x
                nonlocal best_y
                nonlocal best_val

                if val < best_val:
                    best_x = x
                    best_y = y
                    best_val = val

            update_for_min(RankingScore.getTrueNegativeRate())
            update_for_min(RankingScore.getTruePositiveRate())
            update_for_min(RankingScore.getNegativePredictiveValue())
            update_for_min(RankingScore.getPositivePredictiveValue())

            return best_x, best_y, best_val

        else:
            return super().minimize(precision)

    def maximize(self, precision: float = 1e-6) -> tuple[float, float, float]:
        parameterization = self.parameterization
        if isinstance(parameterization, ParameterizationDefault):
            # With the default parameterization, it has been demonstrated in
            # :cite:t:`Pierard2024TheTile-arxiv` that the values taken by the
            # canonical ranking scores on horizontal and vertical lines
            # correspond to some f-means. So, at the extremities, on has the
            # minimal and maximal values. As a consequence, to find a point
            # of the Tile at which the value is minimal or maximal, it suffices
            # to look at the four corners. This can be generalized to all
            # parameterizations: the value taken by any canonical ranking score
            # is bounded by TNR, TPR, NPV, and PPV.

            best_x = math.nan
            best_y = math.nan
            best_val = -math.inf

            def update_for_max(ranking_score):
                x = parameterization.getValueParameter1(ranking_score)
                y = parameterization.getValueParameter2(ranking_score)
                val = ranking_score(self._performance)

                nonlocal best_x
                nonlocal best_y
                nonlocal best_val

                if val > best_val:
                    best_x = x
                    best_y = y
                    best_val = val

            update_for_max(RankingScore.getTrueNegativeRate())
            update_for_max(RankingScore.getTruePositiveRate())
            update_for_max(RankingScore.getNegativePredictiveValue())
            update_for_max(RankingScore.getPositivePredictiveValue())

            return best_x, best_y, best_val

        else:
            return super().maximize(precision)

    def getExplanation(self) -> str:
        flavor_name = self.flavor.name
        performance = self.flavor.performance
        performance_name = performance.name
        ptn = performance.ptn
        pfp = performance.pfp
        pfn = performance.pfn
        ptp = performance.ptp

        if performance._prior_pos() < 1e-8:
            # TODO: handle this case properly
            message = (
                "The implementation is not yet fully compatible with this particular case: "
                + " the prior of the positive class is close to zero."
            )
            logging.warning(message)

        if performance._prior_neg() < 1e-8:
            # TODO: handle this case properly
            message = (
                "The implementation is not yet fully compatible with this particular case: "
                + " the prior of the negative class is close to zero."
            )
            logging.warning(message)

        if performance._rate_pos() < 1e-8:
            # TODO: handle this case properly
            message = (
                "The implementation is not yet fully compatible with this particular case: "
                + " the prediction rate for the positive class is close to zero."
            )
            logging.warning(message)

        if performance._rate_neg() < 1e-8:
            # TODO: handle this case properly
            message = (
                "The implementation is not yet fully compatible with this particular case: "
                + " the prediction rate for the negative class is close to zero."
            )
            logging.warning(message)

        parameterization = self.parameterization
        explanation = (
            f"This Tile displays the flavor '{flavor_name}' for the performance"
        )
        explanation += (
            f" '{performance_name}' (probabilities of a true negtive, false positive,"
        )
        explanation += (
            f" false negative, and true positive of, respectively, {ptn}, {pfp},"
        )
        explanation += (
            f" {pfn}, {ptp}), with the parameterization '{parameterization.getName()}'."
        )

        no_horizontal_gradient = math.isclose(ptn, ptp, abs_tol=1e-6)
        no_vertical_gradient = math.isclose(pfp, pfn, abs_tol=1e-6)

        score_tnr = RankingScore.getTrueNegativeRate()
        score_tpr = RankingScore.getTruePositiveRate()
        score_npv = RankingScore.getNegativePredictiveValue()
        score_ppv = RankingScore.getPositivePredictiveValue()
        score_a = RankingScore.getAccuracy()

        value_tnr = score_tnr(performance)
        value_tpr = score_tpr(performance)
        value_npv = score_npv(performance)
        value_ppv = score_ppv(performance)
        value_a = score_a(performance)

        if (not no_horizontal_gradient) or (not no_vertical_gradient):
            # What is inside this "if" statement is correct. But this information is redundant
            # with what is already outputed hereinafter. So let's skip.

            minimized_x, minimized_y, minimized_val = self.minimize()
            maximized_x, maximized_y, maximized_val = self.maximize()
            explanation += f" The value taken by canonical ranking scores is between {minimized_val}"
            explanation += f" and {maximized_val}."

            if isinstance(parameterization, ParameterizationDefault):
                volume_under_tile = _vut_default_param(ptn, pfp, pfn, ptp)
                explanation += " The mean value over the Tile, called 'Volume Under Tile (VUT) with"
                explanation += f" the default parameterization, is equal to {volume_under_tile} (be"
                explanation += " careful as the score VUT cannot be used to rank)."

        # TODO: quels scores minimisent ? Quels sont leurs positions et noms ?
        # TODO: quels scores maximisent ? Quels sont leurs positions et noms ?
        # TODO: y a-t-il un gradient horizontal ? Pourquoi ?
        # TODO: y a-t-il un gradient vertical ? Pourquoi ?
        # TODO: demander aux annotations les explanations de ce qu'elles ont dessiné.
        # TODO: expliquer le pencil.
        # TODO: cas où ptp=ptn et pfp=pfn: tuile constante
        # TODO: cas où pfp=pfn: lignes verticales
        # TODO: cas où ptp=ptn: lignes horizontales
        # TODO: quid du biais ?
        # TODO: quid du classificateur obtenu en inversant les décisions ?

        if no_horizontal_gradient and no_vertical_gradient:
            explanation += (
                " This Tile is constant. This is because it is a very particular case"
            )
            explanation += (
                " in which the probabilities of a true negative and of a true positive"
            )
            explanation += " are equal and the probabilities of a false positive and of a false negative"
            explanation += " are also equal."
            explanation += " In other words, both class priors are equal to 0.5 and the classifier is"
            explanation += " unbiased (the opposite classifier is also unbiased)."
            assert math.isclose(performance._prior_neg(), 0.5, abs_tol=1e-5)
            assert math.isclose(performance._prior_pos(), 0.5, abs_tol=1e-5)
            assert math.isclose(
                performance._prior_neg(), performance._rate_neg(), abs_tol=1e-5
            )
            assert math.isclose(
                performance._prior_pos(), performance._rate_pos(), abs_tol=1e-5
            )
            explanation += (
                f" The value taken by all canonical ranking scores is {value_a}."
            )
            assert math.isclose(value_tnr, value_a, abs_tol=1e-5)
            assert math.isclose(value_tpr, value_a, abs_tol=1e-5)
            assert math.isclose(value_npv, value_a, abs_tol=1e-5)
            assert math.isclose(value_ppv, value_a, abs_tol=1e-5)
        elif no_horizontal_gradient:
            explanation += (
                " This Tile does not show any horizontal variation. This is because"
            )
            explanation += (
                " it is a very particular case in which the probabilities of a "
            )
            explanation += " true negative and of a true positive are equal."
            if pfn > pfp:
                explanation += (
                    " As the probability of a false negative is higher than the"
                )
                explanation += (
                    " probability of a false positive, the value taken by the"
                )
                explanation += " canonical ranking scores"
                assert minimized_y > maximized_y
                explanation += (
                    " is minimized at the top of the Tile, where no importance is"
                )
                explanation += " given to the false positives and"
                explanation += (
                    " is maximized at the bottom of the Tile, where no importance is"
                )
                explanation += " given to the false negatives."
            if pfn < pfp:
                explanation += (
                    " As the probability of a false negative is lower than the"
                )
                explanation += (
                    " probability of a false positive, the value taken by the"
                )
                explanation += " canonical ranking scores"
                assert minimized_y < maximized_y
                explanation += (
                    " is minimized at the bottom of the Tile, where no importance is"
                )
                explanation += " given to the false negatives and"
                explanation += (
                    " is maximized at the top of the Tile, where no importance is"
                )
                explanation += " given to the false positives."
        elif no_vertical_gradient:
            explanation += (
                " This Tile does not show any vertical variation. This is because"
            )
            explanation += (
                " it is a very particular case in which the probabilities of a "
            )
            explanation += " false positive and of a false negative are equal."
            if ptn > ptp:
                explanation += (
                    " As the probability of a true negative is higher than the"
                )
                explanation += " probability of a true positive, the value taken by the"
                explanation += " canonical ranking scores"
                assert minimized_x > maximized_x
                explanation += (
                    " is minimized at the right of the Tile, where no importance is"
                )
                explanation += " given to the true negatives and"
                explanation += (
                    " is maximized at the left of the Tile, where no importance is"
                )
                explanation += " given to the true positives."
            if ptn < ptp:
                explanation += (
                    " As the probability of a true negative is lower than the"
                )
                explanation += " probability of a true positive, the value taken by the"
                explanation += " canonical ranking scores"
                assert minimized_x < maximized_x
                explanation += (
                    " is minimized at the left of the Tile, where no importance is"
                )
                explanation += " given to the true positives and"
                explanation += (
                    " is maximized at the right of the Tile, where no importance is"
                )
                explanation += " given to the true negatives."

        else:
            if isinstance(parameterization, ParameterizationDefault):
                pencil = self.getPencil()
                vertex = pencil.getVertex()
                vertex_x = vertex.x
                vertex_y = vertex.y
                explanation += (
                    f" With the parameterization '{parameterization}', the canonical"
                )
                explanation += (
                    " ranking scores that take any given value are aligned, and these"
                )
                explanation += (
                    f" lines form a pencil whose vertex is located at ({vertex_x},"
                )
                explanation += f" {vertex_y})."

        return explanation
