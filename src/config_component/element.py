from typing import Dict, Union


class MixedInputs:
    def __init__( self ):
        self.I = ()
        self.Q = ()
        self.lo_frequency = ()
        self.mixer = None
    def to_dict( self ):
        return {
            "mixInputs":{
                "I":self.I,
                "Q":self.Q,
                "lo_frequency":self.lo_frequency,
                "mixer":self.mixer
            }
        }
    
class SingleInput:
    def __init__( self ):
        self.port = ()
    def to_dict( self ):
        return {
            "singleInput":{
                "port":self.port
            }
        }
# class Operation

class Element:
    def __init__(self, name:str ):
        """
        The controller part of configuration
        """
        self._name = name
        self._operations = {}
        self._input_map  = None
        self._output_map = None
        self._intermediate_frequency = None
        self._time_of_flight = None
        self._smearing = None

    @property
    def operations( self )->dict:
        return self._operations
    
    @property
    def input_map( self )->Union[MixedInputs,SingleInput]:
        return self._input_map    
    
    def to_dict( self ):

        output_dict = {
            "operations":self._operations
        }
        output_dict.update( self.input_map.to_dict() )
        
        if self._intermediate_frequency != None:
            output_dict.update( {"operations":self._intermediate_frequency} )
        if self._time_of_flight != None:
            output_dict.update( {"time_of_flight":self._time_of_flight} )
        if self._smearing != None:
            output_dict.update( {"smearing":self._smearing} )

        if self._output_map != None: # TODO fixed output
            output_dict.update( {"outputs":self._output_map} )

        return {
            self._name:output_dict
        }
    
def mixedInputs_read_dict( infos:dict )->MixedInputs:
    """
    Input dictionary and output MixedInputs object
    """
    mixedInputs = MixedInputs()
    mixedInputs.I = infos["I"]
    mixedInputs.Q = infos["Q"]
    mixedInputs.lo_frequency = infos["lo_frequency"]
    mixedInputs.mixer = infos["mixer"]
    return mixedInputs

def singleInput_read_dict( infos:dict )->SingleInput:
    """
    Input dictionary and output MixedInputs object
    """
    singleInput = SingleInput()
    singleInput.port = infos["port"]
    return singleInput

def element_read_dict( name:str, infos:dict )-> Element:
    """
    Input dictionary and output MixedInputs object
    """
    element = Element(name)
    keys = infos.keys()
    if "mixInputs" in keys:
        print("Mixed Inputs Element")
        element._input_map = mixedInputs_read_dict( infos["mixInputs"] )

    if "singleInput" in keys:
        element._input_map = singleInput_read_dict( infos["singleInput"] )

    element._operations = infos["operations"]

    if "outputs" in keys: # TODO fixed output
        element._output_map = infos["outputs"]
    if "time_of_flight" in keys:
        element._time_of_flight = infos["time_of_flight"]
    if "smearing" in keys:
        element._smearing = infos["smearing"]
    
    return element

if __name__ == '__main__':  
    m_e_dict = {
        'mixInputs': {
            'I': ('con1', 1),
            'Q': ('con1', 2),
            'lo_frequency': 6,
            'mixer': 'mixer_qubit'
        },
        'intermediate_frequency': 0,
        'operations': {
            'saturation': 'saturation_pulse',
            'x180': 'pi_pulse',
            'x90': 'pi_half_pulse',
        }
    }
    s_e_dict = {
        'singleInput': {
            'port': ('con1', 1),
        },
        'intermediate_frequency': 0,
        'operations': {
            'saturation': 'saturation_pulse',
        }
    }
    e = element_read_dict("qubit1", m_e_dict)
    print(e.to_dict())