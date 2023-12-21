from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config
from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca

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
            # [target_q, amp_scale, added_IF(MHz)]        
            modifiers = [['q1',0.2,0.7],['q2',0.2,0.39],['q3',0.2,0],['q4',0.15,0.2]] 
            for i in modifiers:
                old_if = spec.get_spec_forConfig("ro")[i[0]]["resonator_IF"]*1e-6
                old_amp = spec.get_spec_forConfig("ro")[i[0]]["readout_amp"]
                config.update_ReadoutFreqs(spec.update_RoInfo_for(target_q=i[0],IF=i[2]+old_if))
                spec.update_RoInfo_for(i[0],amp=old_amp*i[1])
                config.update_Readout(i[0],spec.get_spec_forConfig('ro'))

            spec.export_spec(spec_loca)
            config.export_config(config_loca)
        
        case "flux":
            # Update RO amp, dress RO after power dependence
            # [target_q, offset_bias, added_IF(MHz)]        
            modifiers = [['q1',-0.04,0.0],['q2',-0.055,0.0],['q3',-0.035,0],['q4',-0.03,0.014]] 
            for i in modifiers:
                old_if = spec.get_spec_forConfig("ro")[i[0]]["resonator_IF"]*1e-6
                config.update_ReadoutFreqs(spec.update_RoInfo_for(target_q=i[0],IF=i[2]+old_if))
                z = spec.update_ZInfo_for(target_q=i[0],offset=i[1])
                config.update_z_offset(z,mode='offset')
            
            spec.export_spec(spec_loca)
            config.export_config(config_loca)

        case _:
            pass
