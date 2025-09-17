from collections.abc import Container

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
