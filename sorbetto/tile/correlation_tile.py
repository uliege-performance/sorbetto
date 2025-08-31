import math

import numpy as np

from sorbetto.core.entity import Entity
from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.numeric_tile import AbstractNumericTile


class CorrelationTile(AbstractNumericTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        symbolic_flavor: AbstractSymbolicFlavor,
        entities_list: list[Entity],
        resolution: int = 1001,
    ):
        super().__init__(
            name, parameterization, symbolic_flavor, entities_list, resolution
        )

    def minimize(self, precison: float = 1e-8):
        """
        Tries to minimize the value. There is no guarantee to find the minimum with the implemented algorithm.
        As described in Section A.7.2 of the supplementary material for :cite:t:`Pierard2025Foundations`,
        this method implements a custom coarse-to-fine grid-based direct search :cite:t:`Conn2009Introduction`:
        we compute the value on a coarse grid over the Tile, locate the minimum on the grid, center a smaller
        region of interrest and a finer grid around that point, and iterate until the region of interrest
        is small enough.

        Args:
            precison (float, optional): the desired precision for the coordinates of the point on the Tile. Defaults to 1e-8.

        Returns:
            float: the first coordinate of the point on the Tile where the smallest value has been found.
            float: the second coordinate of the point on the Tile where the smallest value has been found.
            float: the smallest value that has been found.
        """

        parameterization = self.parameterization
        flavor = self.flavor

        min_x, max_x = parameterization.getBoundsParameter1()
        min_y, max_y = parameterization.getBoundsParameter2()

        center_x = 0.5 * (min_x + max_x)
        center_y = 0.5 * (min_y + max_y)

        best_x_y_min = [center_x, center_y]  # initial point for the optimization
        best_val_min = math.inf
        scale_x = max_x - min_x
        scale_y = max_y - min_y
        for _ in range(64):
            if precison > scale_x and precison > scale_y:
                break
            scale_x = scale_x * 0.5
            scale_y = scale_y * 0.5
            best_x, best_y = best_x_y_min
            for x in np.linspace(best_x - scale_x, best_x + scale_x, 16):
                if x < min_x or x > max_x:
                    continue
                for y in np.linspace(best_y - scale_y, best_y + scale_y, 16):
                    if y < min_y or y > max_y:
                        continue
                    importance = parameterization.getCanonicalImportance(x, y)
                    val = flavor(importance)
                    if val < best_val_min:
                        best_x_y_min = x, y
                        best_val_min = val

        return best_x_y_min[0], best_x_y_min[1], best_val_min

    def maximize(self, precison: float = 1e-8):
        """
        Tries to maximize the value. There is no guarantee to find the maximum with the implemented algorithm.
        As described in Section A.7.2 of the supplementary material for :cite:t:`Pierard2025Foundations`,
        this method implements a custom coarse-to-fine grid-based direct search :cite:t:`Conn2009Introduction`:
        we compute the value on a coarse grid over the Tile, locate the maximum on the grid, center a smaller
        region of interrest and a finer grid around that point, and iterate until the region of interrest
        is small enough.

        Args:
            precison (float, optional): the desired precision for the coordinates of the point on the Tile. Defaults to 1e-8.

        Returns:
            float: the first coordinate of the point on the Tile where the largest value has been found.
            float: the second coordinate of the point on the Tile where the largest value has been found.
            float: the largest value that has been found.
        """

        parameterization = self.parameterization
        flavor = self.flavor

        min_x, max_x = parameterization.getBoundsParameter1()
        min_y, max_y = parameterization.getBoundsParameter2()

        center_x = 0.5 * (min_x + max_x)
        center_y = 0.5 * (min_y + max_y)

        best_x_y_min = [center_x, center_y]  # initial point for the optimization
        best_val_min = -math.inf
        scale_x = max_x - min_x
        scale_y = max_y - min_y
        for _ in range(64):
            if precison > scale_x and precison > scale_y:
                break
            scale_x = scale_x * 0.5
            scale_y = scale_y * 0.5
            best_x, best_y = best_x_y_min
            for x in np.linspace(best_x - scale_x, best_x + scale_x, 16):
                if x < min_x or x > max_x:
                    continue
                for y in np.linspace(best_y - scale_y, best_y + scale_y, 16):
                    if y < min_y or y > max_y:
                        continue
                    importance = parameterization.getCanonicalImportance(x, y)
                    val = flavor(importance)
                    if val > best_val_min:
                        best_x_y_min = x, y
                        best_val_min = val

        return best_x_y_min[0], best_x_y_min[1], best_val_min
