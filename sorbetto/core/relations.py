from abc import abstractmethod
from typing import Self

# what is known_properties ??

class AbstractHomogeneousBinaryRelationOnPerformances :

	def __init__ ( self, 
			   name:str | None =None):
		self._name = name
		

	# TODO: should we have some tolerance ? Instead of bool, one could have {yes, perhaps, no}.
	@abstractmethod
	def __call__ ( self, p1, p2 ) -> bool:
		pass
		
	
	@abstractmethod
	def isReflexive ( self ) -> bool:
		pass
	@abstractmethod
	def isIrreflexive ( self ) -> bool:
		pass
	@abstractmethod
	def isTransitive ( self ) -> bool:
		pass
	@abstractmethod
	def isSymmetric ( self ) -> bool:
		pass
	@abstractmethod
	def isAsymmetric ( self ) -> bool:
		pass
	@abstractmethod
	def isAntisymmetric ( self ) -> bool:
		pass
	@abstractmethod
	def isEquivalence ( self ) -> bool:
		pass
	@abstractmethod
	def isPreorder ( self ) -> bool:
		pass
	@abstractmethod
	def isOrder ( self ) -> bool:
		pass
	@abstractmethod
	def isPartialOrder ( self ) -> bool:
		pass
	@abstractmethod
	def isTotalOrder ( self ) -> bool:
		pass
	
	def __invert__ ( self ) -> Self:
		return __Negation(self)

	def __and__ ( self, other):
		return __Conjonction(self, other)

	def __or__ ( self, other ):
		return __Disjonction(self, other)

	def getDual(self):
		return __Dual(self)

	def getName ( self ):
		return self._name

	def __str__ ( self ):
		return f"AbstractHomogeneousBinaryRelationOnPerformances(name={self._name}, known_properties={self._known_properties})"
	

class __Conjonction(AbstractHomogeneousBinaryRelationOnPerformances):

	def __init__(self, rel1: AbstractHomogeneousBinaryRelationOnPerformances, rel2: AbstractHomogeneousBinaryRelationOnPerformances):
		super().__init__(name=f"Conjonction({rel1.getName()}, {rel2.getName()})")
		self._rel1 = rel1
		self._rel2 = rel2


	def isReflexive ( self ) -> bool:
		raise NotImplementedError()

	def isIrreflexive ( self ) -> bool:
		raise NotImplementedError()

	def isTransitive ( self ) -> bool:
		raise NotImplementedError()

	def isSymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isAsymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isAntisymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isEquivalence ( self ) -> bool:
		raise NotImplementedError()

	def isPreorder ( self ) -> bool:
		raise NotImplementedError()

	def isOrder ( self ) -> bool:
		raise NotImplementedError()

	def isPartialOrder ( self ) -> bool:
		raise NotImplementedError()

	def isTotalOrder ( self ) -> bool:
		raise NotImplementedError()
	
	def __call__(self, p1, p2):
		return self._rel1(p1, p2) and self._rel2(p1, p2)
	

class __Disjonction(AbstractHomogeneousBinaryRelationOnPerformances):

	def __init__(self, rel1: AbstractHomogeneousBinaryRelationOnPerformances, rel2: AbstractHomogeneousBinaryRelationOnPerformances):
		super().__init__(name=f"Disjonction({rel1.getName()}, {rel2.getName()})")
		self._rel1 = rel1
		self._rel2 = rel2

	def isReflexive ( self ) -> bool:
		raise NotImplementedError()

	def isIrreflexive ( self ) -> bool:
		raise NotImplementedError()

	def isTransitive ( self ) -> bool:
		raise NotImplementedError()

	def isSymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isAsymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isAntisymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isEquivalence ( self ) -> bool:
		raise NotImplementedError()

	def isPreorder ( self ) -> bool:
		raise NotImplementedError()

	def isOrder ( self ) -> bool:
		raise NotImplementedError()

	def isPartialOrder ( self ) -> bool:
		raise NotImplementedError()

	def isTotalOrder ( self ) -> bool:
		raise NotImplementedError()
	
	def __call__(self, p1, p2):
		return self._rel1(p1, p2) or self._rel2(p1, p2)
	

class __Negation(AbstractHomogeneousBinaryRelationOnPerformances):
	def __init__(self, rel1: AbstractHomogeneousBinaryRelationOnPerformances):
		super().__init__(name=f"Negation({rel1.getName()})")
		self._rel1 = rel1

	def isReflexive ( self ) -> bool:
		raise NotImplementedError()

	def isIrreflexive ( self ) -> bool:
		raise NotImplementedError()

	def isTransitive ( self ) -> bool:
		raise NotImplementedError()

	def isSymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isAsymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isAntisymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isEquivalence ( self ) -> bool:
		raise NotImplementedError()

	def isPreorder ( self ) -> bool:
		raise NotImplementedError()

	def isOrder ( self ) -> bool:
		raise NotImplementedError()

	def isPartialOrder ( self ) -> bool:
		raise NotImplementedError()

	def isTotalOrder ( self ) -> bool:
		raise NotImplementedError()
	
	def __call__(self, p1, p2):
		return not(self._rel1(p1, p2))
	

class __Dual(AbstractHomogeneousBinaryRelationOnPerformances):
	def __init__(self, rel1: AbstractHomogeneousBinaryRelationOnPerformances):
		super().__init__(name=f"Dual({rel1.getName()})")
		self._rel1 = rel1

	def isReflexive ( self ) -> bool:
		raise NotImplementedError()

	def isIrreflexive ( self ) -> bool:
		raise NotImplementedError()

	def isTransitive ( self ) -> bool:
		raise NotImplementedError()

	def isSymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isAsymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isAntisymmetric ( self ) -> bool:
		raise NotImplementedError()

	def isEquivalence ( self ) -> bool:
		raise NotImplementedError()

	def isPreorder ( self ) -> bool:
		raise NotImplementedError()

	def isOrder ( self ) -> bool:
		raise NotImplementedError()

	def isPartialOrder ( self ) -> bool:
		raise NotImplementedError()

	def isTotalOrder ( self ) -> bool:
		raise NotImplementedError()
	
	def __call__(self, p1, p2):
		return self._rel1(p2, p1)
	
