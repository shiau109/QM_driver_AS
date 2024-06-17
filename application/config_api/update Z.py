
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
        "name":"q3",
        "offset": 0.,
        "crosstalk":{}
    },{
        "name":"q4",
        "offset": -0.0495,
        "crosstalk":{}
    },{
        "name":"q7",
        "offset": -0.0,
        "crosstalk":{}
    },{
        "name":"q8",
        "offset": -0.05,
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