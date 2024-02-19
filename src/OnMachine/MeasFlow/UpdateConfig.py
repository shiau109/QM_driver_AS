from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config
from OnMachine.MeasFlow.ConfigBuildUp_old import spec_loca, config_loca
import numpy as np
spec = Circuit_info(q_num=4)
config = QM_config()
spec.import_spec(spec_loca)
config.import_config(config_loca)

if __name__ == '__main__':
    mssn_cata = input("CS, power or flux?")

    match mssn_cata.lower():
        case "cs":
            # Update RO IF after Cavity Search
            # [target_q, IF(MHz)]
            new_LO = 5.96
            cavities = [['q1',-238],['q2',54],['q3',-124],['q4',141]]
            for i in cavities:
                f = spec.update_RoInfo_for(target_q=i[0],LO=new_LO,IF=i[1])
                config.update_ReadoutFreqs(f)
            # print(config.get_config()['mixers'])
            spec.export_spec(spec_loca)
            config.export_config(config_loca)

        case "power":
            # Update RO amp, dress RO after power dependence
            # [target_q, abs_amp, added_IF(MHz)]        
            modifiers = [['q1',0.04,0],['q2',0.04,0],['q3',0.04,0],['q4',0.03,0]] 
            for i in modifiers:
                old_if = spec.get_spec_forConfig("ro")[i[0]]["resonator_IF"]*1e-6
                # old_amp = spec.get_spec_forConfig("ro")[i[0]]["readout_amp"]
                config.update_ReadoutFreqs(spec.update_RoInfo_for(target_q=i[0],IF=i[2]+old_if))
                spec.update_RoInfo_for(i[0],amp=i[1])
                config.update_Readout(i[0],spec.get_spec_forConfig('ro'))

            spec.export_spec(spec_loca)
            config.export_config(config_loca)
        
        case "flux":
            # Update RO amp, dress RO after power dependence
            # [target_q, offset_bias, added_IF(MHz)]        
            modifiers = [['q1',0.11,0],['q2',0.125,0],['q3',-0.04,0],['q4',0,0]] 
            for i in modifiers:
                old_if = spec.get_spec_forConfig("ro")[i[0]]["resonator_IF"]*1e-6
                print(f"{i[0]} new RO IF = {i[2]+old_if}")
                config.update_ReadoutFreqs(spec.update_RoInfo_for(target_q=i[0],IF=i[2]+old_if))
                z = spec.update_ZInfo_for(target_q=i[0],offset=i[1])
                config.update_z_offset(z,mode='offset')
            
            spec.export_spec(spec_loca)
            config.export_config(config_loca)

        case "q":
            # Update RO amp, dress RO after power dependence
            # [target_q, offset_bias, Q freq(GHz), LO(MHz)]        
            modifiers = [['q1',0.112,3.231-0.0017,3.3],['q2',-0.084,4.2461,4.3],['q3',-0.02,3.173,3.3],['q4',0.2,3.1,3.10]] 
            for i in modifiers:
                ref_IF = (i[2]-i[3])*1000
                if np.abs(ref_IF) > 350:
                    print("Warning IF > +/-350 MHz, IF is set 350 MHz")
                    ref_IF = np.sign(ref_IF)*350
                
                config.update_controlFreq(spec.update_aXyInfo_for(target_q=i[0],IF=ref_IF,LO=i[3]))
                z = spec.update_ZInfo_for(target_q=i[0],offset=i[1])
                config.update_z_offset(z,mode='offset')
                print(ref_IF,z)
            spec.export_spec(spec_loca)
            config.export_config(config_loca)

        case "rabi":
            # Update RO amp, dress RO after power dependence
            # [target_q, Q freq(GHz), amp, len]        
            modifiers = [['q1',3.233,0.018*0.8,40],['q2',4.2461,0.1*1.05,40],['q3',3.15,0.02,40],['q4',3.1,0,40]] 
            for i in modifiers:
                qubit_LO = spec.get_spec_forConfig("xy")[i[0]]["qubit_LO"]*1e-9
                ref_IF = (i[1]-qubit_LO)*1000
                print(f"center {ref_IF}")
                print(f"amp {i[2]}")
                if np.abs(ref_IF) > 350:
                    print("Warning IF > +/-350 MHz, IF is set 350 MHz")
                    ref_IF = np.sign(ref_IF)*350
                config.update_controlFreq(spec.update_aXyInfo_for(target_q=i[0],IF=ref_IF,amp=i[2], len=i[3]))  
                config.update_controlWaveform(spec.get_spec_forConfig("xy"),target_q=i[0])          
            spec.export_spec(spec_loca)
            config.export_config(config_loca)

        case "ro":
            # Update RO amp, dress RO after power dependence
            # [target_q, add_IF(MHz), mod_amp]        
            modifiers = [['q1',0,1],['q2',0,1.25],['q3',0,1],['q4',0,1]] 
            for i in modifiers:
                print(f"{i[0]} RO")

                old_If = spec.get_spec_forConfig("ro")[i[0]]["resonator_IF"]*1e-6
                new_IF = i[1]+spec.get_spec_forConfig("ro")[i[0]]["resonator_IF"]*1e-6
                old_amp = spec.get_spec_forConfig("ro")[i[0]]["readout_amp"]
                new_amp = old_amp*i[2]
                print(f"IF {old_If} -> {new_IF}")
                print(f"amp {old_amp} -> {new_amp}")

                config.update_ReadoutFreqs(spec.update_RoInfo_for(target_q=i[0],IF=new_IF,amp=new_amp))
                config.update_Readout(i[0],spec.get_spec_forConfig("ro"))
            spec.export_spec(spec_loca)
            config.export_config(config_loca)
        case _:
            print("No such CMD")
            pass
