class ApplicationSpecificPreferences :

	def __init__ ( self, itn, ifp, ifn, itp, name=None )
	# All >= 0, not all == 0.
	
	def itn ( self ) -> float # I(tn)
	def itp ( self ) -> float # I(fp)
	def ifn ( self ) -> float # I(fn)
	def itp ( self ) -> float # I(tp)
	
	def __eq__ ( self, other ) # use some tolerance ?
	def __ne__ ( self, other ) # use some tolerance ?
	
	def getName ( self )
	
	def __str__ ()
	
	
	
	
	

class RankingScore :

	def __init__ ( self, importance, constraint, name=None )
	
	def getImportance () -> ApplicationSpecificPreferences
	
	def isCanonical ( tol=1e-8 ) -> bool
	
	def plotInROC ( self, fig, ax, priorPos )
	
	def __call__ ( self, performance ) -> float # should check constraint
	
	@abstractmethod
	def getTrueNegativeRate () -> RankingScore
	@abstractmethod
	def getTruePositiveRate () -> RankingScore
	@abstractmethod
	def getSpecificity () -> RankingScore
	@abstractmethod
	def getSelectivity () -> RankingScore
	@abstractmethod
	def getSensitivity () -> RankingScore
	@abstractmethod
	def getNegativePredictiveValue () -> RankingScore
	@abstractmethod
	def getPositivePredictiveValue () -> RankingScore
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
	def getAccuracy () -> RankingScore
	@abstractmethod
	def getMatchingCoefficient () -> RankingScore
	
	@abstractmethod
	def getSkewInvariantVersionOfF ( priorPos ) -> RankingScore               # constraint
	@abstractmethod
	def getWeightedAccuracy ( priorPos, weightPos ) -> RankingScore           # constraint
	@abstractmethod
	def getBalancedAccuracy ( priorPos ) -> RankingScore                      # constraint
	@abstractmethod
	def getProbabilityTrueNegative ( priorPos ) -> RankingScore               # constraint
	@abstractmethod
	def getProbabilityFalsePositiveComplenent ( priorPos ) -> RankingScore    # constraint
	@abstractmethod
	def getProbabilityFalseNegativeComplenent ( priorPos ) -> RankingScore    # constraint
	@abstractmethod
	def getProbabilityTruePositive ( priorPos ) -> RankingScore               # constraint
	@abstractmethod
	def getDetectionRate ( priorPos ) -> RankingScore                         # constraint
	@abstractmethod
	def getRejectionRate ( priorPos ) -> RankingScore                         # constraint
	
	def getName ( self )
	
	def __str__ ()
	
	
	
	
	
	

class PerformanceOrderingInducedByOneScore : # It is a preorder

	def __init__ ( self, score, name=None )
	# warning if score is not a RankingScore.
	
	def __call__ ( self, p1, p2 ) -> bool # Theorem 1 of paper 1.
	
	# TODO: should we have some tolerance ? Instead of bool, one could have {yes, perhaps, no}.
	
	# We have four cases depending on the results of self(p1, p2) and self(p2, p1).
	def equivalent ( self, p1, p2 ) -> bool
	def better ( self, p1, p2 ) -> bool
	def worse ( self, p1, p2 ) -> bool
	def incomparable ( self, p1, p2 ) -> bool
	
	# TODO: do we want the 10 relationships?
	# - we can choose if we accept equivalent
	# - we can choose if we accept better
	# - we can choose if we accept worse
	# - we can choose if we accept incomparable
	# There are 10, and not 2^4=16 interesting relationships because:
	# - we need to accept at least one;
	# - we need to not accept at least one;
	# - and accepting only one is already in the four above methods.
	def worseOrEquivalent ( self, p1, p2 ) -> bool
	def betterOrEquivalent ( self, p1, p2 ) -> bool
	def comparable ( self, p1, p2 ) -> bool
	# TODO ...
	
	def getName ( self )
	
	def __str__ ()







