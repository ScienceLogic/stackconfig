import tempfile

from jinja2.nativetypes import NativeEnvironment
from jinja2 import Undefined

from stackconfig.utils.yaml_utils import load_compose


def render_jijnja2_compose(templates, data_file=None, data_dict=None, jinja2_env=None):
    """
    Render jinja2 templates
    Args:
        templates:
        data_file:
        data_dict:

    Returns:
        template_files(list): list of compiled files names
    """
    template_files = []
    for template in templates:
        try:
            template_string = open(template).read()
            dict_config = {}
            jinja2env = NativeEnvironment(undefined=Undefined)

            if jinja2_env:
                jinja2env = jinja2env()
            if data_file:
                dict_config = load_compose(data_file)
            if data_dict:
                dict_config.update(data_dict)
            t = jinja2env.from_string(template_string).render(dict_config)
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(t.encode())
                name = f.name
        except Exception as err:
            raise Exception(
                f"Please be sure the template {template} is valid. Error: {str(err)}. Error-type: {type(err).__name__}. "
                f"Be sure to escape docker syntax. i.e test-{{{{ '{{.Task.ID}}' }}}}"
            )
        template_files.append(name)
    return template_files
