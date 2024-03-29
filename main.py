import argparse
import tomli
import os
import shutil

import requests
from slugify import slugify
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

debug = False


parser = argparse.ArgumentParser()
parser.add_argument('type', help="Can be install, uninstall, update or docs")
parser.add_argument('name', help="The URL of your package")
args = parser.parse_args()
Name = args.name


def download_packages(packages):
    for package in packages:
        config = fetch_package(package, True)
        if not config:
            print(f"An error has occurred while trying to fetch {package}")
        else:
            download(config, package)


def version_number_to_int(version_num: str):
    return int(version_num.replace(".", ""))


def download(config: dict, url="default"):
    if url == "default":
        url = Name

    print(f"Downloading {config['name']}...")
    content = requests.get(url)
    with ZipFile(BytesIO(content.content)) as zfile:
        zfile.extractall(f"{os.getcwd()}/jpm/{slugify(config['name'])}")

    print(f"Downloading dependencies...")

    try:
        download_packages(config['dependencies'])
    except:
        print("No dependencies found")

    print(f"\nDownloaded {config['name']}")


def fetch_package(url="default", override=True, force=False):
    if url == "default":
        url = Name

    print(f"Fetching {url}...")
    resp = urlopen(url)
    zipfile = ZipFile(BytesIO(resp.read()))

    config = ""
    try:
        for line in zipfile.open("config.toml").readlines():
            config = config + line.decode('unicode_escape')
    except KeyError as e:
        print(f"Error: The package is missing a config.toml \n \nThe package {url} cannot be installed. Contact the "
              "Developer of this package for a fix")
        if debug:
            print(e)
        if force:
            return False
        else:
            raise SystemExit(0)

    config = tomli.loads(config)

    if os.path.isdir(f"{os.getcwd()}/jpm/{slugify(config['name'])}") and not override:
        print("Package exists, aborting install... \n")
        print(f"Package {config['name']} exists. To update a package "
              f"run: \njpm update {slugify(config['name'])}")
        if force:
            return False
        else:
            raise SystemExit(0)

    return config


if args.type == "install":
    Config = fetch_package()

    Install = input(
        f"This will install {Config['name']} {str(Config['version'])} in {os.getcwd()}\\jpm\\{slugify(Config['name'])} \n"
        f"Is that ok (y,n): ")

    if Install.lower() == "n":
        print("Install Canceled")
        raise SystemExit(0)

    download(Config)

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

elif args.type == "update":
    try:
        with open(f"{os.getcwd()}\\jpm\\{slugify(Name)}\\config.toml") as file:
            content = file.read()
            old_version = tomli.loads(content)["version"]
            download_url = tomli.loads(content)["download"]

    except FileNotFoundError as e:
        print("Package Not Found")
        if debug:
            print(e)
        raise SystemExit(0)

    Config = fetch_package(download_url, True)

    if version_number_to_int(Config["version"]) <= version_number_to_int(old_version):
        print(f"No new releases found. Version {old_version} is the latest version of {Name}.")
        raise SystemExit(0)

    print(f"Upgrading {Name} {old_version} to {Name} {Config['version']}...")

    print(f"Removing {Name} {old_version}...")
    shutil.rmtree(f"{os.getcwd()}\\jpm\\{slugify(Name)}")
    print(f"{Name} {old_version} removed")

    download(Config, download_url)
    print(f"\n \nUpdate Completed")


elif args.type == "docs":
    try:
        with open(f"{os.getcwd()}\\jpm\\{slugify(Name)}\\config.toml") as file:
            print("\n\n")
            print(tomli.loads(file.read())["docs"])
    except FileNotFoundError as e:
        print("Error: The package is missing a config.toml or does not exist \n \nThe documentation of this package "
              "cannot be found. Contact the Developer of this package for a fix")

        if debug:
            print(e)
else:
    print(f"Error: Type '{args.type}' is not a type.")
    raise SystemExit(0)
