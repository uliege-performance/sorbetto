class RankingScore :

	def __init__ ( self, importance, constraint=None, name=None )
	
	def getImportance () -> ApplicationSpecificPreferences
	
	def isCanonical ( tol=1e-8 ) -> bool
		"""
		See :cite:t:`Pierard2024TheTile-arxiv`, Definition 1.
		"""
	
	def toPABDC () -> RankingScore
		"""
		See :cite:t:`Pierard2024TheTile-arxiv`, Example 3.
		"""
	
	def drawInROC ( self, fig, ax, priorPos )
	
	def getPencilInROC ( self, priorPos ) -> Pencil
	
	def __call__ ( self, performance ) -> float # should check constraint
	
	@staticmethod
	def getTrueNegativeRate () -> RankingScore                                            # See :cite:t:`Pierard2025Foundations`, Section A.7.3
		"""
		True Negative Rate (TNR).
		Synonyms: specificity, selectivity, inverse recall.
		"""
	@staticmethod
	def getTruePositiveRate () -> RankingScore                                            # See :cite:t:`Pierard2025Foundations`, Section A.7.3
		"""
		True Positive Rate (TPR).
		Synonyms: sensitivity, recall.
		"""
	@staticmethod
	def getSpecificity () -> RankingScore
	@staticmethod
	def getSelectivity () -> RankingScore
	@staticmethod
	def getSensitivity () -> RankingScore
	@staticmethod
	def getNegativePredictiveValue () -> RankingScore                                     # See :cite:t:`Pierard2025Foundations`, Section A.7.3
		"""
		Negative Predictive Value (NPV).
		Synonym: inverse precision
		"""
	@staticmethod
	def getPositivePredictiveValue () -> RankingScore                                     # See :cite:t:`Pierard2025Foundations`, Section A.7.3
		"""
		Positive Predictive Value (PPV).
		Synonym: precision
		"""
	@staticmethod
	def getPrecision () -> RankingScore
	@staticmethod
	def getInversePrecision () -> RankingScore
	@staticmethod
	def getRecall () -> RankingScore
	@staticmethod
	def getInverseRecall () -> RankingScore
	@staticmethod
	def getIntersectionOverUnion () -> RankingScore
	@staticmethod
	def getInverseIntersectionOverUnion () -> RankingScore
	@staticmethod
	def getJaccard () -> RankingScore
		"""
		Jaccard's coefficient.
		Synonyms: Tanimoto coefficient, similarity, Intersection over Union (IoU), critical success index :cite:t:`Hogan2010Equitability`, and G-measure :cite:t:`Flach2003TheGeometry` (not to be confused with the G-measure of :cite:t:`Canbek2017Binary` and other authors).
		"""
	@staticmethod
	def getInverseJaccard () -> RankingScore
	@staticmethod
	def getTanimotoCoefficient () -> RankingScore
	@staticmethod
	def getSimilarity () -> RankingScore
	@staticmethod
	def getCriticalSuccessIndex () -> RankingScore
	@staticmethod
	def getF ( beta=1.0 ) -> RankingScore                                                 # See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.2.
	@staticmethod
	def getInverseF ( beta=1.0 ) -> RankingScore
	@staticmethod
	def getDiceSorensenCoefficient () -> RankingScore
	@staticmethod
	def getZijdenbosSimilarityIndex () -> RankingScore
	@staticmethod
	def getCzekanowskiBinaryIndex () -> RankingScore
	@staticmethod
	def getAccuracy () -> RankingScore                                                    # See :cite:t:`Pierard2025Foundations`, Section A.7.3
	@staticmethod
	def getMatchingCoefficient () -> RankingScore
	
	@staticmethod
	def getSkewInsensitiveVersionOfF ( priorPos ) -> RankingScore                         # TODO: implement constraint
		"""
		The skew-insensitive version of $\scoreFOne$.
		Defined in cite:t:`Flach2003TheGeometry`.
		"""
	@staticmethod
	def getWeightedAccuracy ( priorPos, weightPos ) -> RankingScore                       # TODO: implement constraint. See :cite:t:`Pierard2024TheTile-arxiv`, Section A.3.4.
	@staticmethod
	def getBalancedAccuracy ( priorPos ) -> RankingScore                                  # TODO: implement constraint
	                                                                                      # See :cite:t:`Pierard2025Foundations`, Section A.7.4
	@staticmethod
	def getProbabilityTrueNegative ( priorPos ) -> RankingScore                           # TODO: implement constraint
	                                                                                      # See :cite:t:`Pierard2025Foundations`, Section A.7.4
	@staticmethod
	def getProbabilityFalsePositiveComplenent ( priorPos ) -> RankingScore                # TODO: implement constraint
	@staticmethod
	def getProbabilityFalseNegativeComplenent ( priorPos ) -> RankingScore                # TODO: implement constraint
	@staticmethod
	def getProbabilityTruePositive ( priorPos ) -> RankingScore                           # TODO: implement constraint
	                                                                                      # See :cite:t:`Pierard2025Foundations`, Section A.7.4
	@staticmethod
	def getDetectionRate ( priorPos ) -> RankingScore                                     # TODO: implement constraint
	@staticmethod
	def getRejectionRate ( priorPos ) -> RankingScore                                     # TODO: implement constraint
	
	def getName ( self )
	
	def __str__ ( self )
	
	
	
	
	
	

