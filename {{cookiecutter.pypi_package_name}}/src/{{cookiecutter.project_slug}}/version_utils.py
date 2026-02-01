import importlib.resources
import os.path
import tomllib
from importlib.metadata import PackageNotFoundError, version
from os.path import abspath

_root_module = importlib.resources.files("{{cookiecutter.project_slug}}")
_search_paths = [abspath(str(_root_module.joinpath(p))) for p in ["../", "../../../"]]


def get_package_version(package_name: str) -> str:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Package not found"


def get_version_from_pyproject() -> str | None:
    for lol in _search_paths:
        path = os.path.join(lol, "pyproject.toml")
        try:
            with open(path, "rb") as f:
                pyproject_data = tomllib.load(f)
            return pyproject_data["project"]["version"]
        except FileNotFoundError:
            continue

    return get_package_version("{{cookiecutter.project_slug}}")
