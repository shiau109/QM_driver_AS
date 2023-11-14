from qualang_tools.units import unit
from numpy import array


#######################
# AUXILIARY FUNCTIONS #
#######################
u = unit(coerce_to_integer=True)


############################################
#            control_spec class            #
############################################

class Circuit_info:
    """This object contains the information about RO and XY control on the chip"""
    def __init__(self,q_num,**kwargs):
        self.q_num = q_num
        self.init_XyInfo()
        self.QsRoInfo = {}
        self.init_ZInfo()
        self.init_DecoInfo()
        self.spec = {}
    
    ### Below about RO information ###
    

    ### Below about XY information ###    
    def init_XyInfo(self):
        '''Info for a pi-pulse should envolve:\n
        1)pi_amp, 2)pi_len, 3)qubit_LO(GHz), 4)qubit_IF(MHz), 5)drag_coef, 6)anharmonicity(MHz), 7)AC_stark_detuning(MHz)
        '''
        self.QsXyInfo = {}
        self.QsXyInfo["register"] = []
        for idx in range(1,self.q_num+1):
            for info in ["pi_amp_q","pi_len_q","qubit_LO_q","qubit_IF_q","drag_coef_q","anharmonicity_q","AC_stark_detuning_q","waveform_func_q"]:
                self.QsXyInfo[info+str(idx)] = 0 
            self.QsXyInfo["register"].append("q"+str(idx))
        # CW pulse info
        self.QsXyInfo["const_len"] = 1000
        self.QsXyInfo["const_amp"] = 300 * u.mV
        # Saturation pulse info
        self.QsXyInfo["saturation_len"] = 5 * u.us
        self.QsXyInfo["saturation_amp"] = 0.5
        
    def update_aXyInfo_for(self,target_q,**kwargs):
        '''target_q : "q5"\n
        kwargs :\n
        amp(pi_amp)=0.2\nlen(pi_len)=20\nLO(qubit_LO, GHz)=4.3\nIF(qubit_IF, MHz)=80\ndraga(drag_coef)=0.5\ndelta or anh or d(anharmonicity, MHz)=-200\n
        AC(AC_stark_detuning, MHz)=8,func='gauss' or 'drag'\n
        If update info is related to freq return the dict for updating the config.
        '''
        new_freq = {}
        for name in list(kwargs.keys()):
            if name.lower() == 'amp':
                self.QsXyInfo["pi_amp_"+target_q] = kwargs[name] 
            elif name.lower() == 'len':
                self.QsXyInfo["pi_len_"+target_q] = kwargs[name]
            elif name.lower() == 'lo':
                self.QsXyInfo["qubit_LO_"+target_q] = kwargs[name]*u.GHz
                new_freq["qubit_LO_"+target_q] = kwargs[name]*u.GHz
            elif name.lower() == 'if':
                self.QsXyInfo["qubit_IF_"+target_q] = kwargs[name]*u.MHz
                new_freq["qubit_IF_"+target_q] = kwargs[name]*u.MHz
            elif name.lower() in ['draga','drag_coef'] :
                self.QsXyInfo["drag_coef_"+target_q] = kwargs[name]
            elif name.lower() in ["delta","d","anh","anharmonicity"]:
                self.QsXyInfo["anharmonicity_"+target_q] = kwargs[name]*u.MHz
            elif name.lower() in ['ac',"AC_stark_detuning"]:
                self.QsXyInfo["AC_stark_detuning_"+target_q] = kwargs[name]*u.MHz
            elif name.lower() in ['waveform',"func",'wf']:
                self.QsXyInfo["waveform_func_"+target_q] = kwargs[name]
            else:
                print(name.lower())
                raise KeyError("I don't know what you are talking about!")
        
        return new_freq
    
    def update_XyInfoS_for(self,target_q:str,InfoS:list):
        ''' target_q : "q5"\n
            InfoS : \n
                if type is list : [pi_amp, pi_len, qubit_LO, qubit_IF(MHz), drag_coef, anharmonicity(MHz), AC_stark_detuning]\n
                if type is dict : {"amp", "len", "LO", "IF", "drag_coef", "anharmonicity", "AC_stark_detuning"}
        '''
        if isinstance(InfoS,list):
            vals = ["pi_amp_", "pi_len_", "qubit_LO_", "qubit_IF_", "drag_coef_", "anharmonicity_", "AC_stark_detuning_"]
            for idx in range(len(InfoS)):
                if idx == 2: 
                    self.QsXyInfo[vals[idx]+target_q] = InfoS[idx]*u.GHz
                elif idx in [3,5,6]:
                    self.QsXyInfo[vals[idx]+target_q] = InfoS[idx]*u.MHz
                else:
                    self.QsXyInfo[vals[idx]+target_q] = InfoS[idx]
        else:
            raise TypeError("InfoS should be a list or dict! For a single value use `update_aPiInfo_for()`")

    def export_spec( self, path ):
        import pickle
        # define dictionary
        # create a binary pickle file 
        f = open(path,"wb")
        # write the python object (dict) to pickle file
        spec = {"XyInfo":self.QsXyInfo,"ZInfo":self.ZInfo,"DecoInfo":self.DecoInfo}
        pickle.dump(spec,f)
        # close file
        f.close()

    def import_spec( self, path ):
        import pickle
        # Read dictionary pkl file
        with open(path, 'rb') as fp:
            spec = pickle.load(fp)
        print("XY information loaded successfully!")
        self.QsXyInfo = spec["XyInfo"]
        self.DecoInfo = spec["DecoInfo"]
        self.ZInfo = spec["ZInfo"]

    ### Below about decoherence time T1 and T2
    def init_DecoInfo(self):
        """
            DecoInfo will be like : {"q1":{"T1":10000000,"T2":20000000},"q2":....}
        """
        self.DecoInfo = {}
        for idx in range(1,self.q_num+1):
            self.DecoInfo[f"q{idx}"] = {"T1":0,"T2":0}

    def update_DecoInfo_for(self,target_q:str,**kwargs):
        '''
            update the decoherence info for target qubit like T1 and T2.\n
            target_q : "q1"\n
            kwargs : "T1"= us, "T2"= us. Both or one of them are surpported.
        '''
        if kwargs != {}:
            for info in kwargs:
                if info.lower() in ["t1","t2"]:
                   self.DecoInfo[target_q][info.upper()] = kwargs[info] * u.us  
                else:
                    raise KeyError("Only two types are surpported: T1 and T2!")
        else:
            raise ValueError("You should give the info want to update in kwargs!")
        
    ### Below about the z offset info
    def init_ZInfo(self):
        """
            Zinfo will be like: {"q1":{"con_channel":1,"offset":0.05,"OFFbias":0.2,"idle":0.12},"q2":....}
        """
        self.ZInfo = {}
        for idx in range(1,self.q_num+1):
            self.ZInfo[f"q{idx}"] = {"con_channel":0,"offset":0.0,"OFFbias":0.0,"idle":0.0}

    def update_ZInfo_for(self,target_q:str,**kwargs):
        """
            Update the z info for target qubit: ctrler channel, offset, OFFbias and idle encluded.\n
            target_q: "q3"...\n
            kwargs: con_channel=2, offset=0.03, OFFbias=-0.2, idle=-0.1\n
            return the target_q's z info for config.
        """
        if kwargs != {}:
            for info in kwargs:
                if info.lower() in ["con_channel","offset","offbias","idle"]:
                    self.ZInfo[target_q][info] = kwargs[info]
                else:
                    raise KeyError("Some variables can't be identified, check the kwargs!")
        else:
            raise ValueError("You should give the info want to update in kwargs!")
        return self.ZInfo[target_q]

