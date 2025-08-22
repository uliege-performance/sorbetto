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
	
	def __str__ ( self )
	
	
	
	
	
	

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
	
	def __str__ ( self )







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
	
	def plotInROC ( self, fig, ax ) # and options ?
	
	def getWorstValueTile ( self, parameterization ) # and options ?
	def getBestValueTile ( self, parameterization ) # and options ?
	
	def getName ( self )
	
	def __str__ ( self )
	
class AbstractDistributionOfTwoClassClassificationPerformances ( ABC ) :

	def __init__ ( self )
	
	@abstractmethod
	def drawAtRandom ( self, numPerformances ) -> FiniteSetOfTwoClassClassificationPerformances
	
	@abstractmethod
	def getMean ( self ) -> TwoClassClassificationPerformances

	@abstractmethod
	def getName ( self )
	
	def __str__ ( self )

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
	
	def locateStandardizedNegativePredictiveValue ( self, priorPos ) -> PointInTile
	def locateStandardizedPositivePredictiveValue ( self, priorPos ) -> PointInTile
	def locateNegativeLikelihoodRatioComplement ( self, priorPos ) -> PointInTile
	def locatePositiveLikelihoodRatio ( self, priorPos ) -> PointInTile
	def locateSkewInvariantVersionOfF ( self, priorPos ) -> PointInTile          # Use ***
	def locateWeightedAccuracy ( self, priorPos, weightPos ) -> PointInTile      # Use ***
	def locateBalancedAccuracy ( self, priorPos ) -> PointInTile                 # Use ***
	def locateYoudenJ ( self, priorPos ) -> PointInTile
	def locatePeirceSkillScore ( self, priorPos ) -> PointInTile
	def locateInformedness ( self, priorPos ) -> PointInTile
	def locateCohenKappa ( self, priorPos ) -> PointInTile
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
	
	def __init__ ( self, parameterization, resolution=1001, colormap )
	
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
	
	def genAnnotations ( self ) # generator
	
	def addAnnotation ( self, annotation )
	
	def delAnnotation ( self, annotation )
	
	@abstractmethod
	def plot ( self, fig, ax )
	
	@abstractmethod
	def __call__ ( self, param1, param2 )

	@abstractmethod
	def getName ( self )
	
	def __str__ ( self )
	
class AbstractNumericTile ( AbstractTile ) :
	
	def __init__ ( self )

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
	
	def __init__ ( self ) # TODO: how can we specify the color code?

	@abstractmethod
	def getCodomain ( self ) -> set
	



	


	




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
	
	def plotInROC ( self, fig, ax ) # and options ?
	
	def getAdvice ( self, language ) -> str # language can be: txt, html, latex
	
class AnalysisForBenchmarker ( AbstractAnalysis ) :

	def __init__ ( self, performances, parameterization, resolution=1001, options )
	
	def plotInROC ( self, fig, ax ) # and options ?
	
	def getValueTile ( self, entity ) -> AbstractNumericTile
	
	def getNoSkillTile ( self ) -> AbstractNumericTile
	
	def getRelativeSkillTile ( self ) -> AbstractNumericTile
	
	def getRankingTile ( self, entity ) -> AbstractNumericTile
	
	def getAdviceBasedOnRankingTiles ( self, language ) -> str # language can be: txt, html, latex
	
	def getEntityTile ( self, rank ) -> AbstractSymbolicTile
	
	def getAdviceBasedOnEntityTiles ( self, language ) -> str # language can be: txt, html, latex
	
class AnalysisForAppDeveloper ( AbstractAnalysis ) :

	def __init__ ( self, min_a, max_a, min_b, max_b, performances, parameterization, resolution=1001, options )
	
	def getEntityTile ( self, rank ) -> AbstractSymbolicTile
	
	def getValueTile ( self, entity ) -> AbstractNumericTile
	
	def getAdvice ( self, language ) -> str # language can be: txt, html, latex
	


