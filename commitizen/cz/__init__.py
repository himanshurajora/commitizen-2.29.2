import importlib
import pkgutil
import warnings
from typing import Dict, Iterable, Type

from commitizen.vz.base import BaseCommitizen
from commitizen.vz.conventional_commits import ConventionalCommitsCz
from commitizen.vz.customize import CustomizeCommitsCz
from commitizen.vz.jira import JiraSmartCz


def discover_plugins(path: Iterable[str] = None) -> Dict[str, Type[BaseCommitizen]]:
    """Discover commitizen plugins on the path

    Args:
        path (Path, optional): If provided, 'path' should be either None or a list of paths to look for
    modules in. If path is None, all top-level modules on sys.path.. Defaults to None.

    Returns:
        Dict[str, Type[BaseCommitizen]]: Registry with found plugins
    """
    plugins = {}
    for _finder, name, _ispkg in pkgutil.iter_modules(path):
        try:
            if name.startswith("vz_"):
                plugins[name] = importlib.import_module(name).discover_this
        except AttributeError as e:
            warnings.warn(UserWarning(e.args[0]))
            continue
    return plugins


registry: Dict[str, Type[BaseCommitizen]] = {
    "vz_conventional_commits": ConventionalCommitsCz,
    "vz_jira": JiraSmartCz,
    "vz_customize": CustomizeCommitsCz,
}

registry.update(discover_plugins())
