from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.geometry.pencil import Pencil
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.asbtract_tile import AbstractTile

# from sorbetto.tile.numeric_tile import AbstractNumericTile


class ValueTile(AbstractTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        flavor: AbstractSymbolicFlavor,
        resolution: int = 1001,
    ):
        super().__init__(
            name=name,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
        )

    def getVUT(self):
        """
        Computes the volume

        See :cite:t:`Pierard2024TheTile-arxiv`, Section 3.1. (with default parameterization)
        """

        """

        !!!!!! THIS IS IF THE PARAMETERIZATION IS DEFAUT. OTHERWISE, WE HAVE TO DO ANALYTICALY OR NUMERICALLY. !!!!!


		def x_log_x ( x ) :
			if x == 0 :
				return 0.0
			else :
				return x * np.log ( x )
			
		def vut ( proba_TN , proba_FP , proba_FN , proba_TP ) :

			if proba_TN + proba_FP == 0.0 :
				return math.nan # The code below does not compute the right value, perhaps should we use the limit ?
			if proba_FN + proba_TP == 0.0:
				return math.nan # The code below does not compute the right value, perhaps should we use the limit ?
			if proba_TN + proba_FN == 0.0:
				return math.nan # The code below does not compute the right value, perhaps should we use the limit ?
			if proba_TP + proba_FP == 0.0:
				return math.nan # The code below does not compute the right value, perhaps should we use the limit ?

			same_TN_TP = math.isclose(proba_TN, proba_TP)
			same_FN_FP = math.isclose(proba_FN, proba_FP)
			if same_TN_TP and same_FN_FP :
				return proba_TN + proba_TP
			elif same_TN_TP :
				return proba_TN / (proba_FN - proba_FP) * ( np.log ( proba_TN + proba_FN ) - np.log ( proba_TN + proba_FP ))
			elif same_FN_FP :
				return 1.0 - proba_FN / ( proba_TP - proba_TN ) * ( np.log ( proba_TP + proba_FN ) - np.log ( proba_TN + proba_FN ) )
			else :
				# The analytical solution implemented here is due to Anthony Cioppa; many thanks to him.
				num = (proba_FN - proba_TP) * x_log_x ( proba_FN + proba_TP ) \
					+ (proba_TN - proba_FN) * x_log_x ( proba_TN + proba_FN ) \
					+ (proba_TP - proba_FP) * x_log_x ( proba_FP + proba_TP ) \
					+ (proba_FP - proba_TN) * x_log_x ( proba_TN + proba_FP )
				den = (proba_TP - proba_TN) * (proba_FN - proba_FP)
				return 0.5 - 0.5 * num / den
			
		return _ScoreForTwoClassClassificationFromFunction ( vut , 0 , 1 , 'Volume Under Tile' )
        """
        ...

    def asPencil(self) -> Pencil: ...  # TODO
