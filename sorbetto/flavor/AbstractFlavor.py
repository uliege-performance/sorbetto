class AbstractFlavor ( ABC ) :
	"""
	A flavor is a function that gives something to show on a Tile for any given importance values.
	"""

	def __init__ ( self, name=None )
	
	@abstractmethod
	def getDefinition ( self ) -> str
	
	@abstractmethod
	def __call__ ( self, importances )
	
	@abstractmethod
	def getDefaultColormap ( self )
	
	def getName ( self )
	
	def __str__ ( self )