import io

import numpy as np

from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.abstract_tile import AbstractTile


class EmptyTile(AbstractTile):
    """
    This is the type of Tiles for which there is no flavor. This type of Tiles is
    useful when we want only to draw annotations.
    """

    def __init__(self, name: str | None, parameterization: AbstractParameterization):
        """
        Creates a new EmptyTile object.

        Args:
            name (str | None, optional): the Tile's name. If set to None, a default string is used.
            parameterization (AbstractParameterization): The parameterization to be used for the Tile.
        """

        if name is None:
            name = "empty Tile"
        else:
            if not isinstance(name, str):
                # TODO : emit a warning
                name = str(name)

        assert isinstance(parameterization, AbstractParameterization)

        AbstractTile.__init__(self, name, parameterization)

    def getExplanation(self) -> str:
        annotations = list(self.genAnnotations())
        if len(annotations) == 0:
            return "This is an empty Tile."
        buffer = io.StringIO()
        buffer.write("This Tile shows the following:\n")
        for annotation in annotations:
            buffer.write("- {}\n".format(annotation.getName()))
        return buffer.getvalue()

    # def getParameterization(self) -> AbstractParameterization: ...
    # TODO : should it be defined here ?

    # def getFlavor(self) -> AbstractFlavor: ...
    # TODO : should it be defined here ?

    def getResolution(self) -> int:
        return 0

    def getVecParam1(self) -> np.array:
        return np.empty([0])

    def getVecParam2(self) -> np.array:
        return np.empty([0])

    def getMat(self) -> np.ndarray:
        return np.empty([0, 0])

    def getColormap(self) -> np.ndarray:
        return None
