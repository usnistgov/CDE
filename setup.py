"""The setup.py for corr-cde.
Usage: corrcde --config="path_to_config" --name="project_name" --cmd="command_to_run"
"""

import os
import subprocess
from setuptools import setup, find_packages

p = subprocess.Popen('make install', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line.decode("utf-8")),
retval = p.wait()

setup(
    name='corrcde',
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    maintainer='Faical Yannick P. Congo',
    author_email='yannick.congo@gmail.com',
    description=('The cde binder to hook up CoRR platform.'),
    url='https://github.com/usnistgov/corr-cde',
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'corrcde = corrcde:cli'
        ],
    },
    install_requires=['click', 'configparser', 'httplib2', 'requests']
)
