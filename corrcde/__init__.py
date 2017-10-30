import os
import click
from .corrapi import *
import os
import zipfile
import subprocess

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def get_version():
    """Get the version of the code from egg_info.

    Returns:
      the package version number
    """
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        version = get_distribution(__name__).version # pylint: disable=no-member
    except DistributionNotFound:
        version = "unknown, try running `python setup.py egg_info`"

    return version

def run_cde(cmd):
    p = subprocess.Popen('cde {0}'.format(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line.decode("utf-8")),
    retval = p.wait()
    zipf = zipfile.ZipFile('cde-package.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('cde-package/', zipf)
    zipf.close()


__version__ = get_version()

@click.command()
@click.version_option(__version__)
@click.option('--config', default=None, help="The config file.")
@click.option('--cmd', default=None, help="The command to be executed.")
@click.option('--name', default=None, help="The project name.")
def cli(config, name, cmd):
    if cmd:
        run_cde(cmd)
    if config and name:
        push_to_corr(config, name)
