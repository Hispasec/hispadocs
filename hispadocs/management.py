import click
import os
from click import ClickException, FileError

from hispadocs.config import Config
from hispadocs.odt import OdtFiles, OdtFile
from hispadocs.template import odt_template


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.pass_context
def cli(ctx, debug):
    pass


@cli.command()
@click.argument('file')
def generate(file):
    if not os.path.lexists(file):
        raise FileError(file)
    config_dir = os.path.abspath(os.path.dirname(file))
    config = Config(file)
    config.read()
    if not config.get('inputs'):
        raise ClickException('Define inputs parameter in config file.')
    inputs = [os.path.join(config_dir, inp) for inp in config['inputs']]
    OdtFiles(inputs).create_output(config['output'])
    odt_template(config['output'], config['vars'])
