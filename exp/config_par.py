def get_offset( element, config ):
    port_info = config["elements"][element]["singleInput"]["port"]
    con_name = port_info[0]
    port_name = port_info[1]

    offset = config["controllers"][con_name]["analog_outputs"][port_name]["offset"]
    return offset