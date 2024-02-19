
from typing import List

class IFChannel():
    def __init__(self ):
        """
        The class for different IF freq in the same mixer
        """
        self._intermediate_frequency = 0
        self._lo_frequency = 0
        self._correction = []

    @property
    def intermediate_frequency( self )->int:
        return self._intermediate_frequency
    @intermediate_frequency.setter
    def intermediate_frequency( self, val:int ):
        self._intermediate_frequency = val
        
    @property
    def lo_frequency( self )->int:
        return self._lo_frequency
    @lo_frequency.setter
    def lo_frequency( self, val:int ):
        self._lo_frequency = val
    
    @property
    def correction( self )->list:
        return self._correction
    @correction.setter
    def correction( self, val:list )->list:
        self._correction = val
    
    def to_dict( self )->dict:

        output_dict = {
            "intermediate_frequency":self._intermediate_frequency,
            "lo_frequency": self._lo_frequency,
            "correction": self._correction,
        }        

        return output_dict
          
 
class Mixer:
    def __init__(self, name:str ):
        """
        The Mixer part of configuration
        """
        self._name = name
        self._iFChannels = []
        
    @property
    def iFChannels( self )->List[IFChannel]:
        return self._iFChannels
 
    
    def to_dict( self )->dict:

        channel_dicts = []
        for iFChannel in self.iFChannels:
            channel_dicts.append( iFChannel.to_dict() )  

        return {
            self._name:channel_dicts
        }

def iFChannel_read_dict( infos:dict ):

    iFChannel = IFChannel()
    iFChannel._intermediate_frequency = infos["intermediate_frequency"]
    iFChannel._lo_frequency = infos["lo_frequency"]
    iFChannel._correction = infos["correction"]
    return iFChannel

def mixer_read_list( name:str, infos:list[dict] )-> Mixer:
    """
    Input dictionary and output Mixer object
    """
    mixer = Mixer(name)
    mixer._iFChannels = []
    for iFInfo in infos:
        mixer._iFChannels.append(iFChannel_read_dict(iFInfo))

    return mixer