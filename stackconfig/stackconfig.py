import tempfile

from compose.config.serialize import serialize_config
from compose.cli.command import get_config_from_options


from stackconfig.utils.yaml_utils import save_compose, load_compose, remove_files
from stackconfig.utils.validate_compose import validate_docker_stack_compose


class StackConfigCompose:
    def __init__(self, files, output, version=None):
        self.files = files
        self.output = output
        self.version = version
        self.compose_dict = dict()

    def merge_stack_compose(self):
        """
        Merges docker-compose files using docker-compose library
        """
        # using docker-compose library merge process
        compose_config = get_config_from_options(
            ".", {"--file": self.files}, {"--no-interpolate": False}
        )
        compose_config_str = serialize_config(compose_config, None, escape_dollar=True)

        # tmp file
        name_tmp_file = tempfile.NamedTemporaryFile().name
        save_compose(compose_config_str, name_tmp_file, as_text=True)
        self.compose_dict = load_compose(name_tmp_file)

        remove_files(name_tmp_file)

        if self.version and isinstance(self.version, str):
            self.compose_dict["version"] = self.version

        # validate
        self.remove_invalid_options()
        validate_docker_stack_compose(self.compose_dict)

        # save final docker-compose
        save_compose(self.compose_dict, self.output)

    def remove_invalid_options(self):
        """
        Removes options from the docker-compose
        that are going to be ignored when deploying
        a docker stack
        """
        if "version" in self.compose_dict and float(self.compose_dict["version"]) >= 3:
            for s, sd in self.compose_dict["services"].items():
                sd.pop("depends_on", None)
                self.compose_dict["services"][s] = sd

