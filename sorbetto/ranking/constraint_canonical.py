from sorbetto.ranking import Importance


class ConstraintCanonical:
    def __init__(self):
        pass

    def __call__(self, importance):
        assert isinstance(importance, Importance)
        return importance.isCanonical()

    def __str__(self):
        return "constraint: canonical importance"
