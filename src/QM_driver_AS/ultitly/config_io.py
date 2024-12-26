def import_link( link_path ):
    import tomlkit
    # Assuming 'config.toml' is your file
    with open(link_path, 'r') as file:
        content = file.read()
        link_config = tomlkit.parse(content)
    return link_config

def import_config( link_path ):

    link_config = import_link(link_path)
    from config_component.configuration import import_config
    from qspec.channel_info import import_spec
    spec = import_spec( link_config["path"]["specification"] )
    config = import_config( link_config["path"]["dynamic_config"] )

    return config, spec

def output_config( link_path, config_obj = None, spec = None ):

    link_config = import_link(link_path)
    if spec is not None:
        spec.export_spec(link_config["path"]["specification"])
    
    if config_obj is not None:
        config_obj.export_config(link_config["path"]["dynamic_config"])
        import json
        file_path = link_config["path"]["config"]
        with open(file_path, 'w') as json_file:
            json.dump(config_obj.get_config(), json_file, indent=2)