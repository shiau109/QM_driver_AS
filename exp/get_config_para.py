

def get_IF( element_name, config ):
   return config["elements"][element_name]["intermediate_frequency"]

def get_offset( element_name, config ):
    con_name, port_num = config["elements"][element_name]["singleInput"]["port"]
    return config["controllers"][con_name]["analog_outputs"][port_num]