class TwoClassClassificationPerformance :
	"""A two-class (crisp) classification performance $P$ is a probability measure over the measurable space $(\Omega,\Sigma)$ where the sample (a.k.a. universe) is $\Omega=\{tn,fp,fn,tp\}$ and the event space is $\Sigma=2^\Omega$. By convention, $tn$, $fp$, $fn$, and $tp$ represent the four cases that can arise: a true negative, a false positive, a false negative, and a true positive, respectively. The four elementary probability measures $P(\{tn\})$, $P(\{fp\})$, $P(\{fn\})$, and $P(\{tp\})$ are the elements of the normalized confusion matrix. See :cite:t:`Pierard2025Foundations` for more information on this topic."""

	def __init__ ( self, ptn, pfp, pfn, ptp, name=None )
	
	def ptn ( self ) -> float # P({tn})
	def pfp ( self ) -> float # P({fp})
	def pfn ( self ) -> float # P({fn})
	def ptp ( self ) -> float # P({tp})
	
	def __eq__ ( self, other ) # use some tolerance ?
	def __ne__ ( self, other ) # use some tolerance ?

	@staticmethod
	def buildFromRankingScoreValues ( name, * pairsOfRankingScoresAndValues, tol=1e-3 ) -> Self
	
	def plotInROC ( self, fig, ax )
	def getValueTile ( self, parameterization ) # and options ?
	
	def getName ( self )
	
	def __str__ ()

class FiniteSetOfTwoClassClassificationPerformances ( list[TwoClassClassificationPerformance] ) :
	# TODO: list or dict ?
	# TODO: FiniteSet or Multiset ?

	def __init__ ( self, name )
	
	def getMean ( self ) -> TwoClassClassificationPerformances
	"""
	The mean is know as the summarized performance as well as Fawcett's interpolated performance.
	"""
	
	def getRange ( self, score ) -> tuple[float, float]
	
	def plotInROC ( self, fig, ax ) # and options ?
	
	def getWorstValueTile ( self, parameterization ) # and options ?
	def getBestValueTile ( self, parameterization ) # and options ?
	
	def getName ( self )
	
	def __str__ ()
	
class AbstractDistributionOfTwoClassClassificationPerformances ( ABC ) :

	def __init__ ( self )
	
	@abstractmethod
	def drawAtRandom ( self, numPerformances ) -> FiniteSetOfTwoClassClassificationPerformances
	
	@abstractmethod
	def getMean ( self ) -> TwoClassClassificationPerformances

	@abstractmethod
	def getName ( self )
	
	def __str__ ()

class UniformDistributionOfTwoClassClassificationPerformances ( AbstractDistributionOfTwoClassClassificationPerformances )

class UniformDistributionOfTwoClassClassificationPerformancesForFixedClassPriors ( AbstractDistributionOfTwoClassClassificationPerformances )

class UniformDistributionOfTwoClassClassificationPerformancesForFixedPredictionRates ( AbstractDistributionOfTwoClassClassificationPerformances )











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
	
	def locateRankingScore ( score ) -> PointInTile                    # ***
	def locateTrueNegativeRate () -> PointInTile                                 # Use ***
	def locateTruePositiveRate () -> PointInTile                                 # Use ***
	def locateSpecificity () -> PointInTile                                      # Use ***
	def locateSelectivity () -> PointInTile                                      # Use ***
	def locateSensitivity () -> PointInTile                                      # Use ***
	def locateNegativePredictiveValue () -> PointInTile                          # Use ***
	def locatePositivePredictiveValue () -> PointInTile                          # Use ***
	def locatePrecision () -> PointInTile                                        # Use ***
	def locateInversePrecision () -> PointInTile                                 # Use ***
	def locateRecall () -> PointInTile                                           # Use ***
	def locateInverseRecall () -> PointInTile                                    # Use ***
	def locateIntersectionOverUnion () -> PointInTile                            # Use ***
	def locateInverseIntersectionOverUnion () -> PointInTile                     # Use ***
	def locateJaccard () -> PointInTile                                          # Use ***
	def locateInverseJaccard () -> PointInTile                                   # Use ***
	def locateTanimotoCoefficient () -> PointInTile                              # Use ***
	def locateSimilarity () -> PointInTile                                       # Use ***
	def locateCriticalSuccessIndex () -> PointInTile                             # Use ***
	def locateF ( beta=1.0 ) -> PointInTile                                      # Use ***
	def locateInverseF ( beta=1.0 ) -> PointInTile                               # Use ***
	def locateDiceSørensenCoefficient () -> PointInTile                          # Use ***
	def locateZijdenbosSimilarityIndex () -> PointInTile                         # Use ***
	def locateCzekanowskiBinaryIndex () -> PointInTile                           # Use ***
	def locateAccuracy () -> PointInTile                                         # Use ***
	def locateMatchingCoefficient () -> PointInTile                              # Use ***
	def locateBennettS () -> PointInTile
	
	def locateStandardizedNegativePredictiveValue ( priorPos ) -> PointInTile
	def locateStandardizedPositivePredictiveValue ( priorPos ) -> PointInTile
	def locateNegativeLikelihoodRatioComplement ( priorPos ) -> PointInTile
	def locatePositiveLikelihoodRatio ( priorPos ) -> PointInTile
	def locateSkewInvariantVersionOfF ( priorPos ) -> PointInTile                # Use ***
	def locateWeightedAccuracy ( priorPos, weightPos ) -> PointInTile            # Use ***
	def locateBalancedAccuracy ( priorPos ) -> PointInTile                       # Use ***
	def locateYoudenJ ( priorPos ) -> PointInTile
	def locatePeirceSkillScore ( priorPos ) -> PointInTile
	def locateInformedness ( priorPos ) -> PointInTile
	def locateCohenKappa ( priorPos ) -> PointInTile
	def locateHeidkeSkillScore ( priorPos ) -> PointInTile
	def locateProbabilityTrueNegative ( priorPos ) -> PointInTile                # Use ***
	def locateProbabilityFalsePositiveComplenent ( priorPos ) -> PointInTile     # Use ***
	def locateProbabilityFalseNegativeComplenent ( priorPos ) -> PointInTile     # Use ***
	def locateProbabilityTruePositive ( priorPos ) -> PointInTile                # Use ***
	def locateDetectionRate ( priorPos ) -> PointInTile                          # Use ***
	def locateRejectionRate ( priorPos ) -> PointInTile                          # Use ***
	def locateNormalizedConfusionMatrixDeterminent ( priorPos ) -> PointInTile
	
	def locateMarkedness ( ratePos ) -> PointInTile
	def locateClaytonSkillScore ( ratePos ) -> PointInTile
	
	def locateScoresPuttingNoSkillPerformancesOnAnEqualFooting ( priorPos, ratePos ) -> Union[PointInTile, CurveInTile]

	@abstractmethod
	def getName ( self )
	
	def __str__ ()
	
	def unitTest ()


