"""krank: Fetch curated dream reports."""

from . import _corpus, _registry

__version__ = "0.1.0.dev2"

__all__ = [
    "info",
    "list_collections",
    "list_corpora",
    "list_versions",
    "load",
]


def info(name: str) -> None:
    """Pretty-print corpus metadata.

    Parameters
    ----------
    name : str
        Name of the corpus to display information for.
    """
    entry = _registry.get_entry(name)
    print(f"Corpus: {name}")
    print(f"  Title: {entry.get('title', 'N/A')}")
    print(f"  Description: {entry.get('description', 'N/A')}")
    print(f"  Reports: {entry.get('n_reports', 'N/A')}")
    print(f"  Citation: {entry.get('citation', 'N/A')}")
    print(f"  Version: {entry.get('version', 'N/A')}")
    print(f"  Collection: {entry.get('collection', 'N/A')}")


def list_collections() -> list[str]:
    """List collection names.

    Returns
    -------
    list[str]
        Sorted list of available collection names.
    """
    registry = _registry.load_registry()
    collections = registry["collections"]
    return sorted(collections)


def list_corpora() -> list[str]:
    """List corpus names.

    Returns
    -------
    list[str]
        Sorted list of available corpus names.
    """
    registry = _registry.load_registry()
    corpora = registry["corpora"]
    return sorted(corpora)


def list_versions(name: str) -> list[str]:
    """List available versions for a corpus.

    Parameters
    ----------
    name : str
        Name of the corpus to list versions for.

    Returns
    -------
    list[str]
        Sorted list of available version strings for the specified corpus.

    Raises
    ------
    KeyError
        If the corpus name is not found in the registry.
    """
    registry = _registry.load_registry()
    corpora = registry["corpora"]
    if name not in corpora:
        available = ", ".join(sorted(corpora.keys()))
        raise KeyError(f"Corpus '{name}' not found. Available: {available}")
    return sorted(corpora[name].get("versions", {}).keys())


def load(name: str, version: str = None) -> _corpus.Corpus:
    """Load a corpus by name. Downloads if not cached.

    Parameters
    ----------
    name : str
        Corpus name (e.g., "zhang2019").
    version : str, optional
        Specific version to load. If None, loads latest.

    Returns
    -------
    Corpus
        Corpus object with access to dream reports and metadata.

    Raises
    ------
    KeyError
        If the corpus name or version is not found in the registry.
    """
    metadata = _registry.get_entry(name, version=version)
    path = _registry.fetch_corpus(name, version=version)
    return _corpus.Corpus(name=name, metadata=metadata, path=path)
