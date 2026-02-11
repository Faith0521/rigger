from setuptools import setup, find_namespace_packages
import os
import json

source_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(source_path, "package.json"), "r") as f:
    _cgrig_package = json.load(f)

setup(
    name=_cgrig_package["name"],
    version=_cgrig_package["version"],
    description=_cgrig_package["description"],
    license="LICENSE",
    author=_cgrig_package["author"],
    author_email=_cgrig_package["authorEmail"],
    url="git@gitlab.com:cgrigtoolspro/cgrig_tools.git",
    scripts=["scripts/cgrig_cmd.py"],
    packages=find_namespace_packages(),
    zip_safe=False,
    install_requires=["GitPython"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: System :: Software Distribution"
    ]
)
