from config_component.controller import Controller, controller_read_dict
from config_component.element import Element, element_read_dict
from config_component.pulse import Pulse, pulse_read_dict
from config_component.waveform import Waveform, waveform_read_dict
from config_component.digital_waveform import DigitalWaveform, digitalWaveform_read_dict
from config_component.integration_weight import IntegrationWeights, integrationWeight_read_dict
from config_component.mixer import Mixer, mixer_read_list
from typing import Dict


class Configuration():
    def __init__( self, version:int=1 ):
        
        self.version = 1
        self._controllers = {}
        self._elements = {}
        self._pulses = {}
        self._waveforms = {}
        self._digital_waveforms = { "ON": digitalWaveform_read_dict("ON", {"samples": [(1, 0)]}) }
        self._integration_weights = {}
        self._mixers = {}

    def get_config( self ) -> dict :

        config_dict = {"version": self.version}
        
        components = ["controllers","elements","pulses","waveforms","digital_waveforms","integration_weights","mixers"]
        component_objs = [self.controllers,self.elements,self.pulses,self.waveforms,self.digital_waveforms,self.integration_weights,self.mixers]
        
        for c_type_name, c_objs in zip(components,component_objs):
            config_dict[c_type_name] = {}
            for c_name, c_obj in c_objs.items():
                
                config_dict[c_type_name].update( c_obj.to_dict() )

        return config_dict

    def update_controller( self, controller:Controller):
        """
        The controller will be covered by new one.
        """
        self._controllers[controller.name] = controller

    @property
    def controllers( self )->Dict[str, Controller]:
        return self._controllers

    @property
    def elements( self )->Dict[str, Element]:
        return self._elements

    @property
    def pulses( self )->Dict[str, Pulse]:
        return self._pulses

    @property
    def waveforms( self )->Dict[str, Waveform]:
        return self._waveforms
    
    @property
    def digital_waveforms( self )->Dict[str, DigitalWaveform]:
        return self._digital_waveforms
    
    @property
    def integration_weights( self )->Dict[str, IntegrationWeights]:
        return self._integration_weights
    
    @property
    def mixers( self )->Dict[str, Mixer]:
        return self._mixers
                
    
    

    
        
    

# ================== other functions =======================
    def export_config( self, path ):
        import pickle

        # define dictionary
        # create a binary pickle file 
        f = open(path,"wb")
        # write the python object ) to pickle file
        pickle.dump(self ,f)
        # close file
        f.close()



    def check_mixerCorrectionPair_for(self,target_q:str):
        """
            print out the mixer corrections and the frequencies about target_q both in 'elements' and 'mixers'.
        """
        elements = self.__config['elements'][f"{target_q}_xy"]
        print("=================================================")
        print(f"Mixer for {target_q} is <<{elements['mixInputs']['mixer']}>>")
        print(f"LO frequency registerd: {elements['mixInputs']['lo_frequency']} Hz")
        print(f"IF frequency registerd: {elements['intermediate_frequency']} Hz")
        print(f"Information in mixer:\n {self.__config['mixers'][elements['mixInputs']['mixer']]}")
        print("=================================================")

    # def renew_config_for(self,specs:Circuit_info,target_q:str='all'):
    #     """
    #         Renew the config with the given `Circuit_info` for target_q. This renew includes RO, XY, Z and wiring.\n
    #         target_q: "q2", 'all' for default.
    #     """
    #     qs = [target_q] if target_q != 'all' else specs.__roInfo["registered"]

    #     for q_name in qs:
    #         # Update RO info
    #         RO_freqs = {f'resonator_LO_{q_name}':specs.__roInfo[q_name][f'resonator_LO'],f'resonator_IF_{q_name}':specs.__roInfo[q_name][f'resonator_IF']}
    #         self.update_ReadoutFreqs(updatedInfo=RO_freqs)
    #         self.update_Readout(q_name,specs.get_spec_forConfig('ro'))
    #         # Update XY info
    #         XY_freqs = {f"qubit_LO_{q_name}":specs.__xyInfo[q_name]["qubit_LO"],f"qubit_IF_{q_name}":specs.__xyInfo[q_name]["qubit_IF"]}
    #         self.update_controlFreq(updatedInfo=XY_freqs)
    #         self.update_controlWaveform(specs.get_spec_forConfig('xy'),q_name)
    #         # Update Z info
    #         '''TODO'''
    #         zInfo = specs.update_zInfo_for(q_name)
    #         # Update Wiring info
    #         '''TODO'''
    #     pass


def import_config( path )->Configuration:
    import pickle
    # Read dictionary pkl file
    with open(path, 'rb') as fp:
        config = pickle.load(fp)
    return config

def configuration_read_dict( config:dict )->Configuration:
    # configuration_components = ["controllers"]
    new_config = Configuration( config["version"] )
    for name, infos in config["controllers"].items():
        new_config._controllers[name] = controller_read_dict( name, infos )

    for name, infos in config["elements"].items():
        new_config._elements[name] = element_read_dict( name, infos )    

    for name, infos in config["pulses"].items():
        new_config._pulses[name] = pulse_read_dict( name, infos )    
        
    for name, infos in config["waveforms"].items():
        new_config._waveforms[name] = waveform_read_dict( name, infos ) 

    for name, infos in config["digital_waveforms"].items():
        new_config._digital_waveforms[name] = digitalWaveform_read_dict( name, infos ) 

    for name, infos in config["integration_weights"].items():
        new_config._integration_weights[name] = integrationWeight_read_dict( name, infos )

    for name, infos in config["mixers"].items():
        new_config._mixers[name] = mixer_read_list( name, infos )  
        # new_config.controllers[con_name]
    return new_config

def get_element_template( mode:str )->dict:
    match mode.lower():
        case "ro":
            element_template = {
                "mixInputs": {
                    "I": None,
                    "Q": None,
                    "lo_frequency": None,
                    "mixer": None,
                },
                "intermediate_frequency":  None, 
                "operations": {},
                "outputs": {},
                "time_of_flight": None,
                "smearing": 0,
            } 
        case "xy":
            element_template = {
                "mixInputs": {
                    "I": None,
                    "Q": None,
                    "lo_frequency": None,
                    "mixer": None,
                },
                "intermediate_frequency":  None, 
                "operations": {}
            } 
        case 'z':
            element_template = {
                "singleInput": {
                    "port": None,
                }, 
                "operations": {
                    "const":None,
                },
            }
        case _:
            raise KeyError (f"Can't create an element with the given mode={mode}")
    return element_template   

