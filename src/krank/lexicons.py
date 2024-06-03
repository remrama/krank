"""
Fetchers for Krank's Lexicons module.

The Lexicons module fetches open-source lexicons (including LIWC dictionaries).
"""
from importlib.resources import files
import inspect
import json
import re

import pandas as pd
import pooch


__all__ = [
    "fetch_honor",
    "fetch_threat",
]



################################################################################
# Private Utilities
################################################################################

def _read_registry():
    data_dir = files("krank.data")
    with open(data_dir.joinpath("lexicons.json"), "rt", encoding="utf-8") as f:
        registry = json.load(f)
    return registry


def _retrieve_lexicon(dataset, version, **kwargs):
    """
    Retrieve/download a lexicon from a remote URL (if not already retrieved).

    Parameters
    ----------
    dataset : str
        Name of dataset/lexicon.
    version : str
        Name of version.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :py:func:`pooch.retrieve`.

    Returns
    -------
    fp : str
        The full local filepath of the retrieved file.
    """
    registry = _read_registry()
    if version is None:
        version = sorted(registry[dataset])[-1]
    kwargs.setdefault("fname", dataset)
    kwargs.setdefault("path", pooch.os_cache("krank").joinpath("lexicons"))
    kwargs.setdefault("url", registry[dataset][version]["url"])
    kwargs.setdefault("known_hash", "md5:" + registry[dataset][version]["md5"])
    fp = pooch.retrieve(**kwargs)
    return fp


def _read_txt(fp, **kwargs):
    """
    Convenience function for reading a raw text file.

    Parameters
    ----------
    fp : str
        Local filepath.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :py:func:`~python.write`.

    Returns
    -------
    data : str
        The contents of the text file.
    """
    kwargs.setdefault("mode", "rt")
    kwargs.setdefault("encoding", "utf-8")
    with open(fp, **kwargs) as f:
        return f.read()



################################################################################
# Specific Lexicon Fetchers
################################################################################

def fetch_honor(version=None, load=False, **kwargs):
    """
    Fetch and read the Honor LIWC dictionary.

    Dictionary details
    ^^^^^^^^^^^^^^^^^^
    * **Name:** ``honor``
    * **Language:** English
    * **Source:** https://www.michelegelfand.com/honor-dictionary
    * **Citation:** `doi:10.1002/job.2026 <https://doi.org/10.1002/job.2026>`_

    .. note::
        This .dic file has lots of weird and inconsistent spacing.
        For example, different numbers of tabs between "columns",
        some spaces thrown in, and different number of tabs ending each line.

    Parameters
    ----------
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``True`` (default), fetch the file and load it as a :class:`~pandas.DataFrame`.
        If ``False``, fetch the file and return the local filepath.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    Filepath or DataFrame
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_lexicon(dataset=dataset, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    ## Custom loader ##
    data = _read_txt(fp)  # windows-1251/latin1
    # data = data.replace("“Honor”", '"Honor"')
    ## Fix tab-separation ##
    # First remove any end-of-line tabs or spaces
    data1 = re.sub(r"\s+$", r"\n", data, flags=re.MULTILINE).strip()
    # Replace any tabs followed by additional spacing with a single tab
    data2 = re.sub(r"\t\s+", r"\t", data1, flags=re.MULTILINE)
    # This pattern is slightly different than the more generic one,
    # because the file has lots of weird/inconsistent formatting.
    categories = re.findall(r"^([0-9]+)\t(.*)$", data, flags=re.MULTILINE)
    # categories = re.findall(r"^(\d+)\t(.*)$", data, flags=re.MULTILINE)
    # categories = re.findall(r"^(\d+)\s+([^\t]+)$", data, flags=re.MULTILINE)
    categories = {k: v.strip() for k, v in categories}
    # words = re.findall(r"^([^\t%0-9]+)((?:\s+\d+)*)", data, flags=re.MULTILINE)
    # words = re.findall(r"^([^\t\%0-9]+)((?:\s+\d+)*)", data, flags=re.MULTILINE)
    # words = re.findall(r"^([a-zA-Z\*]+)((?:\s+\d+)*)", data, flags=re.MULTILINE)
    words = re.findall(r"^([^\s\%0-9][^\t]+)((?:\s+\d+)*)", data, flags=re.MULTILINE)
    words = {k: v.strip().split() for k, v in words}
    unknown_category_ids = ["800", "999"]
    words = {k: [categories[x] for x in v if x not in unknown_category_ids] for k, v in words.items()}
    # words = {k: re.findall(r"\d+", a) for k, v in categories}
    # dictionary = {catname: catkey for catkey, catname in categories.items()}
    df = pd.DataFrame(data=False, index=list(words), columns=list(categories.values()), dtype=bool)
    df = df.sort_index(axis=0).sort_index(axis=1)  # Speeding loop up?
    for k, v in words.items():
        df.loc[k, v] = True
    return df


def fetch_threat(version=None, load=True, **kwargs):
    """
    Fetch and read the Threat LIWC dictionary.

    Dictionary details
    ^^^^^^^^^^^^^^^^^^
    * **Name:** ``threat``
    * **Language:** English
    * **Source:** https://www.michelegelfand.com/threat-dictionary
    * **Citation:** `doi:10.1073/pnas.2113891119 <https://doi.org/10.1073/pnas.2113891119>`_

    Parameters
    ----------
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    dictionary : dict
        A dictionary with abbreviated category names as keys and category words as values.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_lexicon(dataset=dataset, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    ## Custom loader ##
    threat_ngrams = _read_txt(fp).splitlines()
    df = (
        pd.DataFrame({"Ngram": threat_ngrams, "threat": 1})
        .astype({"Ngram": "string", "threat": "int64"})
        .set_index("Ngram")
        .rename_axis("Category", axis=1)
        .sort_index(axis=0)
        .sort_index(axis=1)
    )
    return df
