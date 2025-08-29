import logging
import pathlib

import matplotlib

matplotlib.use("svg")

import matplotlib.pyplot as plt

FIG_PATH = pathlib.Path(__file__).parent.parent / "figures"
logging.basicConfig(level=logging.INFO)


def save_fig(name: str):
    """
    Save a figure for the documentation.
    Please provide the figure name without extension.
    Use a relative path from the `figures/` directory.

    Args:
        name (str): Figure name without extension.
    """

    fig_file = FIG_PATH / f"{name}.svg"
    fig_file.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(fig_file)


def run_and_save(func, name: str, *args, skip_existing: bool = True, **kwargs):
    """
    Run a function that generates a figure and save it for the documentation.
    Please provide the figure name without extension.
    Use a relative path from the `figures/` directory.

    Args:
        func (callable): Function that generates a figure.
        name (str): Figure name without extension.
        skip_existing (bool, optinal): If True, skip the function call if the
            figure already exists.
        *args: Optional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
    """

    fig_file = FIG_PATH / f"{name}.svg"

    if skip_existing and fig_file.exists():
        logging.info("Figure %s already exists, skipping.", name)
        return

    try:
        func(*args, **kwargs)
        save_fig(name)
        logging.info("Figure %s saved.", name)
    except Exception as e:
        logging.error(f"Failed to generate figure {name}: {e}")
