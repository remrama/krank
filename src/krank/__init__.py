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

    Raises
    ------
    TypeError
        If name is not a string.
    ValueError
        If name is an empty string.
    KeyError
        If the corpus name is not found in the registry.
    """
    if not isinstance(name, str):
        raise TypeError(
            f"Corpus name must be a string, got {type(name).__name__}. "
            f"Use krank.list_corpora() to see available corpora."
        )
    if not name:
        raise ValueError(
            "Corpus name cannot be empty. "
            "Use krank.list_corpora() to see available corpora."
        )
    # Load the corpus and print its string representation
    corpus = load(name)
    print(corpus)


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
    TypeError
        If name is not a string.
    ValueError
        If name is an empty string.
    KeyError
        If the corpus name is not found in the registry.
    """
    if not isinstance(name, str):
        raise TypeError(
            f"Corpus name must be a string, got {type(name).__name__}. "
            f"Use krank.list_corpora() to see available corpora."
        )
    if not name:
        raise ValueError(
            "Corpus name cannot be empty. "
            "Use krank.list_corpora() to see available corpora."
        )
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
    TypeError
        If name is not a string, or if version is not a string or None.
    ValueError
        If name is an empty string, or if version is an empty string.
    KeyError
        If the corpus name or version is not found in the registry.
    """
    if not isinstance(name, str):
        raise TypeError(
            f"Corpus name must be a string, got {type(name).__name__}. "
            f"Use krank.list_corpora() to see available corpora."
        )
    if not name:
        raise ValueError(
            "Corpus name cannot be empty. "
            "Use krank.list_corpora() to see available corpora."
        )
    if version is not None and not isinstance(version, str):
        raise TypeError(
            f"Version must be a string or None, got {type(version).__name__}. "
            f"Use krank.list_versions('{name}') to see available versions."
        )
    if version is not None and not version:
        raise ValueError(
            f"Version cannot be an empty string. "
            f"Use krank.list_versions('{name}') to see available versions, "
            f"or omit the version parameter to load the latest version."
        )
    metadata = _registry.get_entry(name, version=version)
    path = _registry.fetch_corpus(name, version=version)
    return _corpus.Corpus(name=name, metadata=metadata, path=path)
