from typing import List, Tuple

class IntegrationWeights:
    def __init__(self, name:str ):
        """
        The integration_weights part of configuration
        """
        self._name = name
        self._cosine = []
        self._sine = []

    @property
    def cosine( self )->List[Tuple[float,int]]:
        return self._cosine
    @cosine.setter
    def cosine( self, val:List[Tuple[float,int]] ):
        self._cosine = val
    
    @property
    def sine( self )->List[Tuple[float,int]]:
        return self._sine 
    @sine.setter
    def sine( self, val:List[Tuple[float,int]] ):
        self._sine = val
    
    def to_dict( self ):

        output_dict = {
            "cosine": self._cosine,
            "sine": self._sine
        }        
            
        return {
            self._name:output_dict
        }
 
def integrationWeight_read_dict( name:str, infos:dict )-> IntegrationWeights:
    """
    Input dictionary and output integration_weights object
    """
    integrationWeights = IntegrationWeights(name)
    keys = infos.keys()

    integrationWeights._cosine = infos["cosine"]
    integrationWeights._sine = infos["sine"]

    return integrationWeights