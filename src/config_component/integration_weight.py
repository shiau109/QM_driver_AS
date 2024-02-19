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
    def cosine( self )->List[Tuple[int,int]]:
        return self._cosine
    @property
    def sine( self )->List[Tuple[int,int]]:
        return self._sine 
    
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