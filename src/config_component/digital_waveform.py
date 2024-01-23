from typing import List, Tuple

class DigitalWaveform:
    def __init__(self, name:str ):
        """
        The digital_waveform part of configuration
        """
        self._name = name
        self._samples = []
        
    @property
    def samples( self )->List[Tuple[int,int]]:
        return self._samples
 
    
    def to_dict( self ):

        output_dict = {
            "samples": self._sample,
        }        
            
        return {
            self._name:output_dict
        }
 
def digitalWaveform_read_dict( name:str, infos:dict )-> DigitalWaveform:
    """
    Input dictionary and output DigitalWaveform object
    """
    waveform = DigitalWaveform(name)
    keys = infos.keys()

    waveform._samples = infos["samples"]
    
    return waveform