class Waveform:
    def __init__(self,xyInfo:dict):
        self.QsXyInfo = xyInfo
    def build_waveform(self,target_q:str,axis:str,**kwargs)->dict:
        ''' Create the pulse waveform for XY control for target qubit\n
            target_q : "q2"\n
            func : "drag" or "gauss"\n
            axis : "x" or "y" or "x/2" or "y/2" or "-x/2" or "-y/2"
        '''
        from qualang_tools.config.waveform_tools import drag_gaussian_pulse_waveforms
        # check the info is contained the data about target Q
        if target_q not in self.QsXyInfo["register"]:
            raise KeyError(f"There are not any info in 'QsXyInfo' about target {target_q}")
        # search the waveform function
        func = 'drag' if self.QsXyInfo[f"waveform_func_{target_q}"] == 0 else self.QsXyInfo[f"waveform_func_{target_q}"]
        if func.lower() in ['drag','dragg','gdrag']:
            def wf_func(amp, width, sigma, *args):
                return drag_gaussian_pulse_waveforms(amp, width, sigma, args[0], args[1], args[2])
        elif func.lower() in ['gauss','g','gaussian']:
            def wf_func(amp, width, sigma, *args):
                return drag_gaussian_pulse_waveforms(amp, width, sigma, 0, args[1], args[2])
        else:
            raise ValueError("Only surpport Gaussian or DRAG-gaussian waveform!")
        
        # Create the waveform array for I and Q
        angle = 1/len(axis.split("/")) # if "X/2" angle = 1/2, other angle = 1 (π)
        rotation_to = -1 if axis.split("/")[0][0]=="-" else 1
        scale = rotation_to*angle
        # check pulse sigma
        if kwargs != {} and list(kwargs.keys())[0].lower() in ["sigma","s","sfactor","s-factor"]:
            S_factor = kwargs[list(kwargs.keys())[0]]
        else:
            S_factor = 4

        if 'x' in axis[:2].lower():
            wf, der_wf = array(
                wf_func(self.QsXyInfo["pi_amp_"+target_q]*scale, self.QsXyInfo["pi_len_"+target_q], self.QsXyInfo["pi_len_"+target_q]/S_factor, self.QsXyInfo["drag_coef_"+target_q], self.QsXyInfo["anharmonicity_"+target_q], self.QsXyInfo["AC_stark_detuning_"+target_q])
            )
            I_wf = wf
            Q_wf = der_wf
        elif 'y' in axis[:2].lower():
            wf, der_wf = array(
                wf_func(self.QsXyInfo["pi_amp_"+target_q]*scale, self.QsXyInfo["pi_len_"+target_q], self.QsXyInfo["pi_len_"+target_q]/S_factor, self.QsXyInfo["drag_coef_"+target_q], self.QsXyInfo["anharmonicity_"+target_q], self.QsXyInfo["AC_stark_detuning_"+target_q])
            )
            I_wf = (-1)*der_wf
            Q_wf = wf
        else:
            print(axis[0].lower())
            raise ValueError("Check the given axis, It should start with 'x' or 'y'!")
    
        return {"I":I_wf, "Q":Q_wf}
        
class QM_config():
    def __init__( self ):

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
                "const_wf": {"type": "constant", "sample": 1},
                "zero_wf": {"type": "constant", "sample": 0.0},
            },
            "digital_waveforms": {
                "ON": {"samples": [(1, 0)]},
            },
            "integration_weights": {},
            "mixers": {},
        }
        
    def set_wiring( self, controller_name ):
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

    def get_config(self,*args):
        return self.__config

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
                "smearing": None,
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
           "samples": y180_Q_wf_q1.tolist()  \n
        }
        """
        if setting == None:
            setting = {
                "type": None, 
                "samples": None
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
                else: 
                    print( f"intermediate frequency {setting['intermediate_frequency']} and LO frequency {setting['lo_frequency']} is already in {name}.")

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
            "intermediate_frequency":  int(freq_IF * u.MHz), 
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
        pulse_name = f"{name}_ro_pulse"
        waveform_name = f"{name}_ro_wf"

        element["operations"] = {
            "readout": pulse_name
        }
        mixer_name = element["mixInputs"]["mixer"]
        mixer_setting = {
            "intermediate_frequency": element["intermediate_frequency"],
            "lo_frequency": element["lo_frequency"],
            "correction": (1, 0, 0, 1),
        }
        self.add_element( name, element )
        self.add_pulse( pulse_name, pulse )
        self.add_waveform( waveform_name, waveform )
        self.add_mixer( mixer_name, mixer_setting )


    def create_qubit( self, name ):

        self.create_roChannel( f"{name}_ro")
        self.create_xyChannel( f"{name}_xy")
        # create constant and saturation waveform


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
    
    def update_control_channels( self, target_q:str,**kwargs):
        """
            modify the control wiring channel for target qubit \n
            target_q : "q1"...\n
            The keyname in kwargs must be "I" and "Q":\n
            I=("con1", 3), Q=("con1", 4)
        """

        if kwargs != {}:
            try:
                for channel in kwargs:
                    self.__config['elements'][f"{target_q}_xy"]["mixInputs"][channel] = kwargs[channel]
            except:
                raise KeyError("The keyname for a channel must be 'I' and 'Q'!")
        else:
            raise ValueError("New wiring channel should be given.")

    def update_control_mixer_correction(self,target_q:str,correct:tuple):
        """
            modify the corrections for a given target qubit control mixer:\n
            target_q : "q1"...\n
            correct : (1,0,0,1)
        """
        mixer_name = self.__config['elements'][f"{target_q}_xy"]["mixInputs"]["mixer"]
        self.__config["mixers"][mixer_name][0]["correction"] = correct
        print(f"Correction for {mixer_name} had been modified!")

    def create_xyChannel(self, name, element, wiringANDmachine, XYinfo:dict):
        """
        target_q : "q2"..\n
        wiringANDmachine ex:\n
        [{\n
            "name":"q2"
            "I":("con1", 3),\n
            "Q":("con1", 4),\n
            "mixer": "octave_octave1_2"\n
        },]\n

        xyinfo is from Circuit_info().QsXyInfo\n
        Native gates ["x180","y180","x90","-x90","y90","-y90"]
        """

        # create xy dict in element
        # xy_element_template_dict = {
        #     "mixInputs": {
        #         "I": wiringInfo["I"],
        #         "Q": wiringInfo["Q"],
        #         "lo_frequency": XYinfo["qubit_LO_"+wiringInfo['name']],
        #         "mixer": wiringInfo["mixer"],
        #     },
        #     "intermediate_frequency": XYinfo["qubit_IF_"+wiringInfo['name']],  
        #     "operations": {
        #         "cw": "const_pulse",
        #         "saturation": "saturation_pulse",
        #         "x180": f"x180_pulse_{wiringInfo['name']}",
        #         "x90": f"x90_pulse_{wiringInfo['name']}",
        #         "-x90": f"-x90_pulse_{wiringInfo['name']}",
        #         "y90": f"y90_pulse_{wiringInfo['name']}",
        #         "y180": f"y180_pulse_{wiringInfo['name']}",
        #         "-y90": f"-y90_pulse_{wiringInfo['name']}",
        #     }
        # }  
        default_native_gates = [ "x180","y180","x90","-x90","y90","-y90" ]

        element["operations"] = {
            "cw": f"const_pulse",
            "saturation": f"saturation_pulse",
        }
        for gate_name in default_native_gates:
            element["operations"][gate_name] = f"{name}_{gate_name}_pulse"
        self.add_element( f"{name}_xy", element)
        
        # Create the mixer info for control
        mixer_name = element["mixInputs"]["mixer"]
        mixer_setting = {
            "intermediate_frequency": element["intermediate_frequency"],
            "lo_frequency": element["lo_frequency"],
            "correction": (1, 0, 0, 1),
        }
        self.add_mixer( mixer_name, mixer_setting )
        # create corresponding waveform name in pulses dict, create waveform list in waveforms dict
        wave_maker = Waveform(XYinfo)

        for gate_name in default_native_gates:

            pulse_name = f"{name}_{gate_name}_pulse"
            waveform_name = f"{name}_{gate_name}_wf"
            self.__config["pulses"][pulse_name] = {
                "operation": "control",
                "length": XYinfo[f"{name}_pi_len"],
                "waveforms": {
                    "I": f"{waveform_name}_I",
                    "Q": f"{waveform_name}_Q",
                }
            }
            match gate_name:
                    case "x180": a = "x"
                    case "y180": a = "y"
                    case "x90": a = "x/2"
                    case "-x90": a = "-x/2"
                    case "y90": a = "y/2"
                    case "-y90": a = "-y/2"
                    case _: a = None
            # Create waveform list, if spec is updated it also need to be updated
            for waveform_basis in ["I","Q"]:
                ''' waveform_basis is "I" or "Q" '''
                waveform_name = f"{waveform_name}_{waveform_basis}"
                wf = wave_maker.build_waveform(target_q=name,axis=a)
                self.__config["waveforms"][waveform_name] = {"type": "arbitrary", "samples":wf[waveform_basis].tolist()}


    ### directly update the frequency info into config ### 
    def update_controlFreq(self,updatedInfo:dict):
        """
            Only update the info in config about control frequency\n
            updatedInfo:{"qubit_IF_q1":200, "qubit_LO_q2":4,...}
        """
        for info in updatedInfo:
            if info.split("_")[1].lower() in ["lo","if"]: # this should be update in both elements and mixers
                target_q = info.split("_")[-1]
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
    def update_controlWaveform(self,updatedSpec:dict={},target_q:str="all"):
        '''
            If the spec about control had been updated need to re-build the waveforms in the config.\n
            A updated spec is given and call the Waveform class re-build the config.\n
            Give the specific target qubit "q1" to update if its necessary, default for all the qubits.
        '''
        if updatedSpec != {}:
            waveform_remaker = Waveform(updatedSpec)
        else:
            raise ValueError("The updated spec should be given!")
        qs = [target_q] if target_q != 'all' else updatedSpec["register"]
        for q in qs:
            for waveform in self.__config["elements"][f"{q}_xy"]["operations"]:
                if waveform not in ["cw", "saturation"]:
                    for waveform_basis in self.__config["pulses"][f"{waveform}_pulse_{q}"]["waveforms"]:
                        ''' waveform_basis is "I" or "Q" '''
                        waveform_name = self.__config["pulses"][f"{waveform}_pulse_{q}"]["waveforms"][waveform_basis]
                        posit_minus= "-" if waveform_name.split("_")[0]=='minus' else ""
                        axis = waveform_name.split("_")[1] if waveform_name.split("_")[0]=='minus' else waveform_name.split("_")[0]
                        scale = "/2" if axis[1:] == "90" else ""

                        wf = waveform_remaker.build_waveform(target_q=q,axis=posit_minus+axis[0]+scale)
                        
                        self.__config["waveforms"][waveform_name] = {"type": "arbitrary", "samples":wf[waveform_basis].tolist()}

    def update_z_offset(self,Zinfo:dict,control_mache:str="None",mode:str="offset"):
        '''
            update the z offset in config controllers belongs to the target qubit.\n
            Zinfo is the dict belongs to the target qubit returned by the func. `Circuit_info().update_ZInfo_for()`\n
            control_mache for a specific controller name : "con2", defualt is "con1".\n
            mode for select the z info: 'offset' for maximum qubit freq. 'OFFbias' for tuned qubit away from sweetspot. 'idle' for idle point.\n
        '''
        ctrler_name = 'con1' if control_mache=="None" else control_mache
        z_output = self.__config["controllers"][ctrler_name]['analog_outputs']
        channel = Zinfo['con_channel']
        if mode.lower() in ['offset','offbias','idle']:
            z_output[channel] = {'offset':Zinfo[mode]}   
        else:
            raise ValueError("mode argument should be one of 'offset', 'OFFbias' or 'idle'!")       
    
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
