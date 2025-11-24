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
from sorbetto.ranking.constraint_canonical import ConstraintCanonical
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
        colorbar_mode: str = "default",
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
            colorbar_mode=colorbar_mode,
            base_constraint_on_importances=ConstraintCanonical(),
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
                "`getLineForValue` requires a default parameterization."
            )

        ptn = self._performance.ptn
        pfp = self._performance.pfp
        pfn = self._performance.pfn
        ptp = self._performance.ptp

        # The value taken by the ranking scores is v if and only if
        #     ( itn ptn + itp ptp ) / ( itn ptn + ifp pfp + ifn pfn + itp ptp ) = v
        # <=> ( itn ptn + itp ptp ) - v ( itn ptn + ifp pfp + ifn pfn + itp ptp ) = 0
        # <=> itn ptn(1-v) + ifp pfp(0-v) + ifn pfn(0-v) + itp ptp(1-v) = 0

        # For the default parameterization, we have thus
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
                "`getPencil` requires a default parameterization."
            )

        line_1 = self.getLineForValue(0.0)
        line_2 = self.getLineForValue(1.0)
        pencil = PencilOfLines(
            line_1, line_2, "pencil for performance {}".format(self._performance)
        )
        return pencil

    def minimize(self, precision: float = 1e-6) -> tuple[float, float, float]:
        assert isinstance(precision, float)
        assert precision >= 0.0

        parameterization = self.parameterization

        # With the default parameterization, it has been demonstrated in
        # :cite:t:`Pierard2024TheTile-arxiv` that the values taken by the
        # canonical ranking scores on horizontal and vertical lines
        # correspond to some f-means. So, at the extremities, on has the
        # minimal and maximal values. As a consequence, to find a point
        # of the Tile at which the value is minimal or maximal, it suffices
        # to look at the four corners. This can be generalized to all
        # parameterizations: the value taken by any canonical ranking score
        # is bounded by TNR, TPR, NPV, and PPV.

        # TODO: be sure that this is correct when the value is undefined at some corners!

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

    def maximize(self, precision: float = 1e-6) -> tuple[float, float, float]:
        assert isinstance(precision, float)
        assert precision >= 0.0

        parameterization = self.parameterization

        # With the default parameterization, it has been demonstrated in
        # :cite:t:`Pierard2024TheTile-arxiv` that the values taken by the
        # canonical ranking scores on horizontal and vertical lines
        # correspond to some f-means. So, at the extremities, on has the
        # minimal and maximal values. As a consequence, to find a point
        # of the Tile at which the value is minimal or maximal, it suffices
        # to look at the four corners. This can be generalized to all
        # parameterizations: the value taken by any canonical ranking score
        # is bounded by TNR, TPR, NPV, and PPV.

        # TODO: be sure that this is correct when the value is undefined at some corners!

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
                "The implementation is not yet fully compatible with"
                " this particular case: the prior of the positive class"
                " is close to zero."
            )
            logging.warning(message)

        if performance._prior_neg() < 1e-8:
            # TODO: handle this case properly
            message = (
                "The implementation is not yet fully compatible with "
                "this particular case: the prior of the negative class"
                " is close to zero."
            )
            logging.warning(message)

        if performance._rate_pos() < 1e-8:
            # TODO: handle this case properly
            message = (
                "The implementation is not yet fully compatible with"
                " this particular case: the prediction rate for the positive class"
                " is close to zero."
            )
            logging.warning(message)

        if performance._rate_neg() < 1e-8:
            # TODO: handle this case properly
            message = (
                "The implementation is not yet fully compatible with"
                " this particular case: the prediction rate for the negative class"
                " is close to zero."
            )
            logging.warning(message)

        parameterization = self.parameterization
        min_x, max_x, min_y, max_y = parameterization.getExtent()
        explanation = f"This Tile displays the flavor '{flavor_name}' for the performance '{performance_name}' (probabilities of a true negtive, false positive, false negative, and true positive of, respectively, {ptn}, {pfp}, {pfn}, {ptp}), with the parameterization '{parameterization.getName()}'."

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
            explanation += f" The value taken by canonical ranking scores is between {minimized_val} and {maximized_val}."

            if isinstance(parameterization, ParameterizationDefault):
                volume_under_tile = _vut_default_param(ptn, pfp, pfn, ptp)
                explanation += f" The mean value over the Tile, called 'Volume Under Tile' (VUT) with the default parameterization, is equal to {volume_under_tile} (be careful as the score VUT cannot be used to rank)."

        # TODO: quels scores minimisent ? Quels sont leurs positions et noms ?
        # TODO: quels scores maximisent ? Quels sont leurs positions et noms ?
        # TODO: demander aux annotations les explanations de ce qu'elles ont dessiné.
        # TODO: quid du biais ?
        # TODO: quid du classificateur opposé (inverse?) obtenu en inversant les décisions ?

        if no_horizontal_gradient and no_vertical_gradient:
            explanation += "\nThis Tile is constant. This is because it is a very particular case in which the probabilities of a true negative and of a true positive are equal and the probabilities of a false positive and of a false negative are also equal. In other words, both class priors are equal to 0.5, the classifier is unbiased, and the opposite classifier is also unbiased."
            assert math.isclose(performance._prior_neg(), 0.5, abs_tol=1e-5)
            assert math.isclose(performance._prior_pos(), 0.5, abs_tol=1e-5)
            assert math.isclose(
                performance._prior_neg(), performance._rate_neg(), abs_tol=1e-5
            )
            assert math.isclose(
                performance._prior_pos(), performance._rate_pos(), abs_tol=1e-5
            )
            sentence = f" The value taken by all canonical ranking scores is {value_a}."
            explanation += sentence
            assert math.isclose(value_tnr, value_a, abs_tol=1e-5)
            assert math.isclose(value_tpr, value_a, abs_tol=1e-5)
            assert math.isclose(value_npv, value_a, abs_tol=1e-5)
            assert math.isclose(value_ppv, value_a, abs_tol=1e-5)
        elif no_horizontal_gradient:
            explanation += "\nThis Tile does not show any horizontal variation. This is because it is a very particular case in which the probabilities of a true negative and of a true positive are equal. The opposite classifier is unbiased. However, the classifier is biased."
            if pfn > pfp:
                explanation += "\nAs the probability of a false negative is higher than the probability of a false positive, the value taken by the canonical ranking scores"
                assert minimized_y > maximized_y
                explanation += " is minimized at the top of the Tile, where no importance is given to the false positives and is maximized at the bottom of the Tile, where no importance is given to the false negatives."
            if pfn < pfp:
                explanation += "\nAs the probability of a false negative is lower than the probability of a false positive, the value taken by the canonical ranking scores"
                assert minimized_y < maximized_y
                explanation += " is minimized at the bottom of the Tile, where no importance is given to the false negatives and is maximized at the top of the Tile, where no importance is given to the false positives."
        elif no_vertical_gradient:
            explanation += "\nThis Tile does not show any vertical variation. This is because it is a very particular case in which the probabilities of a false positive and of a false negative are equal. The classifier is unbiased. However, the opposite classifier is biased."
            if ptn > ptp:
                explanation += "\nAs the probability of a true negative is higher than the probability of a true positive, the value taken by the canonical ranking scores"
                assert minimized_x > maximized_x
                explanation += " is minimized at the right of the Tile, where no importance is given to the true negatives and is maximized at the left of the Tile, where no importance is given to the true positives."
            if ptn < ptp:
                explanation += "\nAs the probability of a true negative is lower than the probability of a true positive, the value taken by the canonical ranking scores"
                assert minimized_x < maximized_x
                explanation += " is minimized at the left of the Tile, where no importance is given to the true positives and is maximized at the right of the Tile, where no importance is given to the true negatives."
        else:
            explanation += "\nThere are some horizontal and some vertical variations. This means that both the classifier and its opposite are biased."
            if ptn < ptp:
                assert value_tpr > value_npv
                assert value_ppv > value_tnr
                explanation += " Values of canonical ranking scores increase towards the right of the Tile, which means that the probability of a true negative is lower that the probability of a true positive."
            if ptn > ptp:
                assert value_tpr < value_npv
                assert value_ppv < value_tnr
                explanation += " Values of canonical ranking scores increase towards the left of the Tile, which means that the probability of a true negative is higher that the probability of a true positive."
            if pfp < pfn:
                assert value_tnr > value_npv
                assert value_ppv > value_tpr
                explanation += " Values of canonical ranking scores increase towards the bottom of the Tile, which means that the probability of a false positive is lower that the probability of a false negative."
            if pfp > pfn:
                assert value_tnr < value_npv
                assert value_ppv < value_tpr
                explanation += " Values of canonical ranking scores increase towards the top of the Tile, which means that the probability of a false positive is higher that the probability of a false negative."

            if isinstance(parameterization, ParameterizationDefault):
                pencil = self.getPencil()
                vertex = pencil.getVertex()
                vertex_x = vertex.x
                vertex_y = vertex.y
                explanation += f"\nWith the parameterization '{parameterization}', the canonical ranking scores that take any given value are aligned, and these lines form a pencil whose vertex is located at ({vertex_x}, {vertex_y})."
                if ptn < ptp:
                    assert vertex_x <= min_x
                    explanation += " The fact that the vertex is on the left of the Tile means that the probability of a true negative is lower than the probability of a true positive."
                if ptn > ptp:
                    assert vertex_x >= max_x
                    explanation += " The fact that the vertex is on the right of the Tile means that the probability of a true negative is higher than the probability of a true positive."
                if pfp < pfn:
                    assert vertex_y <= min_y
                    explanation += " The fact that the vertex is below the Tile means that the probability of a false positive is lower than the probability of a false negative."
                if pfp > pfn:
                    assert vertex_y >= max_y
                    explanation += " The fact that the vertex is above the Tile means that the probability of a false positive is higher than the probability of a false negative."
            else:
                # TODO: how can we have an explanation for another parameterization?
                pass

        return explanation
