import os
from setuptools import setup

path = os.path.dirname(os.path.realpath(__file__))
requirement_path = os.path.join(path, "requirements.txt")

if os.path.isfile(requirement_path):
    with open(requirement_path) as f_h:
        install_requires = f_h.read().splitlines()

setup(
    name="beginners-py-learn",
    version="1.0.0",
    packages=["src"],
    python_requires=">= 3.6",
    description="Beginners python with examples.",
    maintainer="paramraghavan",
    classifiers=[
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
    ],
    install_requires=install_requires
)