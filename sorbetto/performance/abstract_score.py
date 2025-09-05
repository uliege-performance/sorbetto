from abc import ABC, abstractmethod

from sorbetto.performance.abstract_performance import AbstractPerformance


class AbstractScore(ABC):
    def __init__(
        self,
        default_name: str,
        default_abbreviation: str | None,
        default_symbol: str | None,
        name: str | None = None,
        abbreviation: str | None = None,
        symbol: str | None = None,
    ):
        """
        Args:
            default_name (str): The name to use in place of None.
            default_abbreviation (str | None): The abbreviation to use when the default name is used.
            default_symbol (str | None): The symbol to use when the default name is used.
            name (str | None, optional): The initial name. Defaults to None.
            abbreviation (str | None, optional): The initial abbreviation. Defaults to None.
            symbol (str | None, optional): The initial symbol. Defaults to None.
        """

        assert isinstance(default_name, str)
        self._default_name = default_name

        assert default_abbreviation is None or isinstance(default_abbreviation, str)
        self._default_abbreviation = default_abbreviation

        assert default_symbol is None or isinstance(default_symbol, str)
        self._default_symbol = default_symbol

        # Initialize instance attributes.
        # The value put here are necessary for the property setter to work propertly.
        # Do not change them, unless you change the logic coded in the setters.
        self._name: str | None = name
        self._abbreviation: str | None = abbreviation
        self._symbol: str | None = symbol

        ABC.__init__(self)

    def rename(
        self,
        name: str | None = None,
        abbreviation: str | None = None,
        symbol: str | None = None,
    ) -> None:
        """
        Set the name, abbreviation, and symbol of the score. It is not allowed
        to set the abbreviation or symbol without giving a name too.

        Args:
            name (str | None, optional): the new name. Defaults to None.
            abbreviation (str | None, optional): the new abbreviation. Defaults to None.
            symbol (str | None, optional): the new symbol. Defaults to None.

        Raises:
            ValueError: if name is None and abbreviation or symbol are not None.
        """
        if name is None:
            self._name = name

            if abbreviation is not None or symbol is not None:
                raise ValueError(
                    "Cannot set abbreviation and symbol when name is None. Abbreviation and symbol must be None too."
                )
            self._abbreviation = None
            self._symbol = None

        else:
            self._name = str(name)
            if abbreviation is None:
                self._abbreviation = None
            else:
                self._abbreviation = str(abbreviation)
            if symbol is None:
                self._symbol = None
            else:
                self._symbol = str(symbol)

    @property
    def name(self) -> str:
        if self._name is None:
            return self._default_name
        else:
            return self._name

    @property
    def abbreviation(self) -> str | None:
        if self._name is None:
            return self._default_abbreviation
        else:
            return self._abbreviation

    @property
    def symbol(self) -> str | None:
        if self._name is None:
            return self._default_symbol
        else:
            return self._symbol

    @property
    def shortLabel(self) -> str:
        name = self.name
        abbreviation = self.abbreviation
        symbol = self.symbol

        if symbol is not None:
            # We assume that the symbol is shorter that the abbreviation and the name
            return symbol
        elif abbreviation is not None:
            # We assume that the abbreviation is shorter that the name
            return abbreviation
        else:
            return name

    @property
    def longLabel(self) -> str:
        name = self.name
        abbreviation = self.abbreviation
        symbol = self.symbol

        provide_abbreviation = abbreviation is not None
        provide_symbol = symbol is not None and symbol != abbreviation

        label = f"{name}"
        if provide_abbreviation or provide_symbol:
            label += " ("
            if abbreviation is not None:
                label += f"{abbreviation}"
            if provide_abbreviation and provide_symbol:
                label += ", "
            if symbol is not None:
                label += f"{symbol}"
            label += ")"
        return label

    @abstractmethod
    def __call__(self, performance: AbstractPerformance) -> float: ...
