"""Registry loading and access functions.

This module provides utilities for managing the corpus registry, including loading
the registry from YAML, fetching corpus data from remote sources, and accessing
individual corpus metadata entries.
"""

from pathlib import Path

import pooch
import yaml

__all__ = [
    "fetch_corpus",
    "get_entry",
    "load_registry",
]


_REGISTRY_PATH = _REGISTRY_PATH = Path(__file__).parent / "data" / "registry.yaml"
_registry_cache = None


def fetch_corpus(name: str, version: str = None) -> Path:
    """Download corpus file via pooch, return local path.

    Parameters
    ----------
    name : str
        Name of the corpus to fetch.
    version : str, optional
        Specific version to fetch. If None, fetches the latest version.

    Returns
    -------
    Path
        Local file system path to the downloaded corpus CSV file.

    Notes
    -----
    The corpus file is cached locally using pooch. Subsequent calls for the same
    corpus version will return the cached file without re-downloading.
    """
    entry = get_entry(name, version=version)

    # Use version in filename for cache separation
    filename = f"{name}_v{entry['version']}.csv"

    # Fetch with pooch
    fname = pooch.retrieve(
        url=entry["download_url"],
        known_hash=entry["hash"],
        fname=filename,
        path=pooch.os_cache("krank"),
    )
    path = Path(fname)
    return path


def get_entry(name: str, version: str = None) -> dict:
    """Get single corpus entry by name, with version info merged in.

    Parameters
    ----------
    name : str
        Name of the corpus to retrieve.
    version : str, optional
        Specific version to retrieve. If None, returns the latest version.

    Returns
    -------
    dict
        Dictionary containing corpus metadata with version-specific fields merged in.
        Includes keys like 'title', 'description', and other metadata.

    Raises
    ------
    KeyError
        If the corpus name is not found in the registry, or if the specified version
        does not exist for the corpus.

    Notes
    -----
    The nested 'versions' and 'latest' keys are removed from the returned entry,
    with version-specific information merged into the top level.
    """
    registry = load_registry()
    corpora = registry["corpora"]
    if name not in corpora:
        available = ", ".join(sorted(corpora.keys()))
        raise KeyError(f"Corpus '{name}' not found. Available: {available}")

    entry = corpora[name].copy()

    # Resolve version
    if version is None:
        version = entry["latest"]

    versions = entry.get("versions", {})
    if version not in versions:
        available_versions = ", ".join(sorted(versions.keys()))
        raise KeyError(
            f"Version '{version}' not found for '{name}'. Available: {available_versions}"
        )

    # Merge version-specific fields into entry
    version_info = versions[version]
    entry["version"] = version
    entry["download_url"] = version_info["download_url"]
    entry["hash"] = version_info["hash"]

    # Remove nested versions dict from returned entry
    del entry["versions"]
    del entry["latest"]

    return entry


def load_registry() -> dict:
    """Load registry.yaml and return as dict. Cached after first load.

    Returns
    -------
    dict
        Dictionary containing the full registry with 'corpora' and 'collections' keys.

    Notes
    -----
    The registry is cached in memory after the first load to avoid repeated file I/O.
    """
    global _registry_cache
    if _registry_cache is None:
        with open(_REGISTRY_PATH, "r", encoding="utf-8") as f:
            _registry_cache = yaml.safe_load(f)
    return _registry_cache
