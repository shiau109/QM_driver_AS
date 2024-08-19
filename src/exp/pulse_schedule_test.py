# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent.parent/"application"/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

from exp.cryoscope import Cryoscope
from exp.exp_temp import ExpTemp

my_exp = ExpTemp(config, qmm)
my_exp.initializer = initializer(2000,mode='wait')

my_exp.pulse_schedule_simulation(["con1"],20000)