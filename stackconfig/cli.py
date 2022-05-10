import datetime

import click

from stackconfig.stackconfig import StackConfigCompose
from stackconfig.utils.jinja2_utils import render_jijnja2_compose
from stackconfig.utils.yaml_utils import remove_files


@click.command()
@click.option(
    "--file",
    "-f",
    multiple=True,
    type=click.Path(exists=True),
    help="docker-compose file to be merged. Accept multiple arguments.",
    default=[],
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output path for the final docker-compose file",
    show_default=True,
    default=f'/tmp/docker-compose-{datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")}.yml',
)
@click.option(
    "--j2data",
    "-d",
    type=click.Path(exists=True),
    help="Yaml file that contains variables to render the provided jinja2 template.",
    show_default=False,
    default=None,
)
@click.option(
    "--j2template",
    "-t",
    type=click.Path(exists=True),
    multiple=True,
    help="Jinja2 template that needs to be a valid docker-compose file after being rendered.",
    default=[],
)
@click.option("--version", help="Set valid version for the final docker-compose file", default=None)
def cli(file, output, j2template=None, j2data=None, version=None):
    try:
        jinja_files = []
        file = list(set(file))
        if j2template:
            if not j2data:
                print(
                    "WARNING: No yaml data file should be provided with the data to render the jinja template"
                )
            jinja_files = render_jijnja2_compose(list(set(j2template)), j2data)
            file = file + jinja_files
        stack_config = StackConfigCompose(file, output, version)
        stack_config.merge_stack_compose()
        print(f"INFO: The docker-compose file was saved in: {output}")
    except Exception as exc:
        print(f"ERROR: {str(exc)}")
        exit(1)
    finally:
        remove_files(jinja_files)
