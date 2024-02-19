from typing import Union

class Waveform:
    def __init__(self, name:str ):
        """
        The Waveform part of configuration
        wf_type: constant or arbitrary
        """
        self._name = name
        self._type = None
        self._sample = None
      
    @property
    def type( self )->str:
        """constant or arbitrary"""
        return self._type
    @type.setter
    def type( self, val:str )->str:
        self._type = val
    
    @property
    def sample( self )->Union[list, float]:
        """ 
        list for arbitrary
        float for constant
        """
        return self._sample 
    @sample.setter
    def sample( self, val:Union[list, float] ):
        self._sample = val
        
    def to_dict( self ):

        output_dict = {
            "type":self.type,
        }
        match self.type:
            case "constant":
                output_dict["sample"] = self._sample
            case "arbitrary":
                output_dict["samples"] = self._sample

        return {
            self._name:output_dict
        }
 
def waveform_read_dict( name:str, infos:dict )-> Waveform:
    """
    Input dictionary and output Waveform object
    """
    waveform = Waveform(name)
    keys = infos.keys()

    waveform._type = infos["type"]
    match waveform._type:
        case "constant":
            waveform._sample = infos["sample"]
        case "arbitrary":
            waveform._sample = infos["samples"] 
        case _:
            waveform._sample = infos["sample"]   
    return waveform