from glob import glob
from os.path import splitext, basename

from setuptools import setup, find_packages

setup(
    name="TodoistAPI",
    version="0.1",
    description="Wrapper for running API calls to Todoist's REST API",
    author="Robert Dermarkar",
    url="https://github.com/dermarkr/TodoistAPI",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=[
        "requests>=2.28.2"
    ],
)