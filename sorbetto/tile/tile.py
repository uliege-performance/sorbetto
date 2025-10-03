# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import io
import logging
from typing import Any, Iterator, SupportsIndex, cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.core.named import Named
from sorbetto.core.types import Extent
from sorbetto.flavor.abstract_flavor import AbstractFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.constraint_fixed_class_priors import (
    ConstraintFixedClassPriors,
)
from sorbetto.performance.constraint_fixed_prediction_rates import (
    ConstraintFixedPredictionRates,
)
from sorbetto.ranking.constraint_relative_importance_satisfying_unsatisfying import (
    ConstraintRelativeImportanceSatisfyingUnsatisfying,
)


class Tile(Named):
    """
    This is the base class for all Tiles. A Tile is a graphical representation (of what ????) with:
    - a parameterization;
    - a flavor;
    - and some annotations.

    Tiles with the default parameterization are studied in detail in :cite:t:`Pierard2024TheTile-arxiv`.
    Various flavors of Tiles are described in :cite:t:`Halin2024AHitchhikers-arxiv` and :cite:t:`Pierard2025AMethodology`.
    """

    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: AbstractFlavor | None = None,
        name: str = "Tile",
        resolution: int = 1001,
        base_constraint_on_importances: Any = None,
    ):
        """
        Args:
            parameterization (AbstractParameterization): The parameterization to be used for the tile.
            flavor (AbstractFlavor | None, optional): The flavor to use. Defaults to None.
            name (str | None, optional): Name of the tile. Defaults to None.
            resolution (int, optional): Resolution of the tile. Defaults to 1001.
            base_constraint_on_importances (Any, optional): The base (that is the one without any annotation) constraint on the importance values. Defaults to None.

        Raises:
            TypeError: If the types of the arguments are incorrect.
        """

        if not isinstance(parameterization, AbstractParameterization):
            raise TypeError(
                f"parameterization must be an instance of AbstractParameterization, got {type(parameterization)}"
            )
        self._parameterization = parameterization

        if flavor is not None:
            if not isinstance(flavor, AbstractFlavor):
                raise TypeError(
                    f"flavor must be an instance of AbstractFlavor, got {type(flavor)}"
                )
        self._flavor = flavor

        if (not isinstance(resolution, int)) or resolution <= 0:
            raise TypeError(
                f"resolution must be a strictly positive integer, got {resolution!r}"
            )
        self._resolution = resolution

        self._zoom = self._parameterization.getExtent()

        self._mat_value: np.ndarray | None = None
        self._update_grid()

        self._annotations: list[AbstractAnnotation] = list()

        self._base_constraint_on_importances = base_constraint_on_importances

        Named.__init__(self, "unnamed Tile", name)

    @property
    def resolution(self) -> int:
        return self._resolution

    @resolution.setter
    def resolution(self, resolution: int):
        if (not isinstance(resolution, int)) or resolution <= 0:
            raise TypeError(
                f"resolution must be a strictly positive integer, got {resolution!r}"
            )
        self._resolution = resolution
        self._update_grid()

    @property
    def zoom(self) -> Extent:
        return self._zoom

    @zoom.setter
    def zoom(self, zoom: Extent):
        def intersection(extent_1: Extent, extent_2: Extent) -> Extent:
            min_x_1, max_x_1, min_y_1, max_y_1 = extent_1
            assert min_x_1 < max_x_1
            assert min_y_1 < max_y_1
            min_x_2, max_x_2, min_y_2, max_y_2 = extent_2
            assert min_x_2 < max_x_2
            assert min_y_2 < max_y_2
            min_x = max(min_x_1, min_x_2)
            max_x = min(max_x_1, max_x_2)
            min_y = max(min_y_1, min_y_2)
            max_y = min(max_y_1, max_y_2)
            assert min_x < max_x
            assert min_y < max_y
            return (min_x, max_x, min_y, max_y)

        assert isinstance(zoom, tuple)
        assert len(zoom) == 4
        assert all(isinstance(v, float) for v in zoom)
        extent = self._parameterization.getExtent()
        self._zoom = intersection(zoom, extent)

    @property
    def parameterization(self) -> AbstractParameterization:
        return self._parameterization

    @property
    def importances(self):
        return self.parameterization.getCanonicalImportanceVectorized(
            self._mat_x, self._mat_y
        )

    @property
    def flavor(self) -> AbstractFlavor | None:
        return self._flavor

    def _update_grid(self):
        x_min, x_max, y_min, y_max = self._zoom
        assert x_min < x_max
        assert y_min < y_max
        vec_x = np.linspace(x_min, x_max, self.resolution)
        self._vec_x = vec_x
        vec_y = np.linspace(y_min, y_max, self.resolution)
        self._vec_y = vec_y
        self._mat_x, self._mat_y = np.meshgrid(vec_x, vec_y, indexing="xy")
        self._mat_value = None

    @property
    def mat_value(self) -> np.ndarray:
        if self._flavor is None:
            tmp = np.empty([self.resolution, self.resolution])
            tmp[:] = np.nan
            return tmp
        if self._mat_value is None:
            self._mat_value = self._compute_mat_value(self._mat_x, self._mat_y)
        return cast(np.ndarray, self._mat_value)

    def _compute_mat_value(
        self,
        param1: list[float] | np.ndarray | None = None,  # TODO: or float ?
        param2: list[float] | np.ndarray | None = None,  # TODO: or float ?
    ):  # uses `flavor ( importances )`.
        if not isinstance(param1, (np.ndarray)):
            param1 = np.array(param1)
        if not isinstance(param2, (np.ndarray)):
            param2 = np.array(param2)

        importance = self.parameterization.getCanonicalImportanceVectorized(
            param1, param2
        )

        if self.flavor is None:
            return np.zeros_like(importance.shape[:-1])

        return self.flavor(importance=importance)

    def __call__(self, param1: np.ndarray, param2: np.ndarray) -> np.ndarray:
        return self._compute_mat_value(param1, param2)

    def genAnnotations(self) -> Iterator[AbstractAnnotation]:  # Generator
        for annotation in self._annotations:
            yield annotation

    def appendAnnotation(self, annotation):
        assert isinstance(annotation, AbstractAnnotation)

        ok = True

        constraint = annotation.getConstraintOnImportances()
        if constraint is not None:
            if not self.isCompatibleWithConstraintOnImportances(constraint):
                message = 'The Tile "{}" is not compatible with the constraint "{}" on importances that the annotation "{}" has.'.format(
                    self.name, constraint, annotation
                )
                logging.warning(message)
                ok = False

        constraint = annotation.getConstraintOnClassPriors()
        if constraint is not None:
            if not self.isCompatibleWithConstraintOnClassPriors(constraint):
                message = 'The Tile "{}" is not compatible with the constraint "{}" on class priors that the annotation "{}" has.'.format(
                    self.name, constraint, annotation
                )
                logging.warning(message)
                ok = False

        constraint = annotation.getConstraintOnPredictionRates()
        if constraint is not None:
            if not self.isCompatibleWithConstraintOnPredictionRates(constraint):
                message = 'The Tile "{}" is not compatible with the constraint "{}" on prediction rates that the annotation "{}" has.'.format(
                    self.name, constraint, annotation
                )
                logging.warning(message)
                ok = False

        constraint = self.getGlobalConstraintOnImportances()
        if constraint is not None:
            if not annotation.isCompatibleWithConstraintOnImportances(constraint):
                message = 'The annotation "{}" is not compatible with the global constraint "{}" on importances that the tile "{}" has.'.format(
                    annotation, constraint, self.name
                )
                logging.warning(message)
                ok = False

        constraint = self.getGlobalConstraintOnClassPriors()
        if constraint is not None:
            if not annotation.isCompatibleWithConstraintOnClassPriors(constraint):
                message = 'The annotation "{}" is not compatible with the global constraint "{}" on class priors that the tile "{}" has.'.format(
                    annotation, constraint, self.name
                )
                logging.warning(message)
                ok = False

        constraint = self.getGlobalConstraintOnPredictionRates()
        if constraint is not None:
            if not annotation.isCompatibleWithConstraintOnPredictionRates(constraint):
                message = 'The annotation "{}" is not compatible with the global constraint "{}" on prediction rates that the tile "{}" has.'.format(
                    annotation, constraint, self.name
                )
                logging.warning(message)
                ok = False

        if ok:
            self._annotations.append(annotation)
        else:
            message = (
                'The annotation "{}" has not been appended to the tile "{}"'.format(
                    annotation, self.name
                )
            )
            logging.warning(message)

    def removeAnnotation(self, annotation):
        assert isinstance(annotation, AbstractAnnotation)
        self._annotations.remove(annotation)

    def popAnnotation(self, index: SupportsIndex = -1) -> AbstractAnnotation:
        """
        Remove and return an annotation at index (default last).

        Args:
            index (SupportsIndex, optional): index of the annotation to pop. Defaults to -1.

        Returns:
            AbstractAnnotation: the annotation at the specified index.

        Raises:
            IndexError: if the index is out of range.
        """
        return self._annotations.pop(index)

    def clearAnnotations(self):
        self._annotations.clear()

    def draw(
        self,
        fig: Figure | None = None,
        ax: Axes | None = None,
        print_traceback_on_annotation_exception: bool = False,
    ) -> tuple[Figure, Axes]:
        """Draws the Tile in the given figure and axes.

        Args:
            fig (Figure | None, optional): The matplotlib.pyplot Figure to use for drawing. Defaults to None in which case a new Figure is created.
            ax (Axes | None, optional): The matplotlib.pyplot Axes to use for drawing. Defaults to None in which case the current Axes are used.

        Returns:
            tuple[Figure, Axes]: The matplotlib.pyplot Figure and Axes used for drawing.
        """

        assert fig is None or isinstance(fig, Figure)
        assert ax is None or isinstance(ax, Axes)

        if fig is None:
            fig = plt.figure()
            ax = fig.gca()
        elif ax is None:
            ax = fig.gca()

        # Draw all annotations

        for annotation in self.genAnnotations():
            assert isinstance(annotation, AbstractAnnotation)
            tile = self
            try:
                annotation.draw(tile, fig, ax)
            except BaseException as e:
                message = "Something went wrong while drawing annotation {!r}, got {} ({})".format(
                    annotation.name, type(e), e
                )
                if print_traceback_on_annotation_exception:
                    import traceback

                    print(traceback.format_exc())
                else:
                    message += " Set print_traceback_on_annotation_exception to True to see debug infos."
                logging.warning(message)

        # Configure the limits, axes labels, and title.

        x_min, x_max, y_min, y_max = self._zoom
        assert x_min < x_max
        assert y_min < y_max

        ax.set_xlim((x_min, x_max))
        ax.set_ylim((y_min, y_max))
        ax.set_aspect("equal")
        parameterization = self.parameterization
        ax.set_xlabel(parameterization.getNameParameter1())
        ax.set_ylabel(parameterization.getNameParameter2())
        ax.set_title(self.name)
        ax.set_facecolor("whitesmoke")

        return fig, ax

    def _unionOfConstraints(self, constraint1, constraint2):
        if constraint1 is None:
            if constraint2 is None:
                return None
            else:
                return constraint2
        else:
            if constraint2 is None:
                return constraint1
            else:
                if constraint1 == constraint2:
                    return constraint1
                else:
                    raise NotImplementedError(
                        "Sorbetto does not support yet the union of different constraints"
                    )

    def getGlobalConstraintOnImportances(
        self,
    ) -> ConstraintRelativeImportanceSatisfyingUnsatisfying | None:
        """Returns the global constraint on the importance values, or None if
        there is no such constraint. The global constraint includes the base
        constraint related to the flavor and how it is used, as well as all
        constraints related to the annotations.

        Returns:
            Any: The constraint.
        """
        global_constraint = self._base_constraint_on_importances
        # Note that the flavor has no getConstraintOnImportances() method.
        for annotation in self._annotations:
            constraint = annotation.getConstraintOnImportances()
            global_constraint = self._unionOfConstraints(global_constraint, constraint)
        return global_constraint

    def getGlobalConstraintOnClassPriors(self) -> ConstraintFixedClassPriors | None:
        """Returns the global constraint on the prediction rates, or None if
        there is no such constraint. The global constraint includes all
        constraints related to the annotations.

        Returns:
            Any: The constraint.
        """
        # Note that the tile has no _base_constraint_on_class_priors field.
        global_constraint = None
        # Note that the flavor has no getConstraintOnClassPriors() method.
        for annotation in self._annotations:
            constraint = annotation.getConstraintOnClassPriors()
            global_constraint = self._unionOfConstraints(global_constraint, constraint)
        return global_constraint

    def getGlobalConstraintOnPredictionRates(
        self,
    ) -> ConstraintFixedPredictionRates | None:
        """Returns the global constraint on the prediction rates, or None if
        there is no such constraint. The global constraint includes all
        constraints related to the annotations.

        Returns:
            Any: The constraint.
        """
        # Note that the tile has no _base_constraint_on_prediction_rates field.
        global_constraint = None
        # Note that the flavor has no getConstraintOnPredictionRates() method.
        for annotation in self._annotations:
            constraint = annotation.getConstraintOnPredictionRates()
            global_constraint = self._unionOfConstraints(global_constraint, constraint)
        return global_constraint

    def isCompatibleWithConstraintOnImportances(
        self, constraint: ConstraintRelativeImportanceSatisfyingUnsatisfying
    ) -> bool:
        assert isinstance(
            constraint, ConstraintRelativeImportanceSatisfyingUnsatisfying
        )
        if self.flavor is not None:
            if not self.flavor.isCompatibleWithConstraintOnImportances(constraint):
                return False
        for annotation in self._annotations:
            if not annotation.isCompatibleWithConstraintOnImportances(constraint):
                return False
        return True

    def isCompatibleWithConstraintOnClassPriors(
        self, constraint: ConstraintFixedClassPriors
    ) -> bool:
        assert isinstance(constraint, ConstraintFixedClassPriors)
        if self.flavor is not None:
            if not self.flavor.isCompatibleWithConstraintOnClassPriors(constraint):
                return False
        for annotation in self._annotations:
            if not annotation.isCompatibleWithConstraintOnClassPriors(constraint):
                return False
        return True

    def isCompatibleWithConstraintOnPredictionRates(
        self, constraint: ConstraintFixedPredictionRates
    ) -> bool:
        assert isinstance(constraint, ConstraintFixedPredictionRates)
        if self.flavor is not None:
            if not self.flavor.isCompatibleWithConstraintOnPredictionRates(constraint):
                return False
        for annotation in self._annotations:
            if not annotation.isCompatibleWithConstraintOnPredictionRates(constraint):
                return False
        return True

    def __str__(self) -> str:
        buffer = io.StringIO()
        buffer.write('This Tile is named "{}".'.format(self.name))
        buffer.write("\nIt uses the flavor: {}.".format(self.flavor))
        buffer.write(
            "\nIt uses the parameterization: {}.".format(self.parameterization)
        )
        if len(self._annotations) > 0:
            buffer.write("\nIt shows the following annotations:\n")
            for annotation in self._annotations:
                buffer.write("- {}\n".format(annotation.name))
        constraint = self.getGlobalConstraintOnImportances()
        buffer.write(
            "\nIt has the following constraint on importances: {}.".format(constraint)
        )
        constraint = self.getGlobalConstraintOnClassPriors()
        buffer.write(
            "\nIt has the following constraint on class priors: {}.".format(constraint)
        )
        constraint = self.getGlobalConstraintOnPredictionRates()
        buffer.write(
            "\nIt has the following constraint on prediction rates: {}.".format(
                constraint
            )
        )
        return buffer.getvalue()

    def getExplanation(self) -> str:
        return self.__str__()
