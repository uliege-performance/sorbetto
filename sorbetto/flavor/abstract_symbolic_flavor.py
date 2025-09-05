from abc import abstractmethod
from typing import Any, Generic, TypeVar

from sorbetto.flavor.abstract_flavor import AbstractFlavor

T = TypeVar("T")


class AbstractSymbolicFlavor(AbstractFlavor, Generic[T]):
    """
    A symbolic flavor is a function that gives something to show on a Tile for any
    given importance values.
    """

    def __init__(self, name: str = "Unnamed Symbolic Flavor", colormap: Any = None):
        super().__init__(name=name, colormap=colormap)
        self._sorted_codomain: list[T] | None = None

    @abstractmethod
    def getCodomain(self) -> set[T]:
        """Returns the codomain of the flavor.
        See https://en.wikipedia.org/wiki/Codomain

        Returns:
            The codomain of the flavor.
        """

    def _getSortedCodomain(self) -> list[T]:
        """Returns the codomain of the flavor, sorted in a stable way.

        This uses Python's built-in sorting with the id function as key, so
        the sorting works with any type, and stays relatively fast.

        Returns:
            The codomain of the flavor, sorted in a stable way.
        """
        if self._sorted_codomain is None:
            self._sorted_codomain = sorted(self.getCodomain(), key=id)  # type:ignore
        return self._sorted_codomain

    def mapper(self, value: T) -> int:
        """Maps a value in the codomain to an integer in [1, n], where n is the size of
        the codomain.

        This is stable as long as the codomain does not change.

        Args:
            value (T): A value in the codomain.

        Returns:
            int: An integer in [1, n], where n is the size of the codomain.
        """

        codomain = self._getSortedCodomain()
        try:
            return codomain.index(value) + 1
        except ValueError as exc:
            raise ValueError(f"Value {value!r} not in codomain {codomain}") from exc

    def reverse_mapper(self, index: int) -> T:
        """Maps an integer in [1, n], where n is the size of the codomain, to a value
        in the codomain.

        This is stable as long as the codomain does not change.

        Args:
            index (int): An integer in [1, n], where n is the size of the codomain.

        Returns:
            T: A value in the codomain.
        """
        codomain = self._getSortedCodomain()
        if index < 1 or index > len(codomain):
            raise ValueError(
                f"Index {index} out of bounds for codomain of size {len(codomain)}"
            )
        return codomain[index - 1]
