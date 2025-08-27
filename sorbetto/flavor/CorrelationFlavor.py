class CorrelationFlavor(AbstractNumericFlavor):
    """
    For a given performance, the *Correlation Flavor* is the mathematical function
    that gives, to any importance $I$  (that is, some application-specific preferences),
    the correlation, using a defined correlation coefficient (e.g., Pearson's r),
    between a score $X$ and the Canonical Ranking Score $R_I$ corresponding to this
    importance.

    Args:
        AbstractNumericFlavor (_type_): _description_
    """

    def __init__(self, name=None):
        return
