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
        self._digital_waveforms = {}
        self._integration_weights = {}
        self._mixers = {}


        self.__config = {
            "version": 1,
            "controllers": {},
            "elements": {},
            "pulses": {
                "const_pulse": {
                    "operation": "control",
                    "length": 1000,
                    "waveforms": {
                        "I": "const_wf",
                        "Q": "zero_wf",
                    },
                },                
            },
            "waveforms": {
                "zero_wf": {"type": "constant", "sample": 0.0},
            },
            "digital_waveforms": {
                "ON": {"samples": [(1, 0)]},
            },
            "integration_weights": {},
            "mixers": {},
        }
        
    def set_wiring( self, controller_name:str ):
        '''
            initialize the controller in configuration with the controller_name.\n
            controller_name: 'con1'.
        '''
        update_setting = {
            controller_name:{
                "analog_outputs": {
                    1: {"offset": 0.0},  # I readout line
                    2: {"offset": 0.0},  # Q readout line
                    3: {"offset": 0.0},  # I qubit1 XY
                    4: {"offset": 0.0},  # Q qubit1 XY
                    5: {"offset": 0.0},  # I qubit2 XY
                    6: {"offset": 0.0},  # Q qubit2 XY
                    7: {"offset": 0.0},  # I qubit3 XY
                    8: {"offset": 0.0},  # Q qubit3 XY
                    9: {"offset": 0.0},  # I qubit4 XY
                    10: {"offset": 0.0},  # Q qubit4 XY
                },
                "digital_outputs": {
                    1: {},
                    3: {},
                    5: {},
                    7: {},
                    9: {},
                },
                "analog_inputs": {
                    1: {"offset": 0, "gain_db": 0},  # I from down-conversion
                    2: {"offset": 0, "gain_db": 0},  # Q from down-conversion
                },
            }
        }
        self.__config["controllers"].update(update_setting)

    def get_config(self,*args) -> dict :
        import copy
        return copy.deepcopy(self.__config)

    def update_controller( self, controller:Controller):
        """
        The controller will be covered by new one.
        """
        self.controllers[controller._name] = controller

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
                
    def update_downconverter(self, channel:int ,ctrl_name:str='con1', **kwargs):
        """
            Update the analog_inputs in the give controller and channel.\n
            ctrl_name: "con1" for default.\n
            channel: 1...\n
            kwargs: offset=0.02, gain_db=10.
        """
        where = self.__config["controllers"][ctrl_name]["analog_inputs"][channel]
        if kwargs != {}:
            for info in kwargs:
                if info.lower() in ["offset","gain_db"]:
                    where[info] = kwargs[info]
                else:
                    raise KeyError("Check the key name in kwargs, it should be 'offset' or 'gain_db'.")
        else:
            raise ValueError("You should give the info want to update in kwargs!")

    def update_element( self, name:str, setting:dict ):
        if name in self.__config["elements"].keys():
            self.__config["elements"][name].update(setting)
        else:
            print(f"Warning: No element name {name}")

    def update_mixer( self, name:str, setting:dict ):
        update_setting = {name:setting}
        self.__config["mixers"].update(update_setting)

    def add_element( self, name, setting:dict = None ):
        """
        Add a initial tempelate for a element
        { \n
            "mixInputs": { \n
                    "I": None, \n
                    "Q": None, \n
                    "lo_frequency": None, \n
                    "mixer": None, \n
            }, \n
            "intermediate_frequency":  None, \n
            "operations": {}, \n
            "outputs": {}, \n
            "time_of_flight": None, \n
            "smearing": None, \n
            }
        }
        """
        if setting == None:
            setting = {
                "mixInputs": {
                    "I": None,
                    "Q": None,
                    "lo_frequency": None,
                    "mixer": None,
                },
                "intermediate_frequency":  None, 
                "operations": {
                },
                "outputs": {
                },
                "time_of_flight": None,
                "smearing": 0,
            }

        self.__config["elements"][name]=setting

    def add_pulse( self, name, setting:dict = None ):
        """
        Add a initial tempelate for a pulse
        {
            "operation": None,
            "length": None,
            "waveforms": {},
            "integration_weights": {},
            "digital_marker": None,
            }
        """
        if setting == None:
            setting = {
            "operation": None,
            "length": None,
            "waveforms": {},
            "integration_weights": {},
            "digital_marker": None,
            }

        self.__config["pulses"][name]=setting

    def add_waveform( self, name, setting:dict = None ):
        """
        Add a initial tempelate for a waveform
        { \n
           "type": "arbitrary", \n
           "sample": y180_Q_wf_q1.tolist()  \n
        }
        """
        if setting == None:
            setting = {
                "type": None, 
                "sample": None
            }

        self.__config["waveforms"][name]=setting

    def add_integrationWeight( self, name, setting:dict = None ):
        """
        Add a initial tempelate for a integration_weight \n
        { \n
            "cosine": [(np.cos(rotation_angle_q1), readout_len)], \n
            "sine": [(np.sin(rotation_angle_q1), readout_len)], \n
        }
        """
        if setting == None:
            setting = {
                "cosine": None, 
                "sine": None
            }
        self.__config["integration_weights"][name]=setting

    def update_integrationWeight(self, target_q:str, updated_RO_spec:dict, from_which_value:str):
        '''
            update the integration weights from the updated_RO_spec by the given value key name.\n
            target_q: "q2",\n
            updated_RO_spec: RO_info from the Circuit_info,\n
            from_which_value: update by which value('origin', 'rotated' or 'optimal')
        '''
        weights_first_name = f"{target_q}_rotated_weight_"
        weights_catalog = ["cos", "sin", "minus_sin"]
        RO_len = updated_RO_spec['readout_len']
        for cata_name in weights_catalog:
            if from_which_value != 'optimal':
                match cata_name:
                    case "cos":
                        self.__config["integration_weights"][weights_first_name+cata_name]['cosine'] = [(cos(float(updated_RO_spec[target_q]["RO_weights"][from_which_value])), RO_len)]
                        self.__config["integration_weights"][weights_first_name+cata_name]['sine'] = [(sin(float(updated_RO_spec[target_q]["RO_weights"][from_which_value])), RO_len)]
                    case "sin":
                        self.__config["integration_weights"][weights_first_name+cata_name]['cosine'] = [(-sin(float(updated_RO_spec[target_q]["RO_weights"][from_which_value])), RO_len)]
                        self.__config["integration_weights"][weights_first_name+cata_name]['sine'] = [(cos(float(updated_RO_spec[target_q]["RO_weights"][from_which_value])), RO_len)]
                    case "minus_sin":
                        self.__config["integration_weights"][weights_first_name+cata_name]['cosine'] = [(sin(float(updated_RO_spec[target_q]["RO_weights"][from_which_value])), RO_len)]
                        self.__config["integration_weights"][weights_first_name+cata_name]['sine'] = [(-cos(float(updated_RO_spec[target_q]["RO_weights"][from_which_value])), RO_len)]
                    case _:
                        pass
            else:
                self.__config["integration_weights"][weights_first_name+cata_name]['cosine'] = updated_RO_spec[target_q]["RO_weights"][from_which_value][cata_name]['cosine']
                self.__config["integration_weights"][weights_first_name+cata_name]['sine'] = updated_RO_spec[target_q]["RO_weights"][from_which_value][cata_name]['sine']


    def add_mixer( self, name, setting:dict = None ):
        """
        Add a initial tempelate for a mixer \n
        { \n
            "intermediate_frequency": resonator_IF[0], \n
            "lo_frequency": resonator_LO, \n
            "correction": (1, 0, 0, 1), \n
        }
        """
        if setting == None:
            setting = {
                "intermediate_frequency": None,
                "lo_frequency": None,
                "correction": (1, 0, 0, 1),
            }

        if name in self.__config["mixers"].keys():
            for mixer_info in self.__config["mixers"][name]: 

                is_exist_IF = setting["intermediate_frequency"] == mixer_info["intermediate_frequency"]
                is_exist_LO = setting["lo_frequency"] == mixer_info["lo_frequency"]
                
                if not (is_exist_IF and is_exist_LO):
                    self.__config["mixers"][name].append(setting)
                    break
                else: 
                    print( f"intermediate frequency {setting['intermediate_frequency']} and LO frequency {setting['lo_frequency']} is already in {name}.\n")

        else:
            self.__config["mixers"][name]=[setting]

    def update_element_mixer( self, name, mixInputs:dict ):
        """
        Change the element mixer setting (mixInputs)
        """
        setting = {
            "mixInputs":  mixInputs, 
        }
        self.update_element( name, setting ) 

    def update_element_TOF( self, name, time_of_flight:float ):
        """
        Change the time of flight (time_of_flight)
        """
        self.__config["elements"][name]["time_of_flight"] = time_of_flight

    def update_element_output( self, name, output:dict ):
        """
        Change the output channel (outputs)
        """
        self.__config["elements"][name]["outputs"] = output

    def update_element_IF( self, name, freq_IF:float ):
        """
        Change the IF of the channel (intermediate_frequency)
        """
        setting = {
            "intermediate_frequency":  freq_IF, 
        }
        self.update_element( name, setting ) 
        
    def create_roChannel( self, name, element, pulse, waveform ):
        """
        element structure \n
        { \n
            "mixInputs": { \n
                "I": ("con1", 1), \n
                "Q": ("con1", 2), \n
                "lo_frequency": resonator_LO, \n
                "mixer": "octave_octave1_1", \n
            }, \n
            "intermediate_frequency": resonator_IF[0], \n
            "operations": {}, \n
            "outputs": { \n
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            }, \n
            "time_of_flight": time_of_flight, \n
            "smearing": 0, \n
        } \n

        register readout pulse by name f"{name}_ro_pulse" \n
        { \n
            "operation": "measurement", \n
            "length": integration_time, \n
            "waveforms": {}, \n
            "integration_weights": {}, \n
            "digital_marker": "ON", \n
        }

        register readout pulse by name f"{name}_ro_wf" \n
        { \n
           "type": "arbitrary", \n
           "samples": y180_Q_wf_q1.tolist()  \n
        }
        """
        pulse_name = f"readout_pulse_{name}"
        waveform_name = f"readout_wf_{name}"

        element["operations"] = {
            "readout": pulse_name
        }

        
        pulse["waveforms"]["I"] = waveform_name
        pulse["waveforms"]["Q"] = "zero_wf"


        mixer_name = element["mixInputs"]["mixer"]
        mixer_setting = {
            "intermediate_frequency": element["intermediate_frequency"],
            "lo_frequency": element["mixInputs"]["lo_frequency"],
            "correction": (1, 0, 0, 1),
        }
        self.add_element( f"{name}_ro", element )
        self.add_pulse( pulse_name, pulse )
        self.add_waveform( waveform_name, waveform )
        self.add_mixer( mixer_name, mixer_setting )
        
        integ_name = f"{name}_rotated_weight"
        integ_len = pulse["length"]

        for weight_name, cos_w, sin_w in zip(["cos", "sin", "minus_sin"],[1,0,0],[0,1,-1]):
            integration_weight = {
                "cosine":[(cos_w,integ_len)],
                "sine":[(sin_w,integ_len)]
            }
            complete_integ_name = f"{integ_name}_{weight_name}"
            pulse["integration_weights"][f"rotated_{weight_name}"] = complete_integ_name
            self.add_integrationWeight( complete_integ_name,integration_weight )

    def get_element_template( self, mode:str ):
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

    def creat_zChannel(self,target_q:str,z_element:dict,zSpec:dict):
        """
            create the z elements for target_q, includes elements, pulses, waveforms.
        """  
        # elements value
        pulse_name = f"const_flux_pulse"
        z_element["singleInput"]["port"] = (zSpec[target_q]["controller"],zSpec[target_q]["con_channel"])
        z_element["operations"]["const"] = pulse_name
        self.__config["elements"][f"{target_q}_z"] = z_element
        # pulses value
        self.__config["pulses"][pulse_name]={
            "operation": "control",
            "length": zSpec["const_flux_len"],
            "waveforms": {
                "single": f"const_flux_wf",
            },
        }
        # waveforms value
        self.__config["waveforms"][f"const_flux_wf"]={
            "type": "constant", "sample": zSpec['const_flux_amp']
        }

    
    def create_qubit( self, name:str, ROinfo:dict, XYinfo:dict, WireInfo:dict, ZInfo:dict, **kwargs):
        """
        name : "q3",\n
        ROinfo
            "ro_IF","ro_LO","electrical_delay","integration_time","ro_wf"
        
        XYinfo
        keys
        "pi_amp","pi_len","qubit_LO","qubit_IF","drag_coef","anharmonicity","AC_stark_detuning","waveform_func"
        
        """
        
        # Build RO
        ro_element = self.get_element_template(mode='ro')
        ro_element["mixInputs"]["I"] = WireInfo[name]["up_I"]
        ro_element["mixInputs"]["Q"] = WireInfo[name]["up_Q"]
        ro_element["mixInputs"]["lo_frequency"] = ROinfo[name]["resonator_LO"]
        ro_element["mixInputs"]["mixer"] = WireInfo[name]["ro_mixer"]
        ro_element["intermediate_frequency"] = ROinfo[name]["resonator_IF"]
        ro_element["outputs"]["out1"] = WireInfo[name]["down_I"]
        ro_element["outputs"]["out2"] = WireInfo[name]["down_Q"]
        ro_element["time_of_flight"] = ROinfo["time_of_flight"]

        ro_pulse = { 
            "operation": "measurement", 
            "length": ROinfo['readout_len'], 
            "waveforms": {
            }, 
            "integration_weights": {}, 
            "digital_marker": "ON", 
        }   
        ro_wf = {
           "type": "constant",
           "sample": ROinfo[name][f"readout_amp"]
        } 
        self.create_roChannel( name, ro_element, ro_pulse, ro_wf)

        # Build XY
        xy_element = self.get_element_template(mode='xy')
        xy_element["mixInputs"]["I"] = WireInfo[name]["xy_I"]
        xy_element["mixInputs"]["Q"] = WireInfo[name]["xy_Q"]
        xy_element["mixInputs"]["lo_frequency"] = XYinfo[name]["qubit_LO"]
        xy_element["mixInputs"]["mixer"] = WireInfo[name]["xy_mixer"]
        xy_element["intermediate_frequency"] = XYinfo[name]["qubit_IF"]
        self.create_xyChannel( name, xy_element, XYinfo)

        # Build Z line
        z_element = self.get_element_template(mode='z')
        self.creat_zChannel(name,z_element,ZInfo)

        


    def create_multiplex_readout_channel( self, common_wiring:dict, individual_setting:list):
        """
        common wiring ex.
        {
            "I":("con1",1)
            "Q":("con1",2)
            "freq_LO": 6, # GHz
            "mixer": "octave_octave1_1",
            "time_of_flight": 250, # ns
            "integration_time": 2000 # ns
        }
        individual setting : list
        {
            "name":"r1",
            "freq_IF": -30.5 , # MHz
            "amp": 0.01 # V
        }
        register readout pulse by name rp f"readout_pulse_{name}"
        """

        freq_LO = int(common_wiring["freq_LO"] * u.GHz) 
        electrical_delay = int(common_wiring["time_of_flight"])
        mixer_name = common_wiring["mixer"]

        resonator_element_template_dict = {
            "mixInputs": {
                "I": common_wiring["I"],
                "Q": common_wiring["Q"],
                "lo_frequency": freq_LO,
                "mixer": mixer_name,
            },
            "intermediate_frequency":  None, 
            "operations": {
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": electrical_delay,
            "smearing": 0,
        }
        integration_time = common_wiring["integration_time"]
        readout_pulse_template_dict = {
            "operation": "measurement",
            "length": integration_time,
            "waveforms": {},
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",

            },
            "digital_marker": "ON",
        }
        
        self.__config["mixers"] = {
            mixer_name:[],
        }

        mixers_template_dict = {
            "intermediate_frequency": 100,
            "lo_frequency": freq_LO,
            "correction": (1, 0, 0, 1),  
        }

        self.__config["integration_weights"].update({
            "cosine_weights": {
                "cosine": [(1.0, integration_time)],
                "sine": [(0.0, integration_time)],
            },
            "sine_weights": {
                "cosine": [(0.0, integration_time)],
                "sine": [(1.0, integration_time)],
            },
            "minus_sine_weights": {
                "cosine": [(0.0, integration_time)],
                "sine": [(-1.0, integration_time)],
            },
        })

        for setting in individual_setting:
            ro_channel_name = setting['name']
            pulse_name = f"readout_pulse_{ro_channel_name}"
            waveform_name = f"readout_wf_{ro_channel_name}"
            freq_IF = int(setting["freq_IF"] * u.MHz) 
            

            # Complete element config setting
            complete_element = resonator_element_template_dict
            self.add_element( ro_channel_name, resonator_element_template_dict )
            self.update_element_IF( ro_channel_name, freq_IF)
            complete_element["operations"]["readout"] = pulse_name

            # Complete pulse config setting
            complete_pulse = readout_pulse_template_dict
            complete_pulse["waveforms"] = {
                "I": waveform_name,
                "Q": "zero_wf",
            }
            self.__config["pulses"][pulse_name] = complete_pulse

            # Complete waveform config setting
            self.__config["waveforms"][waveform_name] = {
                "type": "constant", 
                "sample": setting["amp"]
            }
            # Complete mixers config setting
            complete_mixer = mixers_template_dict
            complete_mixer["intermediate_frequency"] = freq_IF
            self.update_mixer(mixer_name,complete_mixer)

    # Control related shows below
    
    def update_wiring_channels( self, target_q:str,mode:str,**kwargs):
        """
            modify the wiring channel for target qubit \n
            target_q : "q1"...\n
            mode: "xy" or "ro"\n
            The keyname in kwargs must be "I" and "Q":\n
            I=("con1", 3), Q=("con1", 4)
        """

        if (kwargs != {}) and (mode.lower() in ['xy','ro']):
            try:
                for channel in kwargs:
                    self.__config['elements'][f"{target_q}_{mode.lower()}"]["mixInputs"][channel] = kwargs[channel]
            except:
                raise KeyError("The keyname for a channel must be 'I' and 'Q'!")
        else:
            raise ValueError("New wiring channel should be given.")

    def update_mixer_correction(self,target_q:str,correct:tuple,mode:str):
        """
            modify the corrections for a given target qubit mixer control or readout:\n
            target_q: "q1"...\n
            correct: (1,0,0,1),\n
            mode: "xy" or "ro".
        """
        mixer_name = self.__config['elements'][f"{target_q}_{mode.lower()}"]["mixInputs"]["mixer"]
        if mode.lower() == 'xy':    
            self.__config["mixers"][mixer_name][0]["correction"] = correct
        elif mode.lower() == 'ro':
            self.__config["mixers"][mixer_name][int(target_q[-1])-1]["correction"] = correct

        print(f"Correction for {mixer_name} had been modified!")

    def create_xyChannel(self, name, element, XYinfo:dict):
        """
        name : "q2"..\n
        element ex:\n
        \n

        xyinfo is from Circuit_info().XyInfo\n
        Native gates ["x180","y180","x90","-x90","y90","-y90"]
        """

        default_native_gates = [ "x180","-x180","y180","x90","-x90","y90","-y90" ]

        element["operations"] = {
            "cw": f"const_pulse",
            "saturation": f"saturation_pulse",
        }
        for gate_name in default_native_gates:
            element["operations"][gate_name] = f"{gate_name}_pulse_{name}"
        self.add_element( f"{name}_xy", element)
        
        # Create the mixer info for control
        mixer_name = element["mixInputs"]["mixer"]
        mixer_setting = {
            "intermediate_frequency": element["intermediate_frequency"],
            "lo_frequency": element["mixInputs"]["lo_frequency"],
            "correction": (1, 0, 0, 1),
        }
        self.add_mixer( mixer_name, mixer_setting )
        # create corresponding waveform name in pulses dict, create waveform list in waveforms dict
        wave_maker = Waveform(XYinfo)
        self.__config["waveforms"]["const_wf"] = {"type": "constant", "sample":XYinfo["const_amp"]}
        self.__config["pulses"]["const_pulse"] = {
            "operation": "control",
            "length": XYinfo["const_len"],
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            }
        }
        self.__config["waveforms"]["saturation_wf"] = {"type": "constant", "sample":XYinfo["saturation_amp"]}
        self.__config["pulses"]["saturation_pulse"] = {
            "operation": "control",
            "length": XYinfo["saturation_len"],
            "waveforms": {
                "I": "saturation_wf",
                "Q": "zero_wf",
            }
        }

        for gate_name in default_native_gates:

            pulse_name = f"{gate_name}_pulse_{name}"
            waveform_name = f"{gate_name}_wf_{name}"
            self.__config["pulses"][pulse_name] = {
                "operation": "control",
                "length": XYinfo[name][f"pi_len"],
                "waveforms": {
                    "I": f"{waveform_name}_I",
                    "Q": f"{waveform_name}_Q",
                }
            }
            match gate_name:
                case "x180": a = "x"
                case "-x180": a = "-x"
                case "y180": a = "y"
                case "x90": a = "x/2"
                case "-x90": a = "-x/2"
                case "y90": a = "y/2"
                case "-y90": a = "-y/2"
                case _: a = None
            # Create waveform list, if spec is updated it also need to be updated
            for waveform_basis in ["I","Q"]:
                ''' waveform_basis is "I" or "Q" '''
                new_wf_name = f"{waveform_name}_{waveform_basis}"
                wf = wave_maker.build_XYwaveform(target_q=name,axis=a)
                self.__config["waveforms"][new_wf_name] = {"type": "arbitrary", "samples":wf[waveform_basis].tolist()}

