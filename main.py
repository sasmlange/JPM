debug = True

import argparse
import json
import tomli
import os
import shutil

import requests
from slugify import slugify
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

parser = argparse.ArgumentParser()
parser.add_argument('type', help="Can be install or uninstall")
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
    Install = input(f"This will install {Config['name']} {str(Config['version'])} in {os.getcwd()}\\jpm\\{slugify(Config['name'])} \n"
                    f"Is that ok (y,n): ")

    if Install.lower() == "n":
        print("Install Canceled")
        raise SystemExit(0)

    print(f"Downloading {Name}...")
    Content = requests.get(Name)
    with ZipFile(BytesIO(Content.content)) as zfile:
        zfile.extractall(f"{os.getcwd()}/jpm/{slugify(Config['name'])}")

    print(f"Downloaded {Name}")
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


else:
    print(f"Error: Type '{args.type}' is not a type.")
    raise SystemExit(0)
