import click
from io import BytesIO
import requests
from zipfile import ZipFile
import os
from slugify import slugify


@click.command()
@click.argument('type')
@click.argument('name')
def action(type, name):
    if type == "install":
        click.echo(f"Downloading {name}...")
        content = requests.get(name)
        filename = slugify(name)
        path = os.getcwd()
        proceed = input(f"This will save the raw files in '{path}\\_webziprawfiles\\{filename}\\'"
                        f" Do you wish to continue (y/n)? ")

        if proceed.lower() == "y":
            backslash = "\\"
            with ZipFile(BytesIO(content.content)) as zfile:
                zfile.extractall(f'{str(path).replace(backslash, "/")}/_webziprawfiles/{filename}/')

            click.echo(f"Downloaded {name}")

            click.echo(f"Running pip...")

            os.system(f"cd {path}\\_webziprawfiles\\{filename} && pip install . && cd {path}")
        else:
            click.echo("Install Canceled")

    elif type == "uninstall":
        click.echo("Running pip...")
        os.system(f"pip uninstall {name}")
        click.echo(f" You need to delete the raw files manually")
    else:
        raise Exception(f"type {type} not found. Type --help for usage")