class ParameterizationDefault ( AbstractParameterization ) :
	"""This is the parameterization described in: Sébastien Piérard, Anaïs Halin, Anthony Cioppa, Adrien Deliège, and Marc Van Droogenbroeck. The Tile: A 2D map of ranking scores for two-class classification. arXiv, abs/2412.04309, 2024."""
	
	def __init__ ( self )
	
class ParameterizationAdaptedToClassPriors ( AbstractParameterization ) :
	"""Not yet published. Experimental. In Sébastien's mind.'"""
	
	def __init__ ( self )
	
class ParameterizationAdaptedToPredictionRates ( AbstractParameterization ) :
	"""Not yet published. Experimental. In Sébastien's mind."""
	
	def __init__ ( self )









class AbstractTile ( ABC ) :
	"""This is the base class for all Tiles."""
	
	def __init__ ( self, parameterization )
	
	@abstractmethod
	def getDefinition ( self )
	
	@abstractmethod
	def getExplanation ( self )
	
	def getParameterization ( self )
	
	def getAnnotations ( self ) # generator
	
	def addAnnotation ( self, annotation )
	
	def delAnnotation ( self, annotation )
	
	
	@abstractmethod
	def plot ( self, fig, ax )
	
	@abstractmethod
	def __call__ ( self, param1, param2 )

	@abstractmethod
	def getName ( self )
	
	def __str__ ()
	
class AbstractNumericTile ( AbstractTile ) :
	
	def __init__ ( self )

	@abstractmethod
	def getLowerBound ()

	@abstractmethod
	def getUpperBound ()

	@abstractmethod
	def minimize () -> PointInTile
	
	@abstractmethod
	def maximize () -> PointInTile
	
	@abstractmethod
	def intergate () -> float
	
class AbstractSymbolicTile ( AbstractTile ) :
	
	def __init__ ( self ) # TODO: how can we specify the color code?

	@abstractmethod
	def getCodomain () -> set
	








class ValueTile ( AbstractNumericTile ) :
	
	def __init__ ( self, performance )
	
	def getVUT () -> float
	
class CorrelationTile ( AbstractNumericTile ) :
	
	def __init__ ( self, performances, score )
	
class RankingTile ( AbstractNumericTile ) :
	
	def __init__ ( self, entities, entity ) # TODO: do we need a class for Entity or is Performance enough ?
	
class EntityTile ( AbstractSymbolicTile ) :
	
	def __init__ ( self, ?????????? )
	
	


	









class AnalysisForRanking ( AbstractAnalysis? ) :

	def __init__ ( self, parameterization, resolution=1024, maxCacheSize=1024**3,  )










