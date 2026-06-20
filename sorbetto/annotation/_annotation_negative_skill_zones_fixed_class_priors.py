# Copyright (c) 2026, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import math
from typing import TYPE_CHECKING

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull

from sorbetto.flavor._best_value_flavor import BestValueFlavor
from sorbetto.flavor._entity_flavor import EntityFlavor
from sorbetto.flavor._ranking_flavor import RankingFlavor
from sorbetto.flavor._value_flavor import ValueFlavor
from sorbetto.flavor._worst_value_flavor import WorstValueFlavor
from sorbetto.parameterization._parameterization_default import ParameterizationDefault
from sorbetto.performance import (
    ConstraintFixedClassPriors,
    ConstraintFixedPredictionRates,
)
from sorbetto.performance._finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.performance._two_class_classification_performance import (
    TwoClassClassificationPerformance,
)
from sorbetto.ranking._constraint_relative_importance_satisfying_unsatisfying import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)

from ._abstract_annotation import AbstractAnnotation

if TYPE_CHECKING:
    from sorbetto.tile import Tile


class AnnotationNegativeSkillZonesFixedClassPriors(AbstractAnnotation):
    def __init__(
        self,
        priorPos: float | ConstraintFixedClassPriors,
        name: str | None = None,
        **plt_kwargs,
    ):
        if isinstance(priorPos, ConstraintFixedClassPriors):
            priorPos = priorPos.getPriorPos()
        assert isinstance(priorPos, float)
        assert priorPos > 0.0
        assert priorPos < 1.0
        self._priorPos = priorPos

        if name is None:
            name = "negative skill zones"
        else:
            if not isinstance(name, str):
                name = str(name)

        # TODO: this class does not handle yet these supplementary arguments.
        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, name)

    @staticmethod
    def _from_a_b_to_itn_ifp_ifn_itp(a, b):
        """
        Getting I_tn, I_fp, I_fn, I_tp from a, b
        I_tn, I_fp, I_fn, I_tp = from_a_b_to_itn_ifp_ifn_itp ( a , b )
        """
        # TODO: it is not logical to have this in an annotation class.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized
        I_tn = 1 - a
        I_fp = 1 - b
        I_fn = b
        I_tp = a
        return I_tn, I_fp, I_fn, I_tp

    @staticmethod
    def _from_itn_ifp_ifn_itp_to_a_b(I_tn, I_fp, I_fn, I_tp):
        """
        Getting a, b from I_tn, I_fp, I_fn, I_tp
        a, b = from_itn_ifp_ifn_itp_to_a_b ( I_tn, I_fp, I_fn, I_tp )
        """
        # TODO: it is not logical to have this in an annotation class.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized
        a = I_tp / (I_tn + I_tp)
        b = I_fn / (I_fp + I_fn)
        return a, b

    @staticmethod
    def _adapt_a_b(old_prior_pos, new_prior_pos, old_a, old_b):
        """
        For any point (old_a,old_b) in the Tile (these coordinates can be numpy matrices
        if we want to handle multiple ones), this function computes the coordinates (new_a, new_b)
        such that, if one applies the target/prior shift operation to all compared perfomances,
        the performance ordering that was in (old_a,old_b) is moved in (new_a, new_b).
        """
        # TODO: it is not logical to have this in an annotation class.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized

        old_I_tn, old_I_fp, old_I_fn, old_I_tp = (
            AnnotationNegativeSkillZonesFixedClassPriors._from_a_b_to_itn_ifp_ifn_itp(
                old_a, old_b
            )
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

        new_a, new_b = (
            AnnotationNegativeSkillZonesFixedClassPriors._from_itn_ifp_ifn_itp_to_a_b(
                new_I_tn, new_I_fp, new_I_fn, new_I_tp
            )
        )

        return new_a, new_b

    @staticmethod
    def _lines_intersection(line1, line2):
        """
        Computes the intersection between the lines:
        a1 x + b1 y + c1 = 0
        a2 x + b2 y + c2 = 0
        Returns (x,y) if there is a unique solution, else (None,None)
        """
        # TODO : This code is not peculiar to this annotation. It is geometric things. Should be moved.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized
        a1, b1, c1, name1 = line1
        a2, b2, c2, name2 = line2
        dx = -c1 * b2 + b1 * c2
        dy = -a1 * c2 + c1 * a2
        d = a1 * b2 - b1 * a2
        try:
            x, y = dx / d, dy / d
            return x, y
        except:  # noqa: E722
            return None, None

    @staticmethod
    def _satisfies_all_inequalities(x, y, *inequalities):
        """
        Returns true if and only if the point (x,y) satisfies all the
        linear inequalities a * x + b * y + c > 0
        """
        # TODO : This code is not peculiar to this annotation. It is geometric things. Should be moved.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized
        for inequality in inequalities:
            a, b, c, name = inequality
            v = a * x + b * y + c
            if v < 0 and not math.isclose(v, 0.0):
                return False
        return True

    @staticmethod
    def _polygon_half_planes_to_vertices(prior_pos, *inequalities):
        """
        Converts the representation of a polygon:
        - from: the intersection of half planes given by inequalities a * x + b * y + c > 0
        - to: a circular path between vertices, that is a matplotlib.patches.Polygon object.
        The input polygon is assumed to be for a positive prior equal to 0.5.
        The output polygon is transformed to correspond to a positive prior equal to prior_pos.
        """
        # TODO : This code is not peculiar to this annotation. It is geometric things. Should be moved.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized
        xs = list()
        ys = list()
        for idx1, inequality1 in enumerate(inequalities):
            for idx2, inequality2 in enumerate(inequalities):
                if idx2 != idx1:
                    x, y = (
                        AnnotationNegativeSkillZonesFixedClassPriors._lines_intersection(
                            inequality1, inequality2
                        )
                    )
                    if x is not None:
                        if AnnotationNegativeSkillZonesFixedClassPriors._satisfies_all_inequalities(
                            x, y, *inequalities
                        ):
                            xs.append(x)
                            ys.append(y)
        xs = np.asarray(xs)
        ys = np.asarray(ys)
        points = np.asarray([xs, ys]).T
        try:
            hull = ConvexHull(points)
        except:  # noqa: E722
            return None
        if math.isclose(prior_pos, 0.5):
            points = points[hull.vertices, :]
            return Polygon(points, fill=False)
        else:
            ll = np.linspace(0, 1, 10000)
            all_x = list()
            all_y = list()
            xs = points[hull.vertices, 0]
            ys = points[hull.vertices, 1]
            n = len(hull.vertices)
            for i in range(n):
                x1, x2 = xs[i], xs[(i + 1) % n]
                y1, y2 = ys[i], ys[(i + 1) % n]
                x = x1 * (1 - ll) + x2 * ll
                y = y1 * (1 - ll) + y2 * ll
                x, y = AnnotationNegativeSkillZonesFixedClassPriors._adapt_a_b(
                    0.5, prior_pos, x, y
                )
                all_x.append(x)
                all_y.append(y)
            all_x = np.concatenate(all_x)
            all_y = np.concatenate(all_y)
            points = np.asarray([all_x, all_y]).T
            return Polygon(points, fill=False)

    @staticmethod
    def _better_or_equivalent_than(list_tnr_tpr_1, list_tnr_tpr_2, prior_pos):
        """
        Computes the area in the Tile where all performances, such that (TNR,TPR) is in the first iterable,
        are better than or equivalent to all performances, such that (TNR,TPR) is in the second iterable.
        Output: a matplotlib.patches.Polygon object.
        """
        # TODO : This code is not peculiar to this annotation. Should be moved.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized (e.g., take FiniteSetOfTwoClassClassificationPerformances in input instead of lists_tnr_tpr)

        inequalities = list()
        # Let's first restrict the area of interest to the Tile.
        inequalities.append([1, 0, 0, "left border"])  # a >= 0
        inequalities.append([-1, 0, 1, "right border"])  # a <= 1 <=> -a+1 >= 0
        inequalities.append([0, 1, 0, "lower border"])  # b >= 0
        inequalities.append([0, -1, 1, "top border"])  # b <= 1 <=> -b+1 >= 0
        # Now, we consider each pair of performances.
        for idx1, tnr_tpr_1 in enumerate(list_tnr_tpr_1):
            for idx2, tnr_tpr_2 in enumerate(list_tnr_tpr_2):
                tnr1, tpr1 = tnr_tpr_1
                tnr2, tpr2 = tnr_tpr_2
                fpr1, fnr1 = 1 - tnr1, 1 - tpr1
                fpr2, fnr2 = 1 - tnr2, 1 - tpr2
                # When the priors are both 0.5, perf1 >= perf2 is a zone of the tile
                # bounded by the following straight line.
                coef_a = fpr1 * fnr2 - fnr1 * fpr2
                coef_b = tpr1 * tnr2 - tnr1 * tpr2
                coef_c = tnr1 - tnr2
                inequalities.append(
                    [coef_a, coef_b, coef_c, "P{} >= P{}".format(idx1, idx2)]
                )
        # Now, we take the correct priors into account.
        return AnnotationNegativeSkillZonesFixedClassPriors._polygon_half_planes_to_vertices(
            prior_pos, *inequalities
        )

    def _show_performance_worse_than_no_skill_on_tile(
        self, ax: Axes, performance: TwoClassClassificationPerformance, color
    ):
        """
        This function is intended to be used with any tile specific to a given entity or performance.
        It hatches two areas on a previously drawn Tile (ax is the axes object of matplotlib):
        - one where the performance is worse than the no-skill classifier predicting always the positive class (/// hatches)
        - one where the performance is worse than the no-skill classifier predicting always the negative class (\\\\\\ hatches)
        """
        # TODO : This code is not peculiar to this annotation. Should be moved.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized

        prior_pos = self._priorPos

        assert isinstance(performance, TwoClassClassificationPerformance)
        tnr = performance._tnr()
        tpr = performance._tpr()
        assert math.fabs(performance._prior_pos() - prior_pos) < 1e-8

        list_tnr_tpr_1 = list()
        list_tnr_tpr_1.append([0, 1])
        list_tnr_tpr_2 = list()
        list_tnr_tpr_2.append([tnr, tpr])
        polygon = (
            AnnotationNegativeSkillZonesFixedClassPriors._better_or_equivalent_than(
                list_tnr_tpr_1, list_tnr_tpr_2, prior_pos
            )
        )
        if polygon is not None:
            area = ax.add_patch(polygon)
            area.set_hatch("///")
            area.set_edgecolor(color)

        list_tnr_tpr_1 = list()
        list_tnr_tpr_1.append([1, 0])
        list_tnr_tpr_2 = list()
        list_tnr_tpr_2.append([tnr, tpr])
        polygon = (
            AnnotationNegativeSkillZonesFixedClassPriors._better_or_equivalent_than(
                list_tnr_tpr_1, list_tnr_tpr_2, prior_pos
            )
        )
        if polygon is not None:
            area = ax.add_patch(polygon)
            area.set_hatch("\\\\\\")
            area.set_edgecolor(color)

    def _show_comparison_state_of_the_art_no_skill(
        self,
        ax: Axes,
        performances: FiniteSetOfTwoClassClassificationPerformances,
        color,
    ):
        """
        This function is intended to be used with the "State-of-the-Art Value Tile"
        It hatches two areas on a previously drawn Tile (ax is the axes object of matplotlib):
        - one where all performances are worse than the no-skill classifier predicting always the positive class (/// hatches)
        - one where all performances are worse than the no-skill classifier predicting always the negative class (\\\\\\ hatches)
        """
        # TODO : This code is not peculiar to this annotation. Should be moved.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized

        prior_pos = self._priorPos

        assert isinstance(performances, FiniteSetOfTwoClassClassificationPerformances)
        all_tnr = performances._ptn / (performances._ptn + performances._pfp)
        all_tpr = performances._ptp / (performances._pfn + performances._ptp)
        assert math.fabs(performances.getMinPriorPos() - prior_pos) < 1e-8
        assert math.fabs(performances.getMaxPriorPos() - prior_pos) < 1e-8

        # all entities are worse than the classifier saying always "c+"

        list_tnr_tpr_1 = list()
        list_tnr_tpr_1.append([0, 1])
        list_tnr_tpr_2 = zip(all_tnr, all_tpr)
        polygon = (
            AnnotationNegativeSkillZonesFixedClassPriors._better_or_equivalent_than(
                list_tnr_tpr_1, list_tnr_tpr_2, prior_pos
            )
        )
        if polygon is not None:
            area = ax.add_patch(polygon)
            area.set_hatch("///")
            area.set_edgecolor(color)

        # all entities are worse than the classifier saying always "c-"

        list_tnr_tpr_1 = list()
        list_tnr_tpr_1.append([1, 0])
        list_tnr_tpr_2 = zip(all_tnr, all_tpr)
        polygon = (
            AnnotationNegativeSkillZonesFixedClassPriors._better_or_equivalent_than(
                list_tnr_tpr_1, list_tnr_tpr_2, prior_pos
            )
        )
        if polygon is not None:
            area = ax.add_patch(polygon)
            area.set_hatch("\\\\\\")
            area.set_edgecolor(color)

    def _show_comparison_baseline_no_skill(
        self,
        ax: Axes,
        performances: FiniteSetOfTwoClassClassificationPerformances,
        color,
    ):
        """
        This function is intended to be used with the "Baseline Value Tile"
        It hatches two areas on a previously drawn Tile (ax is the axes object of matplotlib):
        - one where there exists a performance that is worse than all others (it belongs to the baseline Tile)
        and also worse than the no-skill classifier predicting always the positive class (/// hatches)
        - one where there exists a performance that is worse than all others (it belongs to the baseline Tile)
        and also worse than the no-skill classifier predicting always the negative class (\\\\\\ hatches)
        """
        # TODO : This code is not peculiar to this annotation. Should be moved.
        # TODO: this is a copy-paste from an old project: https://github.com/pierard/performance
        # TODO: should be modernized

        prior_pos = self._priorPos

        assert isinstance(performances, FiniteSetOfTwoClassClassificationPerformances)
        all_tnr = performances._ptn / (performances._ptn + performances._pfp)
        all_tpr = performances._ptp / (performances._pfn + performances._ptp)
        assert math.fabs(performances.getMinPriorPos() - prior_pos) < 1e-8
        assert math.fabs(performances.getMaxPriorPos() - prior_pos) < 1e-8

        num_entities = len(performances)

        for e1 in range(num_entities):
            list_tnr_tpr_1 = list()
            list_tnr_tpr_1.append([0, 1])
            for e2 in range(num_entities):
                if e2 != e1:
                    list_tnr_tpr_1.append([all_tnr[e2], all_tpr[e2]])

            list_tnr_tpr_2 = list()
            list_tnr_tpr_2.append([all_tnr[e1], all_tpr[e1]])

            polygon = (
                AnnotationNegativeSkillZonesFixedClassPriors._better_or_equivalent_than(
                    list_tnr_tpr_1, list_tnr_tpr_2, prior_pos
                )
            )
            if polygon is not None:
                # print ( '(+) Showing polygon for entity', get_entity_pretty_name_stdout ( list_of_entities [ e1 ] ) )
                area = ax.add_patch(polygon)
                area.set_hatch("///")
                area.set_edgecolor(color)
            else:
                pass  # print ( '(+) Nothing to show for entity', get_entity_pretty_name_stdout ( list_of_entities [ e1 ] ) )

            list_tnr_tpr_1 = list()
            list_tnr_tpr_1.append([1, 0])
            for e2 in range(num_entities):
                if e2 != e1:
                    list_tnr_tpr_1.append([all_tnr[e2], all_tpr[e2]])

            list_tnr_tpr_2 = list()
            list_tnr_tpr_2.append([all_tnr[e1], all_tpr[e1]])

            polygon = (
                AnnotationNegativeSkillZonesFixedClassPriors._better_or_equivalent_than(
                    list_tnr_tpr_1, list_tnr_tpr_2, prior_pos
                )
            )
            if polygon is not None:
                # print ( '(-) Showing polygon for entity', get_entity_pretty_name_stdout ( list_of_entities [ e1 ] ) )
                area = ax.add_patch(polygon)
                area.set_hatch("\\\\\\")
                area.set_edgecolor(color)
            else:
                pass  # print ( '(-) Nothing to show for entity', get_entity_pretty_name_stdout ( list_of_entities [ e1 ] ) )

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile import Tile

        assert isinstance(tile, Tile)
        parameterization = tile.parameterization
        if not isinstance(parameterization, ParameterizationDefault):
            # TODO : make this class more generic !
            raise NotImplementedError()

        flavor = tile.flavor
        if flavor is None:
            return  # Nothing to do

        if isinstance(flavor, ValueFlavor):
            performance = flavor.performance
            color = "hotpink"
            self._show_performance_worse_than_no_skill_on_tile(ax, performance, color)
        elif isinstance(flavor, BestValueFlavor):
            performances = flavor.performances
            color = "hotpink"
            self._show_comparison_state_of_the_art_no_skill(ax, performances, color)
        elif isinstance(flavor, WorstValueFlavor):
            performances = flavor.performances
            color = "hotpink"
            self._show_comparison_baseline_no_skill(ax, performances, color)
        elif isinstance(flavor, EntityFlavor):
            performances = flavor.performances
            color = "k"
            if flavor.rank == 1:
                self._show_comparison_state_of_the_art_no_skill(ax, performances, color)
            elif flavor.rank == flavor.nb_entities:
                self._show_comparison_baseline_no_skill(ax, performances, color)
            else:
                # nothing to do / not implemented case ?
                pass
        elif isinstance(flavor, RankingFlavor):
            # performances = flavor.performances
            entity = flavor.entity
            performance = entity.performance
            color = "k"
            self._show_performance_worse_than_no_skill_on_tile(ax, performance, color)
        else:
            raise NotImplementedError()

    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool:
        return True

    def isCompatibleWithConstraintOnClassPriors(
        self, constraint: ConstraintFixedClassPriors
    ) -> bool:
        return True

    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        return True

    def getConstraintOnImportances(
        self,
    ) -> ConstraintRelativeImportanceSatisfyingUnsatisfying | None:
        return None

    def getConstraintOnClassPriors(self) -> ConstraintFixedClassPriors | None:
        return ConstraintFixedClassPriors(self._priorPos)

    def getConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        return None
