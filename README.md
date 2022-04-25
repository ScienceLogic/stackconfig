Stack Config
===============================

version number: 0.1.0
author: ScienceLogic

Overview
--------

Render, merge and validate docker_compose files for deploying a stack.

This library is using docker-compose merging process, but at the end
it does a final verification to let users know whether this is a valid
docker-compose for deploying a stack or not, as docker-compose doesn't validate that.

Additionally, this library will compile valid yaml jinja2 templates, so they can
be merged along with the other docker-compose files.

Installation
------------

To install use pip:

    $ pip install stackconfig


Or clone the repo:

    $ git clone https://github.com/Sciencelogic/stackconfig.git
    $ python setup.py install


Development
-----------
1. Fork
2. Set Dev Environment
```shell script
pip install -r dev_requirements.txt
pip install -r requirements.txt
pip install -e .
git checkout -b feature-more-cool-stuff
```
Test
----
```shell script
# run tests using tox
tox
# run tests with pytest
pytest
```
Version
-------
```
bumpversion major  # major release
or
bumpversion minor  # minor release
or
bumpversion patch  # hotfix release

git push origin release-n.n.0
or
git push origin hotfix-x.x.n
```

Usage example as cli tool 
-------------------------

```shell
$ stackconfig --help
Usage: stackconfig [OPTIONS]

Options:
  -f, --file PATH        docker-compose file to be merged. Accept multiple
                         arguments.
  -o, --output PATH      Output path for the final docker-compose file
                         [default: /tmp/docker-compose-20220425-16-49-16.yml]
  -d, --j2data PATH      Yaml file that contains variables to render the
                         provided jinja2 template.
  -t, --j2template PATH  Jinja2 template that needs to be a valid docker-
                         compose file after being rendered.
  --version TEXT         Set valid version for the final docker-compose file
  --help                 Show this message and exit.

```

```
$ stackconfig -f docker-compose.yml -f compose-override.yml -t docker-compose-template.yml.j2 -d data_file.yml --version 3.8 -o docker-compose-final.yml
```

Usage example using Python
--------------------------
```python
from stackconfig.stackconfig import StackConfigCompose
from stackconfig.utils.jinja2_utils import render_jijnja2_compose

jinja_env = {}
yml_compiled_files = render_jijnja2_compose(['/tmp/docker-compose.yml.j2',
                                             '/tmp/docker-compose-override-yml.j2'],
                                            data_file='/tmp/data_file.yml',
                                            data_dict=jinja_env)
# valid docker-compose files can be appended, all of them are going to be merged using the docker-compose library
yml_compiled_files.append("/tmp/docker-copmose-override2.yml")
stack_config = StackConfigCompose(yml_compiled_files, '/tmp/docker-compose-output.yml')
stack_config.merge_stack_compose()

```

Not Exactly What You Want?
----------------------------

Options that may be a good fit for you:

- https://github.com/sinzlab/jinja-compose
- https://github.com/Aisbergg/python-docker-compose-templer
- https://github.com/docker/compose