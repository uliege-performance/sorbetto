class ApplicationSpecificPreferences :
	"""This class encodes some application-specific preferences. Currently, it is a random variable, called importance, that gives a positive value to each element of the sample space: tn (for true negative), fp (for false positive), fn (for false negative), and tp (for true positive). See :cite:t:`Pierard2025Foundations` for more information on this topic."""

	def __init__ ( self, itn, ifp, ifn, itp, name=None )
	# All >= 0, not all == 0.
	
	def itn ( self ) -> float # I(tn)
	def itp ( self ) -> float # I(fp)
	def ifn ( self ) -> float # I(fn)
	def itp ( self ) -> float # I(tp)
	
	def __eq__ ( self, other ) # use some tolerance ?
	def __ne__ ( self, other ) # use some tolerance ?
	
	def getName ( self )
	
	def __str__ ( self )
	
	
	
	
	

class RankingScore :

	def __init__ ( self, importance, constraint, name=None )
	
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
	
	def asPencilInROC ( self, priorPos ) -> Pencil
	
	def __call__ ( self, performance ) -> float # should check constraint
	
	@abstractmethod
	def getTrueNegativeRate () -> RankingScore                    # See paper 1, sec A.7.3
	@abstractmethod
	def getTruePositiveRate () -> RankingScore                    # See paper 1, sec A.7.3
	@abstractmethod
	def getSpecificity () -> RankingScore
	@abstractmethod
	def getSelectivity () -> RankingScore
	@abstractmethod
	def getSensitivity () -> RankingScore
	@abstractmethod
	def getNegativePredictiveValue () -> RankingScore             # See paper 1, sec A.7.3
	@abstractmethod
	def getPositivePredictiveValue () -> RankingScore             # See paper 1, sec A.7.3
	@abstractmethod
	def getPrecision () -> RankingScore
	@abstractmethod
	def getInversePrecision () -> RankingScore
	@abstractmethod
	def getRecall () -> RankingScore
	@abstractmethod
	def getInverseRecall () -> RankingScore
	@abstractmethod
	def getIntersectionOverUnion () -> RankingScore
	@abstractmethod
	def getInverseIntersectionOverUnion () -> RankingScore
	@abstractmethod
	def getJaccard () -> RankingScore
	@abstractmethod
	def getInverseJaccard () -> RankingScore
	@abstractmethod
	def getTanimotoCoefficient () -> RankingScore
	@abstractmethod
	def getSimilarity () -> RankingScore
	@abstractmethod
	def getCriticalSuccessIndex () -> RankingScore
	@abstractmethod
	def getF ( beta=1.0 ) -> RankingScore
	@abstractmethod
	def getInverseF ( beta=1.0 ) -> RankingScore
	@abstractmethod
	def getDiceSørensenCoefficient () -> RankingScore
	@abstractmethod
	def getZijdenbosSimilarityIndex () -> RankingScore
	@abstractmethod
	def getCzekanowskiBinaryIndex () -> RankingScore
	@abstractmethod
	def getAccuracy () -> RankingScore                            # See paper 1, sec A.7.3
	@abstractmethod
	def getMatchingCoefficient () -> RankingScore
	
	@abstractmethod
	def getSkewInvariantVersionOfF ( priorPos ) -> RankingScore               # constraint
	@abstractmethod
	def getWeightedAccuracy ( priorPos, weightPos ) -> RankingScore           # constraint
	@abstractmethod
	def getBalancedAccuracy ( priorPos ) -> RankingScore                      # constraint
	                                                              # See paper 1, sec A.7.4
	@abstractmethod
	def getProbabilityTrueNegative ( priorPos ) -> RankingScore               # constraint
	                                                              # See paper 1, sec A.7.4
	@abstractmethod
	def getProbabilityFalsePositiveComplenent ( priorPos ) -> RankingScore    # constraint
	@abstractmethod
	def getProbabilityFalseNegativeComplenent ( priorPos ) -> RankingScore    # constraint
	@abstractmethod
	def getProbabilityTruePositive ( priorPos ) -> RankingScore               # constraint
	                                                              # See paper 1, sec A.7.4
	@abstractmethod
	def getDetectionRate ( priorPos ) -> RankingScore                         # constraint
	@abstractmethod
	def getRejectionRate ( priorPos ) -> RankingScore                         # constraint
	
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
	
	def __invert__ ( self )
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
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 3.2.
	See :cite:t:`Sipka2022TheHitchhikerGuide`
	"""

	def __init__ ( self, srcPriorPos, dstPriorPos, name=None )
	
	def getSrcPriorPos ( self ) -> float
	def getDstPriorPos ( self ) -> float
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance
	
def OpChangePredictedClass ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.1.
	"""

	def __init__ ( self, name=None )
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance
	