# ===================== Update about XY =====================================
    ### directly update the frequency info into config ### 
    def update_controlFreq(self,updatedInfo:dict):
        """
            Only update the info in config about control frequency\n
            updatedInfo: from `Circuit_info.update_aXyInfo_for()`
        """
        print(updatedInfo)
        for info in updatedInfo:
            if info.split("_")[1].lower() in ["lo","if"]: # this should be update in both elements and mixers
                target_q = info.split("_")[-1]
                print(target_q)
                elements = self.__config['elements'][f"{target_q}_xy"]
                mixers = self.__config['mixers']
                mixer_name = elements["mixInputs"]["mixer"]
                # update LO or IF in elements and mixers
                if info.split("_")[1] == "LO":
                    elements["mixInputs"]["lo_frequency"] = updatedInfo[info]
                    mixers[mixer_name][0]["lo_frequency"] = updatedInfo[info]
                else: 
                    elements["intermediate_frequency"] = updatedInfo[info]
                    mixers[mixer_name][0]["intermediate_frequency"] = updatedInfo[info]
                
            else: 
                raise KeyError("Only surpport update frequenct related info to config!")
    
    ### update amp, len,...etc need an updated spec to re-build the waveform ###
    def update_controlWaveform(self,updatedSpec:dict={},target_q:str="all",**kwargs):
        '''
            If the spec about control had been updated need to re-build the waveforms in the config.\n
            A updated spec is given and call the Waveform class re-build the config.\n
            Give the specific target qubit "q1" to update if it's necessary, default for all the qubits.\n
            kwargs for assign update constant wf or saturation wf, USE: other=True/False.
        '''
        if updatedSpec != {}:
            waveform_remaker = Waveform(updatedSpec)
        else:
            raise ValueError("The updated spec should be given!")
        qs = [target_q] if target_q != 'all' else updatedSpec["register"]
        for q in qs:
            print(f"{q} update controlWaveform")
            for waveform in self.__config["elements"][f"{q}_xy"]["operations"]:
                if waveform not in ["cw", "saturation"]:
                    for waveform_basis in self.__config["pulses"][f"{waveform}_pulse_{q}"]["waveforms"]:
                        ''' waveform_basis is "I" or "Q" '''
                        waveform_name = self.__config["pulses"][f"{waveform}_pulse_{q}"]["waveforms"][waveform_basis]
                        match waveform_name.split('_')[0]:
                            case "x180": a = "x"
                            case "-x180": a = "-x"
                            case "y180": a = "y"
                            case "x90": a = "x/2"
                            case "-x90": a = "-x/2"
                            case "y90": a = "y/2"
                            case "-y90": a = "-y/2"
                            case _: a = None

                        wf = waveform_remaker.build_XYwaveform(target_q=q,axis=a)
                        
                        self.__config["waveforms"][waveform_name] = {"type": "arbitrary", "samples":wf[waveform_basis].tolist()}
            
                    # pi_len check
                    old_len = self.__config["pulses"][f"{waveform}_pulse_{q}"]['length']
                    new_len = updatedSpec[q]['pi_len']
                    print(f"new pi len{new_len}")
                    if old_len != new_len:
                        self.__config["pulses"][f"{waveform}_pulse_{q}"]['length'] = new_len

        if "other" in list(kwargs.keys()):
            if kwargs["other"]:  
                self.__config["waveforms"]["const_wf"] = {"type": "constant", "sample":updatedSpec["const_amp"]}
                self.__config["waveforms"]["saturation_wf"] = {"type": "constant", "sample":updatedSpec["saturation_amp"]}

