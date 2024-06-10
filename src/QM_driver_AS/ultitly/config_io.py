def import_config( config_path ):

    import tomlkit
    # Assuming 'config.toml' is your file
    with open(config_path, 'r') as file:
        content = file.read()
        link_config = tomlkit.parse(content)
        

    from config_component.configuration import import_config
    from config_component.channel_info import import_spec
    spec = import_spec( link_config["path"]["specification"] )
    config = import_config( link_config["path"]["dynamic_config"] )

    return config, spec

def output_config( config_path, config_obj, spec ):

    import tomlkit
    # Assuming 'config.toml' is your file
    with open(config_path, 'r') as file:
        content = file.read()
        link_config = tomlkit.parse(content)

    import json
    file_path = link_config["path"]["config"]
    # Open the file in write mode and use json.dump() to export the dictionary to JSON
    with open(file_path, 'w') as json_file:
        json.dump(config_obj.get_config(), json_file, indent=2)

    spec.export_spec(link_config["path"]["specification"])
    config_obj.export_config(link_config["path"]["dynamic_config"])