def OpChangeGroundtruthClass ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.1.
	"""

	def __init__ ( self, name=None )
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance

def OpSwapPredictedAndGroundtruthClasses ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.1.
	"""

	def __init__ ( self, name=None )
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance

def OpSwapNegativeAndPositiveClasses ( AbstractOperationOnTwoClassClassificationPerformances ) :
	"""
	See :cite:t:`Pierard2024TheTile-arxiv`, Section 4.1.
	"""

	def __init__ ( self, name=None )
	
	def __call__ ( self, performance ) -> TwoClassClassificationPerformance






class AbstractParameterization ( ABC ) :
	"""This is the base class for all possible ways of mapping ranking scores (or, equivalently, importance values, tha is some application-related preferences) onto Tiles. All ranking scores inducing the same performance ordering should be mapped to the same point. It is recommended that the subclasses implement continuous mappings between the four importance values and the two parameters. Also, it is recommended that (1) the ranking scores giving no importance at all to the true positives are mapped to points on the left border (minimal value for the first parameter), (2) the ranking scores giving no importance at all to the true negatives are mapped to points on the right border (maximal value for the first parameter), (3) the ranking scores giving no importance at all to the false positives are mapped to points on the lower border (minimal value for the second parameter), and (4) the ranking scores giving no importance at all to the false negatives are mapped to points on the upper border (minimal value for the second parameter)."""

	def __init__ ( self )

	@abstractmethod
	def getNameParameter1 ( self )

	@abstractmethod
	def getNameParameter2 ( self )

	@abstractmethod
	def getBoundsParameter1 ( self ) -> tuple[float, float]

	@abstractmethod
	def getBoundsParameter2 ( self ) -> tuple[float, float]

	@abstractmethod
	def getCanonicalRankingScore ( self, param1, param2 ) -> RankingScore

	@abstractmethod
	def getValueParameter1 ( self, rankingScore ) -> float

	@abstractmethod
	def getValueParameter2 ( self, rankingScore ) -> float
	
	def locateRankingScore ( self, score ) -> PointInTile                    # ***
	def locateTrueNegativeRate ( self ) -> PointInTile                           # Use ***
	def locateTruePositiveRate ( self ) -> PointInTile                           # Use ***
	def locateSpecificity ( self ) -> PointInTile                                # Use ***
	def locateSelectivity ( self ) -> PointInTile                                # Use ***
	def locateSensitivity ( self ) -> PointInTile                                # Use ***
	def locateNegativePredictiveValue ( self ) -> PointInTile                    # Use ***
	def locatePositivePredictiveValue ( self ) -> PointInTile                    # Use ***
	def locatePrecision ( self ) -> PointInTile                                  # Use ***
	def locateInversePrecision ( self ) -> PointInTile                           # Use ***
	def locateRecall ( self ) -> PointInTile                                     # Use ***
	def locateInverseRecall ( self ) -> PointInTile                              # Use ***
	def locateIntersectionOverUnion ( self ) -> PointInTile                      # Use ***
	def locateInverseIntersectionOverUnion ( self ) -> PointInTile               # Use ***
	def locateJaccard ( self ) -> PointInTile                                    # Use ***
	def locateInverseJaccard ( self ) -> PointInTile                             # Use ***
	def locateTanimotoCoefficient ( self ) -> PointInTile                        # Use ***
	def locateSimilarity ( self ) -> PointInTile                                 # Use ***
	def locateCriticalSuccessIndex ( self ) -> PointInTile                       # Use ***
	def locateF ( self, beta=1.0 ) -> PointInTile                                # Use ***
	def locateInverseF ( self, beta=1.0 ) -> PointInTile                         # Use ***
	def locateDiceSørensenCoefficient ( self ) -> PointInTile                    # Use ***
	def locateZijdenbosSimilarityIndex ( self ) -> PointInTile                   # Use ***
	def locateCzekanowskiBinaryIndex ( self ) -> PointInTile                     # Use ***
	def locateAccuracy ( self ) -> PointInTile                                   # Use ***
	def locateMatchingCoefficient ( self ) -> PointInTile                        # Use ***
	def locateBennettS ( self ) -> PointInTile
	
	# See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
	def locateSimilarityCoefficientsT ( self ) -> PointInTile
	# See :cite:t:`Gower1986Metric` and :cite:t:`Pierard2024TheTile-arxiv`, Section 4.2.
	def locateSimilarityCoefficientsS ( self ) -> PointInTile
	
	def locateStandardizedNegativePredictiveValue ( self, priorPos ) -> PointInTile
	def locateStandardizedPositivePredictiveValue ( self, priorPos ) -> PointInTile
	def locateNegativeLikelihoodRatioComplement ( self, priorPos ) -> PointInTile
	                                                              # See paper 1, sec A.7.4
	def locatePositiveLikelihoodRatio ( self, priorPos ) -> PointInTile
	                                                              # See paper 1, sec A.7.4
	def locateSkewInvariantVersionOfF ( self, priorPos ) -> PointInTile          # Use ***
	def locateWeightedAccuracy ( self, priorPos, weightPos ) -> PointInTile      # Use ***
	def locateBalancedAccuracy ( self, priorPos ) -> PointInTile                 # Use ***
	def locateYoudenJ ( self, priorPos ) -> PointInTile
	def locatePeirceSkillScore ( self, priorPos ) -> PointInTile
	def locateInformedness ( self, priorPos ) -> PointInTile      # See paper 1, sec A.7.4
	def locateCohenKappa ( self, priorPos ) -> PointInTile        # See paper 1, sec A.7.4
	def locateHeidkeSkillScore ( self, priorPos ) -> PointInTile
	def locateProbabilityTrueNegative ( self, priorPos ) -> PointInTile          # Use ***
	def locateProbabilityFalsePositiveComplenent ( self, priorPos ) -> PointInTile # Use ***
	def locateProbabilityFalseNegativeComplenent ( self, priorPos ) -> PointInTile # Use ***
	def locateProbabilityTruePositive ( self, priorPos ) -> PointInTile          # Use ***
	def locateDetectionRate ( self, priorPos ) -> PointInTile                    # Use ***
	def locateRejectionRate ( self, priorPos ) -> PointInTile                    # Use ***
	def locateNormalizedConfusionMatrixDeterminent ( self, priorPos ) -> PointInTile
	
	def locateMarkedness ( ratePos ) -> PointInTile
	def locateClaytonSkillScore ( ratePos ) -> PointInTile
	
	def locateScoresPuttingNoSkillPerformancesOnAnEqualFooting ( priorPos, ratePos ) -> Union[PointInTile, CurveInTile]

	@abstractmethod
	def getName ( self )
	
	def __str__ ( self )
	
	def unitTest ( self )


