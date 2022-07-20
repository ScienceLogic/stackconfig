import yaml
import os


def save_compose(compose_definition, path_to_save, as_text=False):
    """
    Creates a new compose.yml file with the dict received
    Args:
        compose_definition(dict or str): dict of the compose file
        path_to_save(str): Local path of the compose file to save it
        as_text: save data into the file without modifications
    """
    with open(path_to_save, "w") as outfile:
        if as_text:
            outfile.write(compose_definition)
        else:
            yaml.dump(
                compose_definition, outfile, default_flow_style=False, sort_keys=False
            )


def load_compose(compose_path):
    """
    Loads the compose.yml file and return a dict
    Args:
        compose_path(str): Local path of the compose file to load
    Returns:
        compose_definition(dict): the compose file loaded
    """
    try:
        with open(compose_path) as f:
            compose_definition = yaml.safe_load(f)
    except FileNotFoundError:
        print("ERROR: no compose file found at: {}".format(compose_path))
        compose_definition = {}

    return compose_definition


def remove_files(files_list):
    if isinstance(files_list, str):
        files_list = [files_list]
    for jf in files_list:
        os.remove(jf)