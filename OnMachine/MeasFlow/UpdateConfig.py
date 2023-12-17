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
            # [target_q, IF]
            cavities = [['q1',-278],['q2',-167],['q3',-95],['q4',12.5]]
            for i in cavities:
                f = spec.update_RoInfo_for(target_q=i[0],IF=i[1])
                config.update_ReadoutFreqs(f)
            print(config.get_config()['mixers'])
            spec.export_spec(spec_loca)
            config.export_config(config_loca)

        case "power":
            # Update RO amp, dress RO after power dependence
            # [target_q, amp_scale, added_IF]        
            modifiers = [['q1',0.08,0.83],['q2',0.1,3.16],['q3',0.08,4.63],['q4',0.1,2]] 
            for i in modifiers:
                old_if = spec.get_spec_forConfig("ro")[i[0]]["resonator_IF"]*1e-6
                old_amp = spec.get_spec_forConfig("ro")[i[0]]["readout_amp"]
                config.update_ReadoutFreqs(spec.update_RoInfo_for(target_q=i[0],IF=i[2]+old_if))
                spec.update_RoInfo_for(i[0],amp=old_amp*i[1])
                config.update_Readout(i[0],spec.get_spec_forConfig('ro'))

            spec.export_spec(spec_loca)
            config.export_config(config_loca)
        
        case "flux":
            pass

        case _:
            pass