class ParameterizationDefault ( AbstractParameterization ) :
	"""
	This is the parameterization described in :cite:t:`Pierard2024TheTile-arxiv`.
	"""
	
	def __init__ ( self )
	
class ParameterizationAdaptedToClassPriors ( AbstractParameterization ) :
	"""
	Not yet published. Experimental. In Sébastien's mind.'
	"""
	
	def __init__ ( self )
	
class ParameterizationAdaptedToPredictionRates ( AbstractParameterization ) :
	"""
	Not yet published. Experimental. In Sébastien's mind.'
	"""
	
	def __init__ ( self )






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



.......................







class AbstractTile ( ABC ) :
	"""
	This is the base class for all Tiles.
	Tiles with the default parameterization are studied in detail in :cite:t:`Pierard2024TheTile-arxiv`.
	Various flavors of Tiles are described in :cite:t:`Halin2024AHitchhikers-arxiv-arxiv` and :cite:t:`Pierard2025AMethodology`.
	"""
	
	# TODO : Is is AbstractTile or AbstractFlavor ? Not crystal clear ...
	# Maybe a Tile is a pair of Parameterization and Flavor ?
	
	def __init__ ( self, name, parameterization, resolution=1001, colormap )
	
	@abstractmethod
	def getDefinition ( self ) -> str
	
	@abstractmethod
	def getExplanation ( self ) -> str
	
	def getParameterization ( self ) -> AbstractParameterization
	
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
	
	@abstractmethod
	def __call__ ( self, param1, param2 )

	def getName ( self )
	
	def __str__ ( self )
	
