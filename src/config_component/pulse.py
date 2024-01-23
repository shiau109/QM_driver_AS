

class Pulse:
    def __init__(self, name:str ):
        """
        The Pulse part of configuration
        """
        self._name = name
        self._operation = "control" # "measurement"
        self._length = 0
        self._waveforms = {}
        self._integration_weights = None
        self._digital_marker = None
        
    @property
    def operation( self )->str:
        return self._operation
 
    
    def to_dict( self ):

        output_dict = {
            "operation":self._operation,
            "length": self._length,
            "waveform": self._waveforms,
        }        
        if self._integration_weights != None:
            output_dict.update( {"integration_weights":self._integration_weights} )
        if self._digital_marker != None:
            output_dict.update( {"digital_marker":self._digital_marker} )

        return {
            self._name:output_dict
        }
 
def pulse_read_dict( name:str, infos:dict )-> Pulse:
    """
    Input dictionary and output Pulse object
    """
    pulse = Pulse(name)
    keys = infos.keys()

    pulse._operation = infos["operation"]
    pulse._length = infos["length"]
    pulse._waveforms = infos["waveforms"]
    if "integration_weights" in keys:
        pulse._integration_weights = infos["integration_weights"]
    if "digital_marker" in keys:
        pulse._digital_marker = infos["digital_marker"]

    return pulse