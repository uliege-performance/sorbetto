import math


def _setupROC(
    fig,
    ax,
    priorPos: float | None = None,
    show_no_skills: bool = True,
    show_priors: bool = True,
    show_unbiased=True,
):
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

    if show_unbiased:
        if priorPos <= 0.5:
            ax.plot([0, priorPos / priorNeg], [1, 0], "--", c="palevioletred")
        else:
            ax.plot([0, 1], [1, 1 - priorNeg / priorPos], "--", c="palevioletred")
        x = 0.5 * priorPos
        y = 0.5 + 0.5 * priorPos
        a = math.atan2(priorNeg, -priorPos) * 180.0 / math.pi
        ax.text(
            x,
            y,
            "unbiased",
            ha="center",
            va="baseline",
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