# ================= Update about Z ===================================
    def update_z_offset(self,Zinfo:dict,mode:str="offset"):
        '''
            update the z offset in config controllers belongs to the target qubit.\n
            Zinfo is the dict belongs to the target qubit returned by the func. `Circuit_info().update_ZInfo_for()`\n
            mode for select the z info: 'offset' for maximum qubit freq. 'OFFbias' for tuned qubit away from sweetspot. 'idle' for idle point.\n
        '''
        ctrler_name = Zinfo["controller"]
        z_output = self.__config["controllers"][ctrler_name]['analog_outputs']
        channel = Zinfo['con_channel']
        if mode.lower() in ['offset','offbias','idle']:
            z_output[channel] = {'offset':Zinfo[mode]}   
        else:
            raise ValueError("mode argument should be one of 'offset', 'OFFbias' or 'idle'!")       
    
    def update_zConstWaveform(self,updatedZspec:dict):
        """
            Update the waveforms about 'const_flux_wf' in config.waveforms by the given updated z spec.
        """
        self.__config["waveforms"][f"const_flux_wf"]={
            "type": "constant", "sample": updatedZspec['const_flux_amp']
        }

    def update_zWiring(self,target_q:str='all',updatedZspec:dict={}):
        """
            Update the z port for target q. target_q default for all qubits.
        """
        '''TODO'''
        pass


