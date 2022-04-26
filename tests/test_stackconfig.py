import pytest

from stackconfig.stackconfig import StackConfigCompose
from stackconfig.utils.jinja2_utils import render_jijnja2_compose


@pytest.fixture()
def mock_success_subprocess(mocker):
    mocker.patch('subprocess.getoutput', return_value={"Additional property z_dummy is not allowed": "test"})


@pytest.fixture()
def mock_error_subprocess(mocker):
    mocker.patch('subprocess.getoutput', return_value={"Error": "test"})


def test_merge_compose_files(mock_success_subprocess):
    override_file = "tests/example_override.yml"
    templates = render_jijnja2_compose(
        [override_file], data_file="tests/data_example.yml"
    )
    c = StackConfigCompose(
        ["tests/example_compose.yml"] + templates, "/tmp/temp_result.yml"
    )
    c.merge_stack_compose()
    assert c.compose_dict["version"] == "3.8"
    assert "deploy" in c.compose_dict["services"]["ui"]
    assert "placement" in c.compose_dict["services"]["ui"]["deploy"]
    assert "max_replicas_per_node" in c.compose_dict["services"]["ui"]["deploy"]["placement"]
    assert c.compose_dict["services"]["ui"]["deploy"]["placement"]["max_replicas_per_node"] == 1


def test_merge_compose_files_invalid_syntax(mock_success_subprocess):
    override_file = "tests/example_override_invalid.yml"
    with pytest.raises(Exception) as err:
        templates = render_jijnja2_compose(
            [override_file], data_file="tests/data_example.yml"
        )
    assert f"Please be sure the template {override_file} is valid" in str(err)


@pytest.mark.parametrize("version", [(None), ("3.9")])
def test_merge_compose_files_invalid(version, mock_success_subprocess):
    c = StackConfigCompose(
        ["tests/example_compose.yml"], "/tmp/temp_result_invalid.yml", version
    )
    c.merge_stack_compose()
    if not version:
        version = "3.8"
    assert c.compose_dict["version"] == version
    assert "depends_on" not in c.compose_dict["services"]["api"]


def test_merge_compose_files_syntax_error(mock_success_subprocess):
    with open("/tmp/invalid-compose.yml", "+w") as file:
        file.writelines("{}\ntests: test_value".format("test"))
    with pytest.raises(Exception) as exc:
        c = StackConfigCompose(
            ["/tmp/invalid-compose.yml", "/tmp/override_invalid.yml"],
            "/tmp/temp_result_invalid.yml",
        )
        c.merge_stack_compose()
    assert "mapping values are not allowed here" in str(exc)


def test_merge_compose_files_invalid_syntax_compose_validation(mock_error_subprocess):
    override_file = "tests/example_override_invalid2.yml"
    with pytest.raises(Exception) as err:
        templates = render_jijnja2_compose(
            [override_file], data_file="tests/data_example.yml"
        )
        c = StackConfigCompose(
            ["tests/example_compose.yml"] + templates, "/tmp/temp_result.yml"
        )
        c.merge_stack_compose()
    assert f"services.service_custom.deploy.replicas contains an invalid type" in str(err)
