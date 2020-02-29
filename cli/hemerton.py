from __future__ import print_function, unicode_literals

from cli.commands import lists
import click


@click.group()
@click.pass_context
def hemerton(ctx):
    """Hemerton Command Line Interface 0.1"""
    pass


hemerton.add_command(lists)
#hemerton.add_command(test)


if __name__ == "__main__":
    hemerton()
