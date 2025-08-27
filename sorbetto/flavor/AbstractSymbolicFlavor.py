class AbstractSymbolicFlavor ( AbstractFlavor ) :

	def __init__ ( self, name=None ):
		return

	@abstractmethod
	def getCodomain ( self ) -> set
	