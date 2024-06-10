
from pathlib import Path
link_path = Path(__file__).resolve().parent/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config
config_obj, spec = import_config( link_path )

from config_component.update import update_z_offset, update_z_crosstalk

# [[ 0.99954093  0.00685605 -0.01088031 -0.01185879 -0.01199802]
#  [ 0.02307034  0.99941776 -0.01729353 -0.01564188 -0.01406762]
#  [ 0.01713722  0.01930098  0.99897034 -0.02075049 -0.01185133]
#  [ 0.02022993  0.01678385  0.01898975  0.99923273 -0.02882381]
#  [ 0.01681398  0.01113205  0.00966305 -0.00497131  0.99965561]]

z_infos = [
    {
        "name":"q0",
        "offset":0.2217,
        "crosstalk":{5:0.99954093-1, 6:0.00685605, 9:-0.01088031, 10:-0.01185879, 4:-0.01199802}
    },{
        "name":"q1",
        "offset":0.1941,
        "crosstalk":{5:0.02307034, 6:0.99941776-1, 9:-0.01729353, 10:-0.01564188, 4:-0.01406762}
    },{
        "name":"q2",
        "offset":0.2063,
        "crosstalk":{5:0.01713722, 6:0.01930098, 9:0.99897034-1, 10:-0.02075049, 4:-0.01185133}
    },{
        "name":"q3",
        "offset":0.1957,
        "crosstalk":{5:0.02022993, 6:0.01678385, 9:0.01898975, 10:0.99923273-1, 4:-0.02882381}
    },{
        "name":"q4",
        "offset":0.1876,
        "crosstalk":{5:0.01681398, 6:0.01113205, 9:0.00966305, 10:-0.00497131, 4:0.99965561-1}
    },{
        "name":"q5",
        "offset":0.152,
        "crosstalk":{}
    },{
        "name":"q6",
        "offset":0.18,
        "crosstalk":{}
    },{
        "name":"q7",
        "offset":0.2027,
        "crosstalk":{}
    },{
        "name":"q8",
        "offset":0.184,
        "crosstalk":{}
    }
]
for i in z_infos:
    wiring = spec.get_spec_forConfig('wire')

    # Tune Z offset
    z_info = spec.update_ZInfo_for(target_q=i["name"],offset=i["offset"])
    # print(wiring[i[0]])
    update_z_offset( config_obj, z_info, wiring[i["name"]], mode='offset')

    z_info = spec.update_ZInfo_for(target_q=i["name"],crosstalk=i["crosstalk"])
    update_z_crosstalk( config_obj, z_info, wiring[i["name"]])
    config_dict = config_obj.get_config() 


from QM_driver_AS.ultitly.config_io import output_config
output_config( link_path, config_obj, spec )