class AbstractHomogeneousBinaryRelationOnPerformances :

	def __init__ ( self, name=None, known_properties=None )

	# TODO: should we have some tolerance ? Instead of bool, one could have {yes, perhaps, no}.
	@abstractmethod
	def __call__ ( self, p1, p2 ) -> bool
	
	@abstractmethod
	def isReflexive ( self ) -> bool
	@abstractmethod
	def isIrreflexive ( self ) -> bool
	@abstractmethod
	def isTransitive ( self ) -> bool
	@abstractmethod
	def isSymmetric ( self ) -> bool
	@abstractmethod
	def isAsymmetric ( self ) -> bool
	@abstractmethod
	def isAntisymmetric ( self ) -> bool
	@abstractmethod
	def isEquivalence ( self ) -> bool
	@abstractmethod
	def isPreorder ( self ) -> bool
	@abstractmethod
	def isOrder ( self ) -> bool
	@abstractmethod
	def isPartialOrder ( self ) -> bool
	@abstractmethod
	def isTotalOrder ( self ) -> bool
	
	def __invert__ ( self ) # dual
	def __and__ ( self, other )
	def __or__ ( self, other )
	
	def getName ( self )
	
	def __str__ ( self )
	
	

class PerformanceOrderingInducedByOneScore ( AbstractHomogeneousBinaryRelationOnPerformances ) : # It is a preorder

	def __init__ ( self, score, name=None )
	# warning if score is not a RankingScore.
	
	def __call__ ( self, p1, p2 ) -> bool # Theorem 1 of :cite:t:`Pierard2025Foundations`.
	
	# We have four cases depending on the results of self(p1, p2) and self(p2, p1).
	def getRelationEquivalent ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances
	def getRelationBetter ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances
	def getRelationWorse ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances
	def getRelationIncomparable ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances
	
	# TODO: do we want the 10 relationships?
	# - we can choose if we accept equivalent
	# - we can choose if we accept better
	# - we can choose if we accept worse
	# - we can choose if we accept incomparable
	# There are 10, and not 2^4=16 interesting relationships because:
	# - we need to accept at least one;
	# - we need to not accept at least one;
	# - and accepting only one is already in the four above methods.
	def getRelationWorseOrEquivalent ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances
	def getRelationBetterOrEquivalent ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances
	def getRelationComparable ( self ) -> AbstractHomogeneousBinaryRelationOnPerformances
	# TODO ...
	
	def getName ( self )
	
	def __str__ ( self )







class TwoClassClassificationPerformance :
	"""A two-class (crisp) classification performance $P$ is a probability measure over the measurable space $(\Omega,\Sigma)$ where the sample (a.k.a. universe) is $\Omega=\{tn,fp,fn,tp\}$ and the event space is $\Sigma=2^\Omega$. By convention, $tn$, $fp$, $fn$, and $tp$ represent the four cases that can arise: a true negative, a false positive, a false negative, and a true positive, respectively. The four elementary probability measures $P(\{tn\})$, $P(\{fp\})$, $P(\{fn\})$, and $P(\{tp\})$ are the elements of the normalized confusion matrix. See :cite:t:`Pierard2025Foundations` for more information on this topic."""

	def __init__ ( self, ptn, pfp, pfn, ptp, name=None )
	
	def ptn ( self ) -> float # P({tn})
	def pfp ( self ) -> float # P({fp})
	def pfn ( self ) -> float # P({fn})
	def ptp ( self ) -> float # P({tp})
	
	def isNoSkill ( self, tol ) -> bool
	def isAboveNoSkills ( self, tol ) -> bool
	def isBelowNoSkills ( self, tol ) -> bool
	
	def __eq__ ( self, other ) # use some tolerance ?
	def __ne__ ( self, other ) # use some tolerance ?

	@staticmethod
	def buildFromRankingScoreValues ( name, * pairsOfRankingScoresAndValues, tol=1e-3 ) -> Self
	
	def drawInROC ( self, fig, ax )
	def getValueTile ( self, parameterization ) # and options ?
	
	def getName ( self )
	
	def __str__ ( self )

