import click

from hispadocs.config import Config
from hispadocs.merge import OdtFiles
from hispadocs.replace import OdtReplace


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.pass_context
def cli(ctx, debug):
    pass


@cli.command()
@click.argument('file')
def generate(file):
    config = Config(file)
    config.read()
    OdtFiles(config['inputs']).create_output(config['output'])
    OdtReplace(config['output'], {'foo': 3}).replace()
