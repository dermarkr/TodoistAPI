from setuptools import setup

setup(
    name="TodoistAPI",
    version="0.1",
    description="Wrapper for running API calls to Todoist's REST API",
    author="Robert Dermarkar",
    url="https://github.com/dermarkr/TodoistAPI",
    packages=["todoistAPI"],
    install_requires=[
        "requests>=2.28.2"
    ],
)