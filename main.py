import argparse
import tomli
import os
import shutil

import requests
from slugify import slugify
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

debug = True


parser = argparse.ArgumentParser()
parser.add_argument('type', help="Can be install, uninstall, or docs")
parser.add_argument('name', help="The URL of your package")
args = parser.parse_args()
Name = args.name

if args.type == "install":
    print(f"Fetching {Name}...")
    resp = urlopen(Name)
    zipfile = ZipFile(BytesIO(resp.read()))

    Config = ""
    try:
        for line in zipfile.open("config.toml").readlines():
            Config = Config + line.decode('unicode_escape')
    except KeyError as e:
        print("Error: The package is missing a config.json \n \nThe package cannot be installed. Contact the Developer "
              "of this package for a fix")
        if debug:
            print(e)
        raise SystemExit(0)

    Config = tomli.loads(Config)

    if os.path.isdir(f"{os.getcwd()}/jpm/{slugify(Config['name'])}"):
        print("Package exists, aborting install... \n")
        print(f"ERROR: Package name exists, please uninstall {Config['name']} before proceeding. To update a package "
              f"run: \njpm update {Config['name']}")
        raise SystemExit(0)

    Install = input(
        f"This will install {Config['name']} {str(Config['version'])} in {os.getcwd()}\\jpm\\{slugify(Config['name'])} \n"
        f"Is that ok (y,n): ")

    if Install.lower() == "n":
        print("Install Canceled")
        raise SystemExit(0)

    print(f"Downloading {Config['name']}...")
    Content = requests.get(Name)
    with ZipFile(BytesIO(Content.content)) as zfile:
        zfile.extractall(f"{os.getcwd()}/jpm/{slugify(Config['name'])}")

    print(f"Downloaded {Config['name']}")
    print(f"\n \nInstall Completed")

elif args.type == "uninstall":
    Uninstall = input(
        f"This will uninstall {Name} and delete {os.getcwd()}\\jpm\\{slugify(Name)} \n"
        f"Is that ok (y,n): ")

    if Uninstall.lower() == "n":
        print("Uninstall Canceled")
        raise SystemExit(0)

    print(f"Uninstalling {Name}...")
    try:
        shutil.rmtree(f"{os.getcwd()}\\jpm\\{slugify(Name)}")
    except FileNotFoundError:
        print("Package Not Found")
        raise SystemExit(0)

    print(f"Uninstalled {Name}")
    print("\n \nUninstall Complete")


elif args.type == "docs":
    try:
        with open(f"{os.getcwd()}\\jpm\\{slugify(Name)}\\config.toml") as file:
            print("\n\n")
            print(tomli.loads(file.read())["docs"])
    except FileNotFoundError as e:
        print("Error: The package is missing a config.json or does not exist \n \nThe documentation of this package "
              "cannot be found. Contact the Developer of this package for a fix")

        if debug:
            print(e)
else:
    print(f"Error: Type '{args.type}' is not a type.")
    raise SystemExit(0)
