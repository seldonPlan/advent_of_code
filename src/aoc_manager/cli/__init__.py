import click
from bs4 import BeautifulSoup
import requests
from aoc_manager.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="Test Me Project")
def test_me_project():
    click.echo("Hello world!")
