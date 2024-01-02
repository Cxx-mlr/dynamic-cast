__title__ = "dynamic-cast"
__author__ = "Cxx-mlr"
__license__ = "MIT"
__version__ = "0.1.0"

from .async_cast import async_cast
from .dynamic_cast import dynamic_cast

from urllib.request import urlopen
from urllib.error import URLError
from json import loads

try:
    response = urlopen("https://pypi.python.org/pypi/dynamic-cast/json", timeout=1)
except URLError:
    __newest__ = __version__
else:
    data = loads(
        response.read()
    )
    __newest__ = data["info"]["version"]

if __version__ != __newest__:
    print(f"New version of {__title__} available: {__newest__} (Using {__version__})")