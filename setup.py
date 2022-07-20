from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]

setup(
    name="stackconfig",
    description="Render, merge and validate docker_compose files for deploying a stack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sciencelogic/stackconfig",
    download_url="https://github.com/Sciencelogic/stackconfig/tarball/",
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    keywords=["stackconfig", "docker-compose-config", "compose-jinja2", "docker-compose-jinja2"],
    entry_points={"console_scripts": ["stackconfig = stackconfig.cli:cli"]},
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    author="Sciencelogic",
    install_requires=install_requires,
    dependency_links=dependency_links,
)
