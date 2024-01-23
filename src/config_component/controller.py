from typing import Dict

class Analog_output:

    def __init__( self, channel_index:int ):
        """
        The analog_outputs part in controller
        """
        self._channel_index = channel_index
        self.offset = 0.0
        self.filter = {} # TODO filter

    def to_dict( self ):
        return {
            self._channel_index:{
                "offset":self.offset,
                "filter":{} # TODO filter
            }

        }
class Filter:
    """ TODO """
    def __init__( self ):
        self.feedforward = []
        self.feedback = []


class Controller:
    def __init__(self, name:str ):
        """
        The controller part of configuration
        """
        self._name = name
        self._analog_outputs = {}
        self.digital_outputs = {} # TODO
        self.analog_inputs = {} 
    
    @property
    def analog_outputs( self )->Dict[int,Analog_output]:
        return self._analog_outputs
    
    def to_dict( self ):
        return {
            self._name:{
                "analog_outputs":self.analog_outputs
            }
        }
    
    def add_analog_output( self, analog_output:Analog_output ):
        add_idx = analog_output._channel_index
        if add_idx not in self.analog_outputs.keys():
            self.analog_outputs[add_idx] = analog_output

def controller_read_dict( key:str, infos:dict )->Controller:
    """
    Input dictionary and output Controller object
    """
    new_controller = Controller(key)
    analog_outputs = infos["analog_outputs"]
    for k, infos in analog_outputs.items():
        channel_index = int(k)
        new_controller.analog_outputs[channel_index] = analog_output_read_dict( channel_index, infos )
    return new_controller

def analog_output_read_dict( channel_index:int, infos:dict )->Analog_output:
    """
    Input dictionary and output Analog_output object
    """
    analog_output = Analog_output( channel_index )
    analog_output.offset = infos["offset"]
    # analog_output.filter = infos["filter"]  TODO
    return analog_output
def controller_read_json( path ):
    pass

# def controller_read_pe
if __name__ == '__main__':
    new_controller = Controller("con1")
    for i in range(5):
        new_analog_output = Analog_output(i)
        new_controller.add_analog_output(new_analog_output)