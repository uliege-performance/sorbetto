import logging


class Named:
    def __init__(self, default_name: str, name: str | None = None):
        assert isinstance(default_name, str)
        self._default_name = default_name
        self.name = name  # use the setter

    @property
    def name(self) -> str:
        if self._name is None:
            return self._default_name
        elif isinstance(self._name, str):
            return self._name
        else:
            return str(self._name)

    @name.setter
    def name(self, name: str | None):
        if name is not None:
            if not isinstance(name, str):
                logging.warning("Setting a name that is not a str.")
        self._name = name

    def __str__(self) -> str:
        return "Named({})".format(self.name)  # use the getter