class AbstractNumericTile ( AbstractTile ) :
	
	def __init__ ( self, name, parameterization, resolution=1001, colormap )

	@abstractmethod
	def getLowerBound ( self )

	@abstractmethod
	def getUpperBound ( self )

	@abstractmethod
	def minimize ( self ) -> PointInTile
	
	@abstractmethod
	def maximize ( self ) -> PointInTile
	
	@abstractmethod
	def intergate ( self ) -> float
	
	@staticmethod
	def getDefaultColormapForValueTiles ()
	
	@staticmethod
	def getDefaultColormapForRankingTiles ()
	
	@staticmethod
	def getDefaultColormapForCorrelationTiles ()
	
class AbstractSymbolicTile ( AbstractTile ) :
	
	def __init__ ( self, name, parameterization, resolution=1001, colormap ) # TODO: how can we specify the color code?

	@abstractmethod
	def getCodomain ( self ) -> set
	
class ValueTile ( AbstractNumericTile ) :

	def getVUT ( self )
		"""
		See :cite:t:`Pierard2024TheTile-arxiv`, Section 3.1.
		"""
	
	def asPencil ( self ) -> Pencil



	


	




class AbstractAnalysis ( ABC ) :

	def __init__ ( self, parameterization, resolution=1001 )
	
	def genTiles ( self ) # generator
	
class AnalysisForTheoreticalAnalyst ( AbstractAnalysis ) :

	def __init__ ( self, performances, score, parameterization, resolution=1001, options )

	def getPearsonCorrelationTile ( self ) -> AbstractNumericTile
	
	def getKendallCorrelationTile ( self ) -> AbstractNumericTile
	
	def getSpearmanCorrelationTile ( self ) -> AbstractNumericTile

class AnalysisForMethodDesigner ( AbstractAnalysis ) :

	def __init__ ( self, performance, competitors, parameterization, resolution=1001, options )
	
	def getNoSkillTile ( self ) -> AbstractNumericTile
	
	def getBaselineValueTile ( self ) -> AbstractNumericTile
	
	def getStateOfTheArtValueTile ( self ) -> AbstractNumericTile
	
	def getValueTile ( self ) -> AbstractNumericTile
	
	def getRankingTile ( self ) -> AbstractNumericTile
	
	def drawInROC ( self, fig, ax ) # and options ?
	
	def getAdvice ( self, fmt ) -> str # fmt can be: txt, html, latex
	
class AnalysisForBenchmarker ( AbstractAnalysis ) :

	def __init__ ( self, performances, parameterization, resolution=1001, options )
	
	def drawInROC ( self, fig, ax ) # and options ?
	
	def getValueTile ( self, entity ) -> AbstractNumericTile
	
	def getNoSkillTile ( self ) -> AbstractNumericTile
	
	def getRelativeSkillTile ( self ) -> AbstractNumericTile
	
	def getRankingTile ( self, entity ) -> AbstractNumericTile
	
	def getAdviceBasedOnRankingTiles ( self, fmt ) -> str # fmt can be: txt, html, latex
	
	def getEntityTile ( self, rank ) -> AbstractSymbolicTile
	
	def getAdviceBasedOnEntityTiles ( self, fmt ) -> str # fmt can be: txt, html, latex
	
class AnalysisForAppDeveloper ( AbstractAnalysis ) :

	def __init__ ( self, min_a, max_a, min_b, max_b, performances, parameterization, resolution=1001, options )
	
	def getEntityTile ( self, rank ) -> AbstractSymbolicTile
	
	def getValueTile ( self, entity ) -> AbstractNumericTile
	
	def getAdvice ( self, fmt ) -> str # fmt can be: txt, html, latex
	


