from relations import AbstractHomogeneousBinaryRelationOnPerformances
from ..performance.two_class_classification import TwoClassClassificationPerformance
import numpy as np

class PerformanceOrderingInducedByOneScore ( AbstractHomogeneousBinaryRelationOnPerformances ) : # It is a preorder

    def __init__ ( self, 
                  score, 
                  name=None ):
        self._score = score

        super().__init__(name)
    # warning if score is not a RankingScore.

    def getName ( self ):
        return self._name
    
    def getScore(self):
        return self._score
    

    def isReflexive ( self ) -> bool:
        return True
    
    def isIrreflexive ( self ) -> bool:
        return False
    
    def isTransitive ( self ) -> bool:
        return True
    
    def isSymmetric ( self ) -> bool:
        # true only in degenerate cases
        return False
    
    def isAsymmetric ( self ) -> bool:
        # maybe degenerate cases
        return False
    
    def isAntisymmetric ( self ) -> bool:
        return False
    
    def isEquivalence ( self ) -> bool:
        raise NotImplementedError()
    
    def isPreorder ( self ) -> bool:
        return True
    
    def isOrder ( self ) -> bool:
        raise NotImplementedError()
    
    def isPartialOrder ( self ) -> bool:
        raise NotImplementedError()
    
    def isTotalOrder ( self ) -> bool:
        raise NotImplementedError()

    def __str__ ( self ):
        return f"PerformanceOrderingInducedByOneScore(name={self._name}, score={self._score})"

    def __call__ (self, 
                  p1: TwoClassClassificationPerformance, 
                  p2: TwoClassClassificationPerformance ) -> bool:
        # Theorem 1 of :cite:t:`Pierard2025Foundations`.

        if p1 == p2: 
            return True

        v1 = self._score(p1)
        v2 = self._score(p2)

        # score should return NaN if out of domain of definition

        if np.isnan(v1) or np.isnan(v2):
            return False

        if v1 <= v2:
            return True
        
        return False

    
    # We have four cases depending on the results of self(p1, p2) and self(p2, p1).
    #A.3.2
    def getRelationEquivalent ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances:
        return self & self.getDual()

    def getRelationBetter ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances:
        return (~self) & self.getDual()

    def getRelationWorse ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances:
        return self & (~self.getDual())
    
    def getRelationIncomparable ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances:
        return (~self) & (~self.getDual())
    
    # TODO: do we want the 10 relationships?
    # - we can choose if we accept equivalent
    # - we can choose if we accept better
    # - we can choose if we accept worse
    # - we can choose if we accept incomparable
    # There are 10, and not 2^4=16 interesting relationships because:
    # - we need to accept at least one;
    # - we need to not accept at least one;
    # - and accepting only one is already in the four above methods.

    def getRelationWorseOrEquivalent ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances:
        return self.getRelationEquivalent() or self.getRelationWorse()
    
    def getRelationBetterOrEquivalent ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances:
        return self.getRelationEquivalent() or self.getRelationBetter()
    
    def getRelationComparable ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances:
        return not self.getRelationIncomparable()
    
    # TODO ...