import click

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
    config = Config(file)
    config.read()
    OdtFiles(config['inputs']).create_output(config['output'])
    odt_template(config['output'], config['vars'])
