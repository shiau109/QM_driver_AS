# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

from exp.cryoscope import Cryoscope
exp_cryoscope = Cryoscope(config, qmm)
exp_cryoscope.initializer = initializer(2000,mode='wait')
exp_cryoscope.ro_elements = ["q0_ro", "q1_ro", "q2_ro", "q3_ro", "q4_ro"]
exp_cryoscope.xy_elements = ["q4_xy"]
exp_cryoscope.z_elements = ["q4_z"]
exp_cryoscope.time_range = ( 16, 800 )
exp_cryoscope.resolution = 4

exp_cryoscope.pulse_schedule_simulation(["con1"],20000)