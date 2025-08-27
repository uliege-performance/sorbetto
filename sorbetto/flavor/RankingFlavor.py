class RankingFlavor(AbstractNumericFlavor):
    """
    For a given entity in a finite set of entities, the *Ranking Flavor* is the
    mathematical function that gives, to any importance $I$  (that is, some application-
    specific preferences), the rank of that entity.
    For a given set of entities, the ranking is based on the ordering of performances
    induced by the Canonical Ranking Score $R_I$ corresponding to the importance $I$.

    Args:
        AbstractNumericFlavor (_type_): _description_
    """

    def __init__(self, name=None):
        return
