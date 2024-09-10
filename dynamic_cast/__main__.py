from urllib.request import urlopen
from urllib.error import URLError
import json
from packaging import version

from . import __version__ as current_version

def main():
    pypi_url = "https://pypi.python.org/pypi/dynamic-cast/json"
    try:
        response = urlopen(pypi_url, timeout=1)

        data = json.loads(response.read())
        
        latest_version = data["info"]["version"]
        package_name = data["info"]["name"]
    except URLError:
        print("Network issue: Unable to check for updates.")
    except (KeyError, ValueError):
        print("Error: Unexpected data format from PyPI.")
    else:
        if version.parse(current_version) < version.parse(latest_version):
            print(f"A new version of {package_name} is available: {latest_version} (Current version: {current_version})")
        else:
            print(f"{package_name} is already up to date (version {current_version}).")
        return
    
    print(f"dynamic-cast {current_version}")