# ================= Update about RO =========================
    def update_ReadoutFreqs(self,updatedInfo:dict):
        '''
            Because frequency info only for mixers and elements,\n
            update the RO freq for dynamic configuration includes IF and LO.\n
            updatedInfo: from `Circuit_info.update_RoInfo_for()`
        '''

        for info in updatedInfo:
            target_q = info.split("_")[-1]
            elements = self.__config['elements'][f'{target_q}_ro']
            mixer_name = elements["mixInputs"]["mixer"]
            match info.split("_")[1].lower():
                case 'if':
                    elements["intermediate_frequency"] = updatedInfo[info]
                    self.__config['mixers'][mixer_name][int(target_q[-1])-1]["intermediate_frequency"] = updatedInfo[info]
                case 'lo' :
                    elements["mixInputs"]["lo_frequency"] = updatedInfo[info]
                    self.__config['mixers'][mixer_name][int(target_q[-1])-1]["lo_frequency"] = updatedInfo[info]
                case _:
                    raise KeyError(f"RO update keyname goes wrong: {info.split('_')[1].lower()}")
            

    def update_Readout(self,target_q:str='all',RoInfo:dict={},integration_weights_from:str='rotated'):
        """
            Beside frequency, other info will need to update the waveform or integration weights,\n
            update the other info for dynamic configuration like amp, len.... for the specific qubit\n
            target_q: "q3", default for all the qubits,\n
            updatedInfo: from `Circuit_info.RoInfo`,\n
            integration_weights_from: which weights should be accepted 'origin', 'rotated' or 'optimal'
        """
        # Check readout pulse leneth is changed or not
        # Check time_of_flights is change or not
        match target_q:
            case 'all':
                len_rewrite = True
                TOF_rewrite = True

            case _:
                if self.__config['pulses'][f'readout_pulse_{target_q}']['length'] != RoInfo['readout_len']:
                    len_rewrite = True
                    if self.__config['elements'][f'{target_q}_ro']['time_of_flight'] != RoInfo['time_of_flight']:
                        TOF_rewrite = True
                    else:
                        TOF_rewrite = False
                else:
                    len_rewrite = False
                    if self.__config['elements'][f'{target_q}_ro']['time_of_flight'] != RoInfo['time_of_flight']:
                        TOF_rewrite = True
                    else:
                        TOF_rewrite = False

        if len_rewrite:
            q_in_config = [q.split("_")[0] for q in self.__config['elements'].keys() if q.split("_")[-1]=='ro']
            for q in q_in_config:
                # pulses length
                self.__config['pulses'][f'readout_pulse_{q}']['length'] = RoInfo['readout_len']
        if TOF_rewrite:
            q_in_config = [q.split("_")[0] for q in self.__config['elements'].keys() if q.split("_")[-1]=='ro']
            for q in q_in_config:
                # time_of_flights
                self.__config['elements'][f'{q}_ro']['time_of_flight'] = RoInfo['time_of_flight']

        qs = [target_q] if target_q != 'all' else RoInfo["register"] 
        for q in qs:
            if integration_weights_from.lower() in ['origin', 'rotated', 'optimal']:
                # integration Weight
                self.update_integrationWeight(target_q=q,updated_RO_spec=RoInfo,from_which_value=integration_weights_from)
            # waveforms values
            self.__config['waveforms'][f'readout_wf_{q}']['sample'] = RoInfo[q]['readout_amp']
        print('RO dynamic config secessfully updated!')

