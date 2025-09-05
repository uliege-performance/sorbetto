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
from sorbetto.tile.numeric_tile import NumericTile


def __vut_default_param(ptn, pfp, pfn, ptp):
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
        return super().flavor  # type: ignore

    @property
    def performance(self) -> TwoClassClassificationPerformance:
        return self._performance

    @performance.setter
    def performance(self, value: TwoClassClassificationPerformance):
        self._performance = value

    def getVUT(self) -> float:
        """
        Computes the volume

        See :cite:t:`Pierard2024TheTile-arxiv`, Section 3.1. (with default parameterization)
        """
        if isinstance(self.parameterization, ParameterizationDefault):
            return __vut_default_param(
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

    def getExplanation(self) -> str:
        return "Explanation for this tile is not implemented yet"
