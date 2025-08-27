class AbstractSymbolicFlavor ( AbstractFlavor ) :

	def __init__ ( self, name=None )

	@abstractmethod
	def getCodomain ( self ) -> set
	