# ================== other functions =======================
    def export_config( self, path ):
        import pickle

        # define dictionary
        # create a binary pickle file 
        f = open(path,"wb")
        # write the python object (dict) to pickle file
        pickle.dump(self.__config,f)
        # close file
        f.close()


    def import_config( self, path ):
        import pickle
        # Read dictionary pkl file
        with open(path, 'rb') as fp:
            self.__config = pickle.load(fp)

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
    #     qs = [target_q] if target_q != 'all' else specs.__RoInfo["registered"]

    #     for q_name in qs:
    #         # Update RO info
    #         RO_freqs = {f'resonator_LO_{q_name}':specs.__RoInfo[q_name][f'resonator_LO'],f'resonator_IF_{q_name}':specs.__RoInfo[q_name][f'resonator_IF']}
    #         self.update_ReadoutFreqs(updatedInfo=RO_freqs)
    #         self.update_Readout(q_name,specs.get_spec_forConfig('ro'))
    #         # Update XY info
    #         XY_freqs = {f"qubit_LO_{q_name}":specs.__XyInfo[q_name]["qubit_LO"],f"qubit_IF_{q_name}":specs.__XyInfo[q_name]["qubit_IF"]}
    #         self.update_controlFreq(updatedInfo=XY_freqs)
    #         self.update_controlWaveform(specs.get_spec_forConfig('xy'),q_name)
    #         # Update Z info
    #         '''TODO'''
    #         zinfo = specs.update_ZInfo_for(q_name)
    #         # Update Wiring info
    #         '''TODO'''
    #     pass

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