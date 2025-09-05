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

        self._no_name = True

        # Initialize instance attributes.
        # The value put here are necessary for the property setter to work propertly.
        # Do not change them, unless you change the logic coded in the setters.
        self._name: str | None = None
        self._abbreviation: str | None = None
        self._symbol: str | None = None

        # Noww, use the property setters to check the arguments, choose the default
        # value if the provided value is None, and to store the right value in the
        # instance attribute. Do not change the order in which these calls are made,
        # unless you change the logic coded in the setters.
        self.name = name
        self.abbreviation = abbreviation
        self.symbol = symbol

        ABC.__init__(self)

    @property
    def name(self) -> str:
        if self._no_name:
            return self._default_name
        else:
            return self._name

    @name.setter
    def name(self, name: str | None) -> None:
        """
        Set the name of the ranking score, and erases the abbreviation and symbol.
        If the provided name is None, it is replaced by a default string.

        Args:
            name (str | None): the name.
        """
        if name is None:
            self._no_name = True
        else:
            self._no_name = False
            self._name = str(name)
            # If we change the score name, the previous abbreviation is most probably no longer relevant.
            # Note that you can use the abbreviation setter after calling the name setter.
            self._abbreviation = None
            # If we change the score name, the previous symbol is most probably no longer relevant.
            # Note that you can use the symbol setter after calling the name setter.
            self._symbol = None

    @property
    def abbreviation(self) -> str | None:
        if self._no_name:
            return self._default_abbreviation
        else:
            return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation: str | None) -> None:
        """
        Set the abbreviation of the ranking score. The abbreviation can be set to a
        string only once after setting the name. If you need to change the abbreviation a
        second time, call the name setter first.

        Args:
            abbreviation (str | None): the abbreviation.

        Raises:
            RuntimeError: when trying to change the abbreviation twice.
        """
        # check argument
        assert abbreviation is None or isinstance(abbreviation, str)
        # check that the abbreviation is unset (the instance attribute should be None)
        assert not self._no_name
        if self._abbreviation is not None:
            raise RuntimeError("The name should be set before the abbreviation")
        else:
            self._abbreviation = abbreviation

    @property
    def symbol(self) -> str | None:
        if self._no_name:
            return self._default_symbol
        else:
            return self._symbol

    @symbol.setter
    def symbol(self, symbol: str | None) -> None:
        """
        Set the (mathematical) symbol of the ranking score. The symbol can be set to a
        string only once after setting the name. If you need to change the symbol a
        second time, call the name setter first.

        Args:
            symbol (str | None): the symbol.

        Raises:
            RuntimeError: when trying to change the symbol twice.
        """
        # check argument
        assert symbol is None or isinstance(symbol, str)
        # check that the symbol is unset (the instance attribute should be None)
        assert not self._no_name
        if self._symbol is not None:
            raise RuntimeError("The name should be set before the symbol")
        else:
            self._symbol = symbol

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
