class AbstractNumericFlavor ( AbstractFlavor ) :

	def __init__ ( self, name=None )

	@abstractmethod
	def getLowerBound ( self )

	@abstractmethod
	def getUpperBound ( self )