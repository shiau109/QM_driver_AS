# Import necessary file
from pathlib import Path
link_path = Path(__file__).resolve().parent.parent/"config_api"/"config_link.toml"

from QM_driver_AS.ultitly.config_io import import_config, import_link
link_config = import_link(link_path)
config_obj, spec = import_config( link_path )

config = config_obj.get_config()
qmm, _ = spec.buildup_qmm()

from ab.QM_config_dynamic import initializer

# Set parameters
from exp.SQDB import SQ_deterministic_benchmarking
my_exp = SQ_deterministic_benchmarking(config, qmm)
my_exp.initializer = initializer(120000,mode='wait')
my_exp.ro_elements = ['q4_ro']
my_exp.xy_elements = ["q4_xy"]

my_exp.sequence_repeat = 300     # are variables if process = 'repeat'

my_exp.gate = 3
    # 1 = X X
    # 2 = X -X
    # 3 = Y Y
    # 4 = Y -Y
    # 11 = Y/2 * 4 
dataset = my_exp.run( 1000 )


#Save data
save_data = True
folder_label = "1QDB_test"
if save_data: 
    from exp.save_data import DataPackager
    save_dir = link_config["path"]["output_root"]
    dp = DataPackager( save_dir, folder_label )
    dp.save_config(config)
    dp.save_nc(dataset,folder_label)

# Plot
save_figure = 1
from exp.plotting import Painter1QDB
painter = Painter1QDB()
painter.gate = my_exp.gate
figs = painter.plot(dataset,folder_label)
if save_figure: dp.save_figs( figs )
