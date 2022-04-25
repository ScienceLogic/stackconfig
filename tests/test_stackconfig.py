import os

import pytest

from stackconfig.stackconfig import StackConfigCompose
from stackconfig.utils.jinja2_utils import render_jijnja2_compose


def test_merge_compose_files():
    override_file = "tests/example_override.yml"
    templates = render_jijnja2_compose(
        [override_file], data_file="tests/data_example.yml"
    )
    c = StackConfigCompose(
        ["tests/example_compose.yml"] + templates, "/tmp/temp_result.yml"
    )
    c.merge_stack_compose()
    assert c.compose_dict["version"] == "3.3"


def test_merge_compose_files_invalid_syntax():
    override_file = "tests/example_override_invalid.yml"
    with pytest.raises(Exception) as err:
        templates = render_jijnja2_compose(
            [override_file], data_file="tests/data_example.yml"
        )
        c = StackConfigCompose(
            ["tests/example_compose.yml"] + templates, "/tmp/temp_result.yml"
        )
        c.merge_stack_compose()
    assert f"Please be sure the template {override_file} is valid" in str(err)


@pytest.mark.parametrize("version, version_result", [(None, "3.3"), ("3.8", "3.8")])
def test_merge_compose_files_invalid(version, version_result):
    c = StackConfigCompose(
        ["tests/example_compose.yml"], "/tmp/temp_result_invalid.yml", version
    )
    c.merge_stack_compose()
    assert c.compose_dict["version"] == version_result
    assert "depends_on" not in c.compose_dict["services"]["api"]


def test_merge_compose_files_syntax_error():
    with open("/tmp/invalid-compose.yml", "+w") as file:
        file.writelines("{}\ntests: test_value".format("test"))
    with pytest.raises(Exception) as exc:
        c = StackConfigCompose(
            ["/tmp/invalid-compose.yml", "/tmp/override_invalid.yml"],
            "/tmp/temp_result_invalid.yml",
        )
        c.merge_stack_compose()
    assert "mapping values are not allowed here" in str(exc)
