import math

import numpy as np

from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.geometry.line import Line
from sorbetto.geometry.pencil_of_lines import PencilOfLines
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.parameterization.parameterization_default import ParameterizationDefault
from sorbetto.performance.two_class_classification import (
    TwoClassClassificationPerformance,
)
from sorbetto.tile.asbtract_tile import AbstractTile

# from sorbetto.tile.numeric_tile import AbstractNumericTile


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


class ValueTile(AbstractTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        flavor: AbstractSymbolicFlavor,
        performance: TwoClassClassificationPerformance,
        resolution: int = 1001,
    ):
        self._performance = performance
        super().__init__(
            name=name,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
        )

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

    def asPencil(self) -> PencilOfLines:
        if not isinstance(self.parameterization, ParameterizationDefault):
            raise NotImplementedError(
                "VUT is not implemented for other parameterization for now."
            )

        ptn = self._performance.ptn
        pfp = self._performance.pfp
        pfn = self._performance.pfn
        ptp = self._performance.ptp

        # score = ( itn ptn + itp ptp ) / ( itn ptn + ifp pfp + ifn pfn + itp ptp )
        #       = ( (1-a) ptn + a ptp ) / ( (1-a) ptn + (1-b) pfp + b pfn + a ptp )
        #       = ( (ptp-ptn) a + (ptn) ) / ( (ptp-ptn) a + (pfn-pfp) b + (ptn+pfp) )
        #
        # So, the pencil is
        # lambda_1 ( (ptp-ptn) a + (ptn) ) + lambda_2 ( (ptp-ptn) a + (pfn-pfp) b + (ptn+pfp) ) = 0

        line_1 = Line(ptp - ptn, 0, ptn)
        line_2 = Line(ptp - ptn, pfn - pfp, ptn + pfp)
        pencil = PencilOfLines(
            line_1, line_2, "pencil for score {}".format(self._performance)
        )
        return pencil