class FiniteSetOfTwoClassClassificationPerformances ( list[TwoClassClassificationPerformance] ) :
	# TODO: list or dict ?
	# TODO: FiniteSet or Multiset ?

	def __init__ ( self, name )
	
	def getMean ( self ) -> TwoClassClassificationPerformances
	"""
	The mean is know as the summarized performance as well as Fawcett's interpolated performance.
	"""
	
	def getRange ( self, score ) -> tuple[float, float]
	
	def drawInROC ( self, fig, ax ) # and options ?
	
	def getWorstValueTile ( self, parameterization ) # and options ?
	def getBestValueTile ( self, parameterization ) # and options ?
	
	def getName ( self )
	
	def __str__ ( self )
	
class AbstractDistributionOfTwoClassClassificationPerformances ( ABC ) :

	def __init__ ( self )
	
	# def getSupport () -> ???
	
	@abstractmethod
	def drawAtRandom ( self, numPerformances ) -> FiniteSetOfTwoClassClassificationPerformances
	
	@abstractmethod
	def getMean ( self ) -> FiniteSetOfTwoClassClassificationPerformances

	@abstractmethod
	def getName ( self )
	
	def __str__ ( self )

class UniformDistributionOfTwoClassClassificationPerformances ( AbstractDistributionOfTwoClassClassificationPerformances )
	
	def sampleOnRegularGrid ( self, grid_size ) -> FiniteSetOfTwoClassClassificationPerformances

class UniformDistributionOfTwoClassClassificationPerformancesForFixedClassPriors ( AbstractDistributionOfTwoClassClassificationPerformances )
	
	def sampleOnRegularGrid ( self, grid_size ) -> FiniteSetOfTwoClassClassificationPerformances

class UniformDistributionOfTwoClassClassificationPerformancesForFixedPredictionRates ( AbstractDistributionOfTwoClassClassificationPerformances )
	
	def sampleOnRegularGrid ( self, grid_size ) -> FiniteSetOfTwoClassClassificationPerformances








def AbstractOperationOnTwoClassClassificationPerformances ( ABC ) :

	def __init__ ( self, name=None )
	
	@abstractmethod
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance
	
	def getName ( self )
	
	def __str__ ( self )

