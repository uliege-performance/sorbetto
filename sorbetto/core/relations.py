from abc import ABC, abstractmethod


class AbstractHomogeneousBinaryRelationOnPerformances(ABC):
    def __init__(self, name: str | None = None):
        self._name = name
        ABC.__init__(self)

    @property
    def name(self) -> str | None:
        return self._name

    # TODO: should we have some tolerance in the following methods ? Instead of bool, one could have something like {yes, perhaps, no}.
    @abstractmethod
    def __call__(self, p1, p2) -> bool: ...

    @abstractmethod
    def isReflexive(self) -> bool: ...

    @abstractmethod
    def isIrreflexive(self) -> bool: ...

    @abstractmethod
    def isTransitive(self) -> bool: ...

    @abstractmethod
    def isSymmetric(self) -> bool: ...

    @abstractmethod
    def isAsymmetric(self) -> bool: ...

    @abstractmethod
    def isAntisymmetric(self) -> bool: ...

    @abstractmethod
    def isEquivalence(self) -> bool: ...

    @abstractmethod
    def isPreorder(self) -> bool: ...

    @abstractmethod
    def isOrder(self) -> bool: ...

    @abstractmethod
    def isPartialOrder(self) -> bool: ...

    @abstractmethod
    def isTotalOrder(self) -> bool: ...

    def __invert__(self) -> "AbstractHomogeneousBinaryRelationOnPerformances":
        return _Complement(self)

    def __and__(self, other) -> "AbstractHomogeneousBinaryRelationOnPerformances":
        return _Intersection(self, other)

    def __or__(self, other) -> "AbstractHomogeneousBinaryRelationOnPerformances":
        return _Union(self, other)

    def getDual(self):
        return _Dual(self)

    def __str__(self):
        return f"AbstractHomogeneousBinaryRelationOnPerformances(name={self._name})"


class _Intersection(AbstractHomogeneousBinaryRelationOnPerformances):
    def __init__(
        self,
        rel1: AbstractHomogeneousBinaryRelationOnPerformances,
        rel2: AbstractHomogeneousBinaryRelationOnPerformances,
    ):
        super().__init__(name=f"Conjonction({rel1.name}, {rel2.name})")
        self._rel1 = rel1
        self._rel2 = rel2

    def isReflexive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isIrreflexive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isTransitive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isSymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isAsymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isAntisymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isEquivalence(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isPreorder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isPartialOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isTotalOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def __call__(self, p1, p2):
        return self._rel1(p1, p2) and self._rel2(p1, p2)


class _Union(AbstractHomogeneousBinaryRelationOnPerformances):
    def __init__(
        self,
        rel1: AbstractHomogeneousBinaryRelationOnPerformances,
        rel2: AbstractHomogeneousBinaryRelationOnPerformances,
    ):
        super().__init__(name=f"Disjonction({rel1.name}, {rel2.name})")
        self._rel1 = rel1
        self._rel2 = rel2

    def isReflexive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isIrreflexive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isTransitive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isSymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isAsymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isAntisymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isEquivalence(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isPreorder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isPartialOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isTotalOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def __call__(self, p1, p2):
        return self._rel1(p1, p2) or self._rel2(p1, p2)


class _Complement(AbstractHomogeneousBinaryRelationOnPerformances):
    def __init__(self, rel1: AbstractHomogeneousBinaryRelationOnPerformances):
        super().__init__(name=f"Negation({rel1.name})")
        self._rel1 = rel1

    def isReflexive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isIrreflexive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isTransitive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isSymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isAsymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isAntisymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isEquivalence(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isPreorder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isPartialOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isTotalOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def __call__(self, p1, p2):
        return not (self._rel1(p1, p2))


class _Dual(AbstractHomogeneousBinaryRelationOnPerformances):
    def __init__(self, rel1: AbstractHomogeneousBinaryRelationOnPerformances):
        super().__init__(name=f"Dual({rel1.name})")
        self._rel1 = rel1

    def isReflexive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isIrreflexive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isTransitive(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isSymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isAsymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isAntisymmetric(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isEquivalence(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isPreorder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isPartialOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def isTotalOrder(self) -> bool:
        raise NotImplementedError()  # TODO: implement this!

    def __call__(self, p1, p2):
        return self._rel1(p2, p1)
