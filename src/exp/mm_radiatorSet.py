"""
## This script is only for single readout radiation test.\n
Before you start a measurement, please make sure:\n
1) The `meas_raw_dir` in line 23 is CORRECT! Because we will import it everywhere to analyze the data.\n
2) The signal had been rotated along i chennel.
"""
import warnings
warnings.filterwarnings("ignore")

# Python program to explain os.mkdir() method 
  
# importing os module 
import os, json
from exp.save_data import save_nc
from datetime import datetime
# Dynamic config
from OnMachine.SetConfig.config_path import spec_loca, config_loca
from config_component.configuration import import_config
from config_component.channel_info import import_spec
from ab.QM_config_dynamic import initializer
from exp.relaxation_time import statistic_T1_exp
from exp.ramsey import statistic_T2_exp
from exp.readout_fidelity import readout_fidelity

# * Check here when you want an analysis please! 
meas_raw_dir = "C:/Data/20240424_5q/10K~60K"

# def create_folder(idx:int,temperature:str,result:bool=False):
#     # Parent Directory path 
#     parent_dir = os.path.join(meas_raw_dir, temperature)
#     # Directory 
#     if result:
#         parent_dir = os.path.join(parent_dir, "Results") 
#         if not os.path.isdir(parent_dir):
#             os.mkdir(parent_dir)
#     directory = f"Radiator({idx})"
    
#     # Path 
#     path = os.path.join(parent_dir, directory) 
#     if not os.path.exists(path):
#         os.mkdir(path) 
#     return path

def create_temperature_folder(temperature:str)->str:
    parent_dir = os.path.join(meas_raw_dir, temperature)
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir) 
    return parent_dir

def create_set_folder(idx:int,temperature_folder_path:str)->str:
    set_path = os.path.join(temperature_folder_path, f"Radiator({idx})")
    if not os.path.isdir(set_path):
        os.mkdir(set_path)
    return set_path 

def create_result_folder(temperature_folder_path:str)->str:
    result_path = os.path.join(temperature_folder_path, "results")
    if not os.path.isdir(result_path):
        os.mkdir(result_path)
    return result_path


if __name__ == '__main__':

    spec = import_spec( spec_loca )
    config = import_config( config_loca ).get_config()
    qmm, _ = spec.buildup_qmm()
    init_macro = initializer(170000,mode='wait')

    # 1*2  : 1.4 mins
    # 1*10 : 7.2mins

    """ Manually input """
    temp = '00K'
    ro_elements = ['q3_ro']
    f01 = 4e9                 # Because 'update XY.py' has a space inside the filename, we can't import it in this py script unfortunately.
    q_name = ['q3_xy']
    n_avg = 500
    tracking_time_min = 4 * 60
    max_time = 80 #us
    time_resolution = 0.4 #us  
    virtual_detune = 0.25
    histo_counts = 10
    shot_num = 10000

    
    """ Do NOT touch bellow """
    other_info = {}
    temp_folder_path = create_temperature_folder(temp)
    import time
    start = time.time()
    cut_time = time.time()
    if tracking_time_min == 'free':
        tracking_time_min = 500 * 24 * 60

    exp_start_time = datetime.now()
    exp_start_time = f"{exp_start_time.strftime('%Y-%m-%d')} {exp_start_time.strftime('%H:%M')}"

    set_idx = 0
    while (cut_time-start)/60 < tracking_time_min:
        if set_idx == 0:
            other_info[f"{ro_elements[0].split('_')[0]}"] = {"start_time":exp_start_time,"refIQ":[0,0],"time_past":[],"f01":f01}
        else:
            with open(os.path.join(temp_folder_path,"otherInfo.json")) as JJ:
                other_info = json.load(JJ)

        set_folder = create_set_folder(set_idx,temp_folder_path)
        # T1 measurement
        acc_T1, dataset1 = statistic_T1_exp( histo_counts, max_time, time_resolution, q_name, ro_elements, config, qmm, n_avg=n_avg, initializer=init_macro )
        # T2 measurement
        acc_T2, dataset2 = statistic_T2_exp( histo_counts, 30, 0.2, q_name, ro_elements, config, qmm, n_avg, initializer=init_macro, virtual_detune=virtual_detune)
        # readout_fidelity
        for ith in range(histo_counts):
            dataset = readout_fidelity( q_name, ro_elements, shot_num, config, qmm, init_macro)  
            save_nc(set_folder, f"{q_name}_readout_fidelity({ith})", dataset)
        
        
        save_nc(set_folder, f"{q_name}_T1", dataset1)
        save_nc(set_folder, f"{q_name}_T2", dataset2)
        cut_time = time.time()
        other_info[f"{ro_elements[0].split('_')[0]}"]["time_past"].append(cut_time-start)
        set_idx += 1

        """ Storing """
        with open(os.path.join(temp_folder_path,"otherInfo.json"),"w") as record_file:
            json.dump(other_info,record_file)
        
    end = time.time()
    print(f"cost time = {round((end-start)/60,1)} mins")