def OpFilter ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2025Foundations`, Property 1.
	"""

	def __init__ ( self, importances, name=None )
	
	def getImportances ( self ) -> ApplicationSpecificPreferences
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance

def OpNoSkill  ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 2.2.
	"""

	def __init__ ( self, name=None )
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance

def OpClassPriorShift ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 3.2 and Lemma 5.
	See :cite:t:`Sipka2022TheHitchhikerGuide`
	"""

	def __init__ ( self, srcPriorPos, dstPriorPos, name=None )
	
	def getSrcPriorPos ( self ) -> float
	def getDstPriorPos ( self ) -> float
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance
	
def OpChangePredictedClass ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.1 and Lemma 1.
	"""

	def __init__ ( self, name=None )
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance
	
def OpChangeGroundtruthClass ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.1 and Lemma 2.
	"""

	def __init__ ( self, name=None )
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance

def OpSwapPredictedAndGroundtruthClasses ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.1 and Lemma 3.
	"""

	def __init__ ( self, name=None )
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance

def OpSwapNegativeAndPositiveClasses ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.1 and Lemma 4.
	"""

	def __init__ ( self, name=None )
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance















class AbstractAnnotation ( ABC ) :
	"""
	This is the base class for all annotations, which are things that are drawn on top of Tiles.
	"""
	
	def __init__ ( self, name )
	
	@abstractmethod
	def draw ( self, tile, fig, ax )

	def getName ( self )
	
	def __str__ ( self )
	
class AnnotationPoint ( AbstractAnnotation ) :

	def __init__ ( self, point_or_score_or_ordering_or_preferences, label, ... ) # options for fontsize, fontcolor, markersize, markercolor, marker, etc.
	
	def getPoint ( self )
	
	def getLabel ( self )
	
class AnnotationCurve ( AbstractAnnotation ) :

	def __init__ ( self, curve, label, ... ) # options for color, linestyle, linewidth
	
	def getCurve ( self )

class AnnotationClassPriorShiftGrid ( AbstractAnnotation ) :
	# See :cite:t:`Pierard2024TheTile-arxiv`, Section A.2.2 
	# See :cite:t:`Pierard2024TheTile-arxiv`, Figure 8

	def __init__ ( self, srcPriorPos, dstPriorPos, ... )
	
	def getSrcPriorPos ( self ) -> float
	def getDstPriorPos ( self ) -> float
	
class AnnotationEntityName ( AbstractAnnotation ) :
	
	def __init__ ( self )
	
	

+ zones hachurées des no-skills.






class AbstractTile ( ABC ) :
	"""
	This is the base class for all Tiles.
	Tiles with the default parameterization are studied in detail in :cite:t:`Pierard2024TheTile-arxiv`.
	Various flavors of Tiles are described in :cite:t:`Halin2024AHitchhikers-arxiv` and :cite:t:`Pierard2025AMethodology`.
	"""
	
	def __init__ ( self, name, parameterization, flavor, resolution=1001, ... )
	
	@abstractmethod
	def getExplanation ( self ) -> str
	
	def getParameterization ( self ) -> AbstractParameterization
	
	def getFlavor ( self ) -> AbstractFlavor
	
	def getResolution ( self ) -> int
	
	def getVecParam1 ( self ) -> nparray
	def getVecParam2 ( self ) -> nparray 
	def getMat ( self ) -> nparray
	
	def getColormap ( self )
	
	# annotations : List [ Annotation ]
	
	def genAnnotations ( self ) # generator
	
	def addAnnotation ( self, annotation )
	
	def delAnnotation ( self, annotation )
	
	@abstractmethod
	def draw ( self, fig, ax )
	
	def __call__ ( self, param1, param2 ) # uses `flavor ( importances )`.

	def getName ( self )
	
	def __str__ ( self )
	
class AbstractNumericTile ( AbstractTile ) :
	
	def __init__ ( self, name, parameterization, numeric_flavor, resolution=1001, ... )

	@abstractmethod
	def minimize ( self ) -> PointInTile
	
	@abstractmethod
	def maximize ( self ) -> PointInTile
	
	@abstractmethod
	def intergate ( self ) -> float
	
class AbstractSymbolicTile ( AbstractTile ) :
	
	def __init__ ( self, name, parameterization, symbolic_flavor, resolution=1001, ... )
	




class ValueTile ( AbstractNumericTile ) :

	def getVUT ( self )
		"""
		See :cite:t:`Pierard2024TheTile-arxiv`, Section 3.1. (with default parameterization)
		"""
	
	def asPencil ( self ) -> Pencil
	
class CorrelationTile ( AbstractNumericTile )
class RankingTile ( AbstractNumericTile )
class EntityTile ( AbstractSymbolicTile )


	



class PointInTile :
	pass
	
class CurveInTile :
	pass
	




class AbstractAnalysis ( ABC ) :

	def __init__ ( self, parameterization, resolution=1001 )
	
	def genTiles ( self ) # generator
	
class AnalysisForTheoreticalAnalyst ( AbstractAnalysis ) :
	"""
	For an example, see :cite:t:`Pierard2024TheTile-arxiv`, Figure 4.
	For an example, see :cite:t:`Pierard2024TheTile-arxiv`, Figure 7.
	"""

	def __init__ ( self, performances, score, parameterization, resolution=1001, options )

	def getPearsonCorrelationTile ( self ) -> AbstractNumericTile
	
	def getKendallCorrelationTile ( self ) -> AbstractNumericTile
	
	def getSpearmanCorrelationTile ( self ) -> AbstractNumericTile

class AnalysisForMethodDesigner ( AbstractAnalysis ) :

	def __init__ ( self, performance, competitors, parameterization, resolution=1001, options )
	
	def getNoSkillTile ( self ) -> AbstractNumericTile # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 9.
	
	def getBaselineValueTile ( self ) -> AbstractNumericTile
	
	def getStateOfTheArtValueTile ( self ) -> AbstractNumericTile
	
	def getValueTile ( self ) -> ValueTile
	
	def getRankingTile ( self ) -> AbstractNumericTile
	
	def drawInROC ( self, fig, ax ) # and options ?
	
	def getAdvice ( self, fmt ) -> str # fmt can be: txt, html, latex
	
class AnalysisForBenchmarker ( AbstractAnalysis ) :

	def __init__ ( self, performances, parameterization, resolution=1001, options )
	
	def drawInROC ( self, fig, ax ) # and options ?
	
	def getValueTile ( self, entity ) -> ValueTile
	
	def getNoSkillTile ( self ) -> AbstractNumericTile # See :cite:t:`Pierard2024TheTile-arxiv`, Figure 9.
	
	def getRelativeSkillTile ( self ) -> AbstractNumericTile
	
	def getRankingTile ( self, entity ) -> AbstractNumericTile
	
	def getAdviceBasedOnRankingTiles ( self, fmt ) -> str # fmt can be: txt, html, latex
	
	def getEntityTile ( self, rank ) -> AbstractSymbolicTile
	
	def getAdviceBasedOnEntityTiles ( self, fmt ) -> str # fmt can be: txt, html, latex
	
class AnalysisForAppDeveloper ( AbstractAnalysis ) :

	def __init__ ( self, min_a, max_a, min_b, max_b, performances, parameterization, resolution=1001, options )
	
	def getEntityTile ( self, rank ) -> AbstractSymbolicTile
	
	def getValueTile ( self, entity ) -> ValueTile
	
	def getAdvice ( self, fmt ) -> str # fmt can be: txt, html, latex
	


