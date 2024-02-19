class Waveform:
    def __init__( self ):
        """
        The waveform in Pulse
        """
        self._I = None
        self._Q = None
        self._single = None

    @property
    def I( self )->str:
        """ For signal with mixer """
        return self._I
    @I.setter
    def I( self, val:str ):
        self._I = val
    
    @property
    def Q( self )->str:
        """ For signal with mixer """
        return self._Q
    @Q.setter
    def Q( self, val:str )->str:
        self._Q = val

    @property
    def single( self )->str:
        """ For direct signal """
        return self._single
    @single.setter
    def single( self, val:str ):
        self._single = val
        
    def to_dict( self ):

        output_dict = {}        

        if self.I != None:
            output_dict["I"] = self.I
        if self.Q != None:
            output_dict["Q"] = self.Q
        if self.single != None:
            output_dict["single"] = self.single

        return output_dict
    
class Pulse:
    def __init__(self, name:str ):
        """
        The Pulse part of configuration
        """
        self._name = name
        self._operation = None
        self._length = 0
        self._waveforms = Waveform()
        self._integration_weights = {}
        self._digital_marker = {}
        
    @property
    def operation( self )->str:
        """control or measurement"""
        return self._operation
    @operation.setter
    def operation( self, val:str ):
        self._operation = val
        
    @property
    def length( self )->int:
        return self._length 
    @length.setter
    def length( self, val:int ):
        self._length = val  
       
    @property
    def waveforms( self )->Waveform:
        return self._waveforms
    @waveforms.setter
    def waveforms( self, val:Waveform ):
        self._waveforms = val

    @property
    def integration_weights( self )->dict:
        """
        {\n
        "name_in_pulse": "name_in_integration_weight_conponent",\n
        "rotated_sin": "rotated_sine_weights_q1",\n
        "rotated_minus_sin": "rotated_minus_sine_weights_q1"\n
        }
        """
        return self._integration_weights
    @integration_weights.setter
    def integration_weights( self, val:dict ):
        self._integration_weights = val

    def to_dict( self ):

        output_dict = {
            "operation":self.operation,
            "length": self.length,
            "waveforms": self.waveforms.to_dict(),
        }        
        if len(self._integration_weights) != 0:
            output_dict.update( {"integration_weights":self._integration_weights} )
        if len(self._digital_marker) != 0:
            output_dict.update( {"digital_marker":self._digital_marker} )

        return {
            self._name:output_dict
        }
 
def pulse_read_dict( name:str, infos:dict )-> Pulse:
    """
    Input dictionary and output Pulse object
    "operation": "measurement",\n
    "length": 2000,\n
    "waveforms": {\n
        "I": "readout_wf_q1",\n
        "Q": "zero_wf"\n
    },\n
    "integration_weights": {\n
        "rotated_cos": "rotated_cosine_weights_q1",\n
        "rotated_sin": "rotated_sine_weights_q1",\n
        "rotated_minus_sin": "rotated_minus_sine_weights_q1"\n
    },\n
    "digital_marker": "ON"
    """
    pulse = Pulse(name)
    keys = infos.keys()

    pulse._operation = infos["operation"]
    pulse._length = infos["length"]
    pulse._waveforms = pwaveform_read_dict(infos["waveforms"])
    if "integration_weights" in keys:
        pulse._integration_weights = infos["integration_weights"]
    if "digital_marker" in keys:
        pulse._digital_marker = infos["digital_marker"]

    return pulse

def pwaveform_read_dict( infos:dict )-> Waveform:
    """
    "waveforms": {\n
        "I": "readout_wf_q1",\n
        "Q": "zero_wf"\n
    },\n
    """
    wf = Waveform()
    keys = infos.keys()

    if "I" in keys:
        wf.I = infos["I"]
    if "Q" in keys:
        wf.Q = infos["Q"]
    if "single" in keys:
        wf.single = infos["single"]

    return wf