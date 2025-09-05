from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.core.importance import Importance
from sorbetto.geometry.point import Point
from sorbetto.ranking.ranking_score import RankingScore

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AnnotationText(AbstractAnnotation):
    """
    This type of annotation can be used to place a text on the Tile, next to the point
    corresponding to given importance values.
    """

    def __init__(
        self,
        location: Importance | RankingScore | Point,
        label: str | None = None,
        **plt_kwargs,
    ):
        """
        Initializes a new annotation for a text object.

        Args:
            location (Importance | RankingScore | Point): where to write the label
            label (str | None, optional): what text to write (if None, will
                attempt to use the shortName of the location). Defaults to None.
        """

        assert isinstance(location, (Importance, RankingScore, Point))
        self._location = location

        if label is not None:
            if not isinstance(label, str):
                label = str(label)
        elif isinstance(location, RankingScore):
            label = location.shortLabel

        self._plt_kwargs = plt_kwargs

        AbstractAnnotation.__init__(self, label)

    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        from sorbetto.tile.tile import Tile

        assert isinstance(tile, Tile)
        parameterization = tile.parameterization
        location = self._location
        if isinstance(location, Importance):
            importance = location
            rankingScore = RankingScore(importance)
            x = parameterization.getValueParameter1(rankingScore)
            y = parameterization.getValueParameter2(rankingScore)
        elif isinstance(location, RankingScore):
            rankingScore = location
            x = parameterization.getValueParameter1(rankingScore)
            y = parameterization.getValueParameter2(rankingScore)
        elif isinstance(location, Point):
            point = location
            x = point.x
            y = point.y
        else:
            assert False  # This should never happen
        min_x, max_x = parameterization.getBoundsParameter1()
        min_y, max_y = parameterization.getBoundsParameter2()
        if x < min_x or x > max_x:
            return
        if y < min_y or y > max_y:
            return
        center_x = 0.5 * (min_x + max_x)
        center_y = 0.5 * (min_y + max_y)
        ax.plot(x, y, "o", **self._plt_kwargs)
        if x < center_x:
            if y < center_y:
                ax.text(x, y, self.name, ha="left", va="bottom")
            else:
                ax.text(x, y, self.name, ha="left", va="top")
        else:
            if y < center_y:
                ax.text(x, y, self.name, ha="right", va="bottom")
            else:
                ax.text(x, y, self.name, ha="right", va="top")
