
	
class ParameterizationAdaptedToPredictionRates ( AbstractParameterization ) :
	"""
	Not yet published. Experimental. In Sébastien's mind.'
	
	Using the parameterization adapted to prediction rates with performances corresponding
	to the prediction rates $(\tau_-,\tau_+)$ is equivalent to using the default
	parameterization after applying a target shift operation
	:cite:t:`Sipka2022TheHitchhikerGuide` on all performances in order to balance the
	prediction rates.
	
	See Theorem 6 of future "paper 6".
	"""
	
	def __init__ ( self, ratePos ) :
		assert isinstance ( ratePos, float )
		assert ratePos >= 0.0
		assert ratePos <= 1.0
		self._ratePos = ratePos
		self._ratePos = 1 - ratePos
		AbstractParameterization.__init__ ( self )
	
	def getRateOfNegativePredictions () -> float :
		return self._rateNeg
	
	def getRateOfPositivePredictions () -> float :
		return self._ratePos

	@abstractmethod
	def getName ( self ) :
		return 'adapted to prediction rates (pos: {:g})'.format ( self._ratePos )



