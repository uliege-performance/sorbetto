# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
import math
from collections.abc import Container

import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import hsv_to_rgb
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text


def _filter_properties(
    properties: dict | None, supported_properties: Container
) -> dict | None:
    assert isinstance(supported_properties, Container)

    if properties is None:
        return None

    assert isinstance(properties, dict)
    filtered_kwargs = {k: v for k, v in properties.items() if k in supported_properties}
    return filtered_kwargs


def supported_properties_fot_text() -> Container:
    # print("Determining the supported properties for text ...")
    # Properties supported by any matplotlib.text.Text object.
    return Text().properties().keys()


def filter_properties_for_text(
    properties: dict | None,
    _supported_properties: Container = supported_properties_fot_text(),
) -> dict | None:
    return _filter_properties(properties, _supported_properties)


def supported_properties_for_plot() -> Container:
    # print("Determining the supported properties for plot ...")
    # Properties supported by any matplotlib.lines.Line2D object.
    return Line2D([], []).properties().keys()


def filter_properties_for_plot(
    properties: dict | None,
    _supported_properties: Container = supported_properties_for_plot(),
) -> dict | None:
    return _filter_properties(properties, _supported_properties)


def supported_properties_for_arrow() -> Container:
    # print("Determining the supported properties for arrow ...")
    # Properties supported by any matplotlib.patches.Patch object.
    return Rectangle((0, 0), 1, 1).properties().keys()


def filter_properties_for_arrow(
    properties: dict | None,
    _supported_properties: Container = supported_properties_for_arrow(),
) -> dict | None:
    return _filter_properties(properties, _supported_properties)


def _setupROC(
    fig: Figure,
    ax: Axes,
    priorPos: float | None = None,
    show_no_skills: bool = True,
    show_priors: bool = True,
    show_unbiased: bool = True,
    show_opposite_unbiased: bool = True,
):
    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)
    if priorPos is not None:
        assert isinstance(priorPos, float)
        assert priorPos >= 0.0
        assert priorPos <= 1.0
        priorNeg = 1.0 - priorPos
    else:
        show_priors = False
        show_unbiased = False
        show_opposite_unbiased = False
        priorNeg = None

    assert isinstance(show_no_skills, bool)
    assert isinstance(show_priors, bool)
    assert isinstance(show_unbiased, bool)
    assert isinstance(show_opposite_unbiased, bool)

    if priorNeg < 1e-8:
        message = "The prior of the negative class is {:g}".format(priorNeg)
        message += "ROC coordinates are unreliable with such a low value."
        logging.warning(message)
    if priorNeg < 1e-8:
        message = "The prior of the positive class is {:g}".format(priorPos)
        message += "ROC coordinates are unreliable with such a low value."
        logging.warning(message)

    if show_no_skills:
        ax.plot([0, 1], [0, 1], "--", c="palevioletred")
        ax.text(
            0.5,
            0.5,
            r"no-skill: $P(Y,\hat{Y}) = P(Y) P(\hat{Y})$",
            ha="center",
            va="baseline",
            rotation=45,
            c="palevioletred",
            rotation_mode="anchor",
        )

    if show_priors:
        ax.plot(
            [0, priorPos, priorPos], [priorPos, priorPos, 0], ":", c="palevioletred"
        )
        ax.plot(priorPos, priorPos, "o", c="palevioletred")

    if show_unbiased:
        if priorPos <= 0.5:
            ax.plot([0, priorPos / priorNeg], [1, 0], "--", c="palevioletred")
        else:
            ax.plot([0, 1], [1, 1 - priorNeg / priorPos], "--", c="palevioletred")
        x = 0.5 * priorPos
        y = 0.5 + 0.5 * priorPos
        a = math.atan2(-priorNeg, priorPos) * 180.0 / math.pi
        ax.text(
            x,
            y,
            r"unbiased\n$P(\{fp\}) = P(\{fn\})$",
            ha="center",
            va="top" if priorPos >= 0.5 else "baseline",
            rotation=a,
            c="palevioletred",
            rotation_mode="anchor",
        )

    if show_opposite_unbiased:
        if priorPos <= 0.5:
            ax.plot([1, 1 - priorPos / priorNeg], [0, 1], "--", c="palevioletred")
        else:
            ax.plot([1, 0], [0, priorNeg / priorPos], "--", c="palevioletred")
        x = 1.0 - 0.5 * priorPos
        y = 0.5 - 0.5 * priorPos
        a = math.atan2(-priorNeg, priorPos) * 180.0 / math.pi
        ax.text(
            x,
            y,
            r"opposite unbiased\n$P(\{tn\}) = P(\{tp\})$",
            ha="center",
            va="top" if priorPos < 0.5 else "baseline",
            rotation=a,
            c="palevioletred",
            rotation_mode="anchor",
        )

    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xlabel("False Positive Rate (FPR)")
    ax.set_ylabel("True Positive Rate (TPR)")
    ax.set_aspect("equal")
    if priorPos is None:
        ax.set_title("ROC space")
    else:
        ax.set_title(r"ROC space for $\pi_+={:g}$".format(priorPos))


# TODO rename for clarity
def get_colors(num_colors):
    x = np.linspace(0.0, 1.0, num_colors)
    a = np.floor(x * x * np.sqrt(num_colors))
    v = 1.0 - a / (np.max(a) + 1)
    h = x * x * (np.max(a) + 1)
    h = h - np.floor(h)
    hsv = np.ones([num_colors, 3])
    hsv[:, 0] = h
    hsv[:, 1] = v
    hsv[:, 2] = 1.0
    rgb = hsv_to_rgb(hsv)
    rgba = np.ones([num_colors, 4])
    rgba[:, 0:3] = rgb
    return rgba
