from ..core.importance import Importance
from ..performance.two_class_classification import TwoClassClassificationPerformance

class RankingScore:

    def __init__ (self, importance: Importance, constraint=None, name: str| None=None):
        """
        Args:
            importance (Importance): _description_
            constraint (_type_, optional): _description_. Defaults to None.
            name (str | None, optional): _description_. Defaults to None.

        Raises:
            TypeError: _description_
        """
        if not isinstance(importance, Importance):
            raise TypeError(f"importance must be an instance of Importance, got {type(importance)}")
        
        self.importance = importance
        self.constraint = constraint
        
        self.name = name or "R_I"

    def getImportance (self) -> Importance: 
        return self.importance
        
    
    def isCanonical (self, tol=1e-8 ) -> bool:
        """
        See :cite:t:`Pierard2024TheTile-arxiv`, Definition 1.
        """
        return ( self.importance.itn + self.importance.itp ) > tol and ( self.importance.ifp + self.importance.ifn ) > tol
    
    # def toPABDC () -> "RankingScore"
    #     """
    #     See :cite:t:`Pierard2024TheTile-arxiv`, Example 3.
    #     """
    
    def drawInROC (self, fig, ax, priorPos):
        return
    
    # def getPencilInROC ( self, priorPos ) -> Pencil:
    #     return
    
    def __call__ (self, performance) -> float : # should check constraint
        satisfying = performance.ptn * self.importance.itn + performance.ptp * self.importance.itp
        unsatisfying = performance.pfp * self.importance.ifp + performance.pfn * self.importance.ifn
        return satisfying/(satisfying+unsatisfying)
    
    @staticmethod
    def getTrueNegativeRate () -> "RankingScore" :                                           # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        True Negative Rate (TNR).
        Synonyms: specificity, selectivity, inverse recall.
        """
        I = Importance(itn=1, ifp=1, ifn=0, itp=0)
        return RankingScore(I, name="TNR")

    @staticmethod
    def getTruePositiveRate () -> "RankingScore" :                                            # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        True Positive Rate (TPR).
        Synonyms: sensitivity, recall.
        """
        I = Importance(itn=0, ifp=0, ifn=1, itp=1)
        return RankingScore(I, name="TPR")
    
    @staticmethod
    def getSpecificity () -> "RankingScore":
        return RankingScore.getTrueNegativeRate()
    
    @staticmethod
    def getSelectivity () -> "RankingScore":
        return RankingScore.getTrueNegativeRate()
    
    @staticmethod
    def getSensitivity () -> "RankingScore":
        return RankingScore.getTruePositiveRate()
    
    @staticmethod
    def getNegativePredictiveValue () -> "RankingScore":                                     # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        Negative Predictive Value (NPV).
        Synonym: inverse precision
        """
        I = Importance(itn=1, ifp=0, ifn=1, itp=0)
        return RankingScore(I, name="NPV")

    @staticmethod
    def getPositivePredictiveValue () -> "RankingScore":                                     # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        """
        Positive Predictive Value (PPV).
        Synonym: precision
        """
        I = Importance(itn=0, ifp=1, ifn=0, itp=1)
        return RankingScore(I, name="PPV")
    
    @staticmethod
    def getPrecision () -> "RankingScore":
        return RankingScore.getPositivePredictiveValue()
    
    @staticmethod
    def getInversePrecision () -> "RankingScore":
        return RankingScore.getNegativePredictiveValue()
    
    @staticmethod
    def getRecall () -> "RankingScore":
        return RankingScore.getTruePositiveRate()
    
    @staticmethod
    def getInverseRecall () -> "RankingScore":
        return RankingScore.getTrueNegativeRate()
    
    @staticmethod
    def getIntersectionOverUnion () -> "RankingScore":
        """
        Intersection over Union (IoU).
        Synonyms: Jaccard index, Jaccard similarity coefficient, Tanimoto coefficient, similarity, critical success index (CSI), threat score.
        """
        I = Importance(itn=0, ifp=1, ifn=1, itp=1)
        return RankingScore(I, name="IoU")
    
    @staticmethod
    def getInverseIntersectionOverUnion () -> "RankingScore":
        I = Importance(itn=1, ifp=1, ifn=1, itp=0)
        return RankingScore(I, name="Inverse IoU")
    
    @staticmethod
    def getJaccard () -> "RankingScore":
        return RankingScore.getIntersectionOverUnion ()
    
    @staticmethod
    def getInverseJaccard () -> "RankingScore":
        return RankingScore.getInverseIntersectionOverUnion ()
    
    @staticmethod
    def getTanimotoCoefficient () -> "RankingScore":
        return RankingScore.getIntersectionOverUnion ()
    
    @staticmethod
    def getSimilarity () -> "RankingScore":
        return RankingScore.getIntersectionOverUnion ()
    
    @staticmethod
    def getCriticalSuccessIndex () -> "RankingScore":
        return RankingScore.getIntersectionOverUnion ()

    @staticmethod
    def getF (beta=1.0) -> "RankingScore":                               # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        if beta < 0:
            raise ValueError(f"beta must be positive, got {beta}")
        
        I = Importance(itn=0, ifp=1/(1+beta**2), ifn=beta**2/(1+beta**2), itp=1)
        return RankingScore(I, name=f"F{beta}")
        
                                                         
    @staticmethod
    def getInverseF (beta=1.0) -> "RankingScore":
        if beta < 0:
            raise ValueError(f"beta must be positive, got {beta}")
        
        I = Importance(itn=1, ifp=beta**2/(1+beta**2), ifn=1/(1+beta**2), itp=0)
        return RankingScore(I, name=f"Inverse F{beta}")

    @staticmethod
    def getDiceSorensenCoefficient () -> "RankingScore":
        return RankingScore.getF(beta=1.0)

    @staticmethod
    def getZijdenbosSimilarityIndex () -> "RankingScore":
        return RankingScore.getF(beta=1.0)
    
    @staticmethod
    def getCzekanowskiBinaryIndex () -> "RankingScore":
       return RankingScore.getF(beta=1.0)
    
    @staticmethod
    def getAccuracy () -> "RankingScore":                                                    # See :cite:t:`Pierard2025Foundations`, Section A.7.3
        I = Importance(itn=1, ifp=1, ifn=1, itp=1)
        return RankingScore(I, name="A")

    @staticmethod
    def getMatchingCoefficient () -> "RankingScore": # SimpleMatchingCoefficient ??? Same as Jaccard ???
        return RankingScore.getAccuracy()
    
    @staticmethod
    def getSkewInsensitiveVersionOfF (priorPos) -> "RankingScore":                         # TODO: implement constraint
        """
        The skew-insensitive version of $\scoreFOne$.
        Defined in cite:t:`Flach2003TheGeometry`.
        """
    @staticmethod
    def getWeightedAccuracy (priorPos, weightPos) -> "RankingScore":                       # TODO: implement constraint. See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.4.
        return

    @staticmethod
    def getBalancedAccuracy (priorPos) -> "RankingScore":                                  # TODO: implement constraint
        return                                                                                      # See :cite:t:`Pierard2025Foundations`, Section A.7.4
    
    @staticmethod
    def getProbabilityTrueNegative (priorPos) -> "RankingScore":                           # TODO: implement constraint
        return                                                                                      # See :cite:t:`Pierard2025Foundations`, Section A.7.4
    
    @staticmethod
    def getProbabilityFalsePositiveComplenent (priorPos) -> "RankingScore":               # TODO: implement constraint
        return
    
    @staticmethod
    def getProbabilityFalseNegativeComplenent (priorPos) -> "RankingScore":               # TODO: implement constraint
        return
    
    @staticmethod
    def getProbabilityTruePositive (priorPos) -> "RankingScore":                           # TODO: implement constraint
        return                                                                                      # See :cite:t:`Pierard2025Foundations`, Section A.7.4
   
    @staticmethod
    def getDetectionRate (priorPos) -> "RankingScore":                                     # TODO: implement constraint
        return
    
    @staticmethod
    def getRejectionRate (priorPos) -> "RankingScore":                                     # TODO: implement constraint
        return
    
    def getName (self):
        return self.name
    
    def __str__ (self):
        return f"Ranking Score: {self.name} with importance {str(self.importance)}"
    