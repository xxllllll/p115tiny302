import requests
import sys

def get_latest_pypi_version(package_name):
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        return response.json()["info"]["version"]
    except Exception as e:
        print(f"Error fetching PyPI version: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_version.py <package_name>")
        sys.exit(1)
    
    package_name = sys.argv[1]
    version = get_latest_pypi_version(package_name)
    if version:
        print(version)
    else:
        sys.exit(1) 