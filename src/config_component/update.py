from config_component.controller import Controller, controller_read_dict
from config_component.element import Element, element_read_dict
from config_component.pulse import Pulse, pulse_read_dict
from config_component.waveform import Waveform, waveform_read_dict
from config_component.digital_waveform import DigitalWaveform, digitalWaveform_read_dict
from config_component.integration_weight import IntegrationWeights, integrationWeight_read_dict
from config_component.mixer import Mixer, mixer_read_list
from config_component.configuration import Configuration


# ===================== Update about XY =====================================
### directly update the frequency info into config ### 
def update_controlFreq( config:Configuration, updatedInfo:dict ):
    """
        Only update the info in config about control frequency\n
        updatedInfo: from `Circuit_info.update_axyInfo_for()`
    """
    for info in updatedInfo:
        print(info)
        if info.split("_")[1].lower() in ["lo","if"]: # this should be update in both elements and mixers
            target_q = info.split("_")[-1]
            target_q_idx = int(target_q[1:])
            element_name = f"{target_q}_xy"
            element = config.elements[element_name]
            mixer_name = element.input_map.mixer
            mixer = config.mixers[mixer_name]
            # print(mixer.iFChannels)
            # update LO or IF in elements and mixers
            # TODO target_q_idx should replace 0
            if info.split("_")[1] == "LO":
                element.input_map.lo_frequency = updatedInfo[info]
                mixer.iFChannels[target_q_idx].lo_frequency = updatedInfo[info]
            else: 
                element.intermediate_frequency = updatedInfo[info]
                mixer.iFChannels[target_q_idx].intermediate_frequency = updatedInfo[info]
            
        else: 
            raise KeyError("Only surpport update frequenct related info to config!")

### update amp, len,...etc need an updated spec to re-build the waveform ###
def update_controlWaveform(config:Configuration,updatedSpec:dict={},target_q:str="all",**kwargs):
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
        for waveform in config.elements[f"{q}_xy"].operations:
            if waveform not in ["cw", "saturation", "const"]:
                for waveform_basis in config.pulses[f"{waveform}_pulse_{q}"].waveforms:
                    ''' waveform_basis is "I" or "Q" '''
                    waveform_name = config.pulses[f"{waveform}_pulse_{q}"].waveforms[waveform_basis]
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
                    
                    config.waveforms[waveform_name].sample = wf[waveform_basis].tolist()
        
                # pi_len check
                old_len = config.pulses[f"{waveform}_pulse_{q}"].length
                new_len = updatedSpec[q]['pi_len']
                print(f"new pi len{new_len}")
                if old_len != new_len:
                    config.pulses[f"{waveform}_pulse_{q}"].length = new_len

            config.waveforms[f"{q}_xy_const_wf"].sample = updatedSpec["const_amp"]

# ================= Update about Z ===================================
def update_z_offset(config:Configuration,zInfo:dict,wire:dict,mode:str="offset"):
    '''
        update the z offset in config controllers belongs to the target qubit.\n
        zInfo is the dict belongs to the target qubit returned by the func. `Circuit_info().update_zInfo_for()`\n
        mode for select the z info: 'offset' for maximum qubit freq. 'OFFbias' for tuned qubit away from sweetspot. 'idle' for idle point.\n
    '''
    ctrler_name, channel = wire["z"]
    z_output = config.controllers[ctrler_name].analog_outputs

    if mode.lower() in ['offset','offbias','idle']:
        z_output[channel].offset = zInfo[mode]   
    else:
        raise ValueError("mode argument should be one of 'offset', 'OFFbias' or 'idle'!")       

def update_zConstWaveform(config,updatedZspec:dict):
    """
        Update the waveforms about 'const_flux_wf' in config.waveforms by the given updated z spec.
    """
    config.__config["waveforms"][f"const_flux_wf"]={
        "type": "constant", "sample": updatedZspec['const_flux_amp']
    }

def update_zWiring(config,target_q:str='all',updatedZspec:dict={}):
    """
        Update the z port for target q. target_q default for all qubits.
    """
    '''TODO'''
    pass


# ================= Update about RO =========================
def update_ReadoutFreqs(config:Configuration,updatedInfo:dict):
    '''
        Because frequency info only for mixers and elements,\n
        update the RO freq for dynamic configuration includes IF and LO.\n
        updatedInfo: from `Circuit_info.update_roInfo_for()`
    '''

    for info in updatedInfo:
        target_q = info.split("_")[-1]
        elements = config.elements[f'{target_q}_ro']
        mixer_name = elements.input_map.mixer
        match info.split("_")[1].lower():
            case 'if':
                elements.intermediate_frequency = updatedInfo[info]
                config.mixers[mixer_name].iFChannels[int(target_q[-1])].intermediate_frequency = updatedInfo[info]
            case 'lo' :
                elements.input_map.lo_frequency = updatedInfo[info]
                config.mixers[mixer_name].iFChannels[int(target_q[-1])].lo_frequency = updatedInfo[info]
            case _:
                raise KeyError(f"RO update keyname goes wrong: {info.split('_')[1].lower()}")
        

def update_Readout(config:Configuration,target_q:str='all',roInfo:dict={},integration_weights_from:str='rotated'):
    """
        Beside frequency, other info will need to update the waveform or integration weights,\n
        update the other info for dynamic configuration like amp, len.... for the specific qubit\n
        target_q: "q3", default for all the qubits,\n
        updatedInfo: from `Circuit_info.roInfo`,\n
        integration_weights_from: which weights should be accepted 'origin', 'rotated' or 'optimal'
    """
    # Check readout pulse leneth is changed or not
    # Check time_of_flights is change or not
    qs = [target_q] if target_q != 'all' else roInfo["register"] 

    for q in qs:
        element_name = f'{q}_ro'
        wf_name = f'{element_name}_readout_wf'
        pulse_name = f'{element_name}_readout_pulse'
        # if integration_weights_from.lower() in ['origin', 'rotated', 'optimal']:
        #     # integration Weight
        #     config.update_integrationWeight(target_q=q,updated_RO_spec=roInfo,from_which_value=integration_weights_from)
        # pulses length
        config.pulses[pulse_name].length = roInfo[q]['readout_len']
        # time_of_flights
        config.elements[element_name].time_of_flight = roInfo[q]['time_of_flight']        
        # waveforms values
        config.waveforms[wf_name].sample = roInfo[q]['readout_amp']
    print('RO dynamic config secessfully updated!')