import tempfile
import subprocess

from stackconfig.utils.yaml_utils import save_compose, remove_files


def validate_docker_stack_compose(compose_dict):
    """
    Validates if the final docker-compose file is valid to deploy a docker stack
    """
    name_tmp_file = tempfile.NamedTemporaryFile().name
    compose_dict["z_dummy"] = None
    save_compose(compose_dict, f"{name_tmp_file}")
    compose_dict.pop("z_dummy", None)
    result = subprocess.getoutput(
        f"docker stack deploy -c {name_tmp_file} tmp_stack"
    )
    remove_files([name_tmp_file])
    if "Additional property z_dummy is not allowed" not in result:
        print(f"INFO: docker stack validation failed: {result}. "
              f"This is only a warning as docker may not be installed or "
              f"the user doesnt have perms to execute docker cmds.")
