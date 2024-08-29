
from pathlib import Path
link_path = Path(__file__).resolve().parent/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config
config_obj, spec = import_config( link_path )

from qspec.update import update_z_offset, update_z_crosstalk, update_zWaveform

# [[ 0.99954093  0.00685605 -0.01088031 -0.01185879 -0.01199802]
#  [ 0.02307034  0.99941776 -0.01729353 -0.01564188 -0.01406762]
#  [ 0.01713722  0.01930098  0.99897034 -0.02075049 -0.01185133]
#  [ 0.02022993  0.01678385  0.01898975  0.99923273 -0.02882381]
#  [ 0.01681398  0.01113205  0.00966305 -0.00497131  0.99965561]]

z_infos = [
    {
        "name":"q2",
        "offset": 0.2,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    {
        "name":"q3",
        "offset": 0.0,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
    {
        "name":"q4",
        "offset": -0.01,
        "crosstalk":{},
        "z_amp": 0.1,
        "z_len": 1000,
    },
]
for i in z_infos:
    q_name = i["name"]
    wiring = spec.get_spec_forConfig('wire')
    z_amp = i["z_amp"]
    z_len = i["z_len"]
    if "wf" in i.keys():
        qubit_wf = i["wf"]
    else:
        qubit_wf = 0

    # Tune Z offset
    z_info = spec.update_ZInfo_for(target_q=q_name,offset=i["offset"])
    # print(wiring[i[0]])
    update_z_offset( config_obj, z_info, wiring[q_name], mode='offset')

    z_info = spec.update_ZInfo_for(target_q=q_name,crosstalk=i["crosstalk"])
    update_z_crosstalk( config_obj, z_info, wiring[q_name])
    update_zWaveform(config_obj, spec.get_spec_forConfig("z"), target_q=q_name )
    config_dict = config_obj.get_config() 


from QM_driver_AS.ultitly.config_io import output_config
output_config( link_path, config_obj, spec )