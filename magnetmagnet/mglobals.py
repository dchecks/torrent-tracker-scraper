import os
import platform
from pathlib import Path, PureWindowsPath

_platform_ = platform.system()


if _platform_ == 'Windows':
    BASE_PATH = PureWindowsPath('%s\\eliasbenb\\MagnetMagnet' %  os.environ['APPDATA'])
else:
    BASE_PATH = Path('%s/eliasbenb/MagnetMagnet' % os.environ['HOME'])

images_path = BASE_PATH/'images'
icon = str(images_path / "icon.png")
github_icon = str(images_path / "github.png")
website_icon = str(images_path / "website.png")
kat_icon = str(images_path / "kat.png")
nyaa_icon = str(images_path / "nyaa.png")
tpb_icon = str(images_path / "tpb.png")
x1377_icon = str(images_path / "x1377.png")
rarbg_icon = str(images_path / "rarbg.png")

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0'