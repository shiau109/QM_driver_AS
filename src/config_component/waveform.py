

class Waveform:
    def __init__(self, name:str ):
        """
        The Waveform part of configuration
        """
        self._name = name
        self._type = None
        self._sample = None
        
    @property
    def type( self )->str:
        return self._type
 
    
    def to_dict( self ):

        output_dict = {
            "type":self._type,
            "sample": self._sample,
        }        
            
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