from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
# or: requests.get(url).content

resp = urlopen("https://sasmlange.github.io/mltestlib.zip")
zipfile = ZipFile(BytesIO(resp.read()))

Config = ""
try:
    for line in zipfile.open("setup.py").readlines():
        Config = Config + line.decode('unicode_escape')
except KeyError:
    print("Error: The package is missing a setup.json \n \nThe package cannot be installed. Contact the Developer "
          "of this package for a fix")
    raise SystemExit(0)

print(Config)

