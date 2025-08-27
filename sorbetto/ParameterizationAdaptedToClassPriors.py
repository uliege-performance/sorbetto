
	
class ParameterizationAdaptedToClassPriors ( AbstractParameterization ) :
	"""
	Not yet published. Experimental. In Sébastien's mind.'
	
	
	Using the parameterization adapted to class priors with performances corresponding to
	the class priors $()\pi_-,\pi_+)$ is equivalent to using the default parameterization
	after applying a target shift operation :cite:t:`Sipka2022TheHitchhikerGuide` on all 
	performances in order to balance the class priors.
	
	See Theorem 5 of future "paper 6".
	"""
	
	def __init__ ( self, priorPos ) :
		assert isinstance ( priorPos, float )
		assert priorPos >= 0.0
		assert priorPos <= 1.0
		self._priorPos = priorPos
		self._priorNeg = 1 - priorPos
		AbstractParameterization.__init__ ( self )
	
	def getNegativeClassPrior () -> float :
		return self._priorNeg
	
	def getPositiveClassPrior () -> float :
		return self._priorPos

	def getNameParameter1 ( self ) :
        return r'a^{(\pi)}(I)'

	def getNameParameter2 ( self ) :
        return r'b^{(\pi)}(I)'
    
	def getBoundsParameter1 ( self ) -> tuple[float, float] :
        return 0.0, 1.0
	
	def getBoundsParameter2 ( self ) -> tuple[float, float] :
        return 0.0, 1.0
    
	def getCanonicalRankingScore ( self, param1, param2 ) -> RankingScore

	
	def getValueParameter1 ( self, rankingScore ) -> float

	
	def getValueParameter2 ( self, rankingScore ) -> float

	
	def getName ( self ) :
		return 'adapted to class priors (pos: {:g})'.format ( self._priorPos )





