# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
import math

from matplotlib.axes import Axes
from matplotlib.figure import Figure


def _setupROC(
    fig: Figure,
    ax: Axes,
    priorPos: float | None = None,
    show_no_skills: bool = True,
    show_priors: bool = True,
    show_unbiased=True,
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
        priorNeg = None

    assert isinstance(show_no_skills, bool)
    assert isinstance(show_priors, bool)
    assert isinstance(show_unbiased, bool)

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
            "no-skill",
            ha="center",
            va="baseline",
            rotation=45,
            c="palevioletred",
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
            "unbiased",
            ha="center",
            va="top" if priorPos >= 0.5 else "baseline",
            rotation=a,
            c="palevioletred",
        )

    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xlabel("False Positive Rate (FPR)")
    ax.set_ylabel("True Positive Rate (TPR)")
    ax.set_aspect("equal")
    if priorPos is None:
        ax.set_title("ROC space")
    else:
        ax.set_title("ROC space for $\\pi_+={:g}$".format(priorPos))
