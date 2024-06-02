"""
Fetchers for Krank's Tables module.

The Tables module fetches tables that were manually extracted from journal publications.

Fetch functions in the Tables module differ slightly from others in that they
require a specific table to be requested in addition to the dataset (i.e, publication),
since each dataset may or may not have multiple tables to choose from.
"""
import inspect
import json
import re

import pooch
import pandas as pd

from importlib.resources import files


__all__ = [
    "fetch_barrett2020",
    "fetch_cariola2010",
    "fetch_cariola2014",
    "fetch_hawkins2017",
    "fetch_mariani2023",
    "fetch_mcnamara2015",
    "fetch_meador2022",
    "fetch_niederhoffer2017",
    "fetch_paquet2020",
    "fetch_pennebaker1999",
    "fetch_pennebaker2001",
    "fetch_pennebaker2007",
    "fetch_pennebaker2015",
    "fetch_boyd2022",
]



################################################################################
# Private Utilities
################################################################################

def _read_registry():
    data_dir = files("krank.data")
    with open(data_dir.joinpath("tables.json"), "rt", encoding="utf-8") as f:
        registry = json.load(f)
    return registry


def _retrieve_table(dataset, table, version, **kwargs):
    """
    Retrieve a table from a specific dataset/publication.

    Parameters
    ----------
    dataset : str
        Name of dataset (i.e., publication).
    table : str
        Name of table from within the dataset.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    fp : str
        The full local filepath of the retrieved file.
    """
    registry = _read_registry()
    if version is None:
        version = sorted(registry[dataset])[-1]
    kwargs.setdefault("fname", dataset)
    kwargs.setdefault("path", pooch.os_cache("krank").joinpath("tables"))
    kwargs.setdefault("url", registry[dataset][version][table]["url"])
    kwargs.setdefault("known_hash", "md5:" + registry[dataset][version][table]["md5"])
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
        Additional keyword arguments are passed to :func:`~python.write`.

    Returns
    -------
    data : str
        The contents of the text file.
    """
    kwargs.setdefault("mode", "rt")
    kwargs.setdefault("encoding", "utf-8")
    with open(fp, **kwargs) as f:
        return f.read()


def _parse_bib(bib):
    """
    Parse a string representation of a standard (single) bibtex citation.

    Parameters
    ----------
    bib : str
        A string representation of a standard (single) bibtex citation.

    Returns
    -------
    entry : dict
        A dictionary with key, value pairs containing the citation info.
    """
    entry_type = re.search(r"^@(\w+){", bib).group(1)
    entry_key = re.search(r"{(\w+),$", bib, re.MULTILINE).group(1)
    entry_fields = dict(re.findall(r"^\s{4}(\w+)\s+=\s+{(.*)},$", bib, re.MULTILINE))
    entry = dict(type=entry_type, key=entry_key, fields=entry_fields)
    return entry


################################################################################
# Specific Table Fetchers
################################################################################

def fetch_barrett2020(table, version=None, load=True, **kwargs):
    """
    Barrett, 2020, *Dreaming*,
    Dreams about COVID-19 versus normative dreams: Trends by gender,
    doi:`10.1037/drm0000149 <https://doi.org/10.1037/drm0000149>`_

    Table captions:

    * **Table 1:** Female Pandemic Survey Dreams Versus Hall and Van de Castle Female Normative Dreams.
    * **Table 2:** Male Pandemic Survey Dreams Versus Hall and Van de Castle Male Normative Dreams.

    .. note::
        Table 2 has "male" int the column names, but Table 1 does not have "female"
        in the same respective location. Note that Table 1 is female-only values.

    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table in ["table1", "table2"]:
        return pd.read_table(fp, index_col=0)


def fetch_cariola2010(table, version=None, load=True, **kwargs):
    """
    Cariola, 2010, *unpublished paper*,
    Assessing the latent linguistic structure of oral dream narratives,
    url:`<https://www.research.ed.ac.uk/en/publications/assessing-the-latent-linguistic-structure-of-oral-dream-narrative>`_

    Table captions
    --------------
    * **Table 1:** Descriptive statistics of linguistic variables in orally elicited dream narratives.

    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        return pd.read_table(fp, index_col=0)


def fetch_cariola2014(table, version=None, load=True, **kwargs):
    """
    Cariola, 2014, *Imagin Cogn Pers*,
    Lexical tendencies of high and low barrier personalities in narratives of everyday and dream memories,
    doi:`10.2190/IC.34.2.d <https://doi.org/10.2190/IC.34.2.d>`_

    Table captions
    --------------
    * **Table 1:** Univariate Results of Body Boundary Imagery and LIWC Linguistic Variables of Low and High Barrier Personalities in Narratives of Everyday Memories.
    * **Table 2:** Univariate Results of Body Boundary Imagery and LIWC Linguistic Variables of Low and High Barrier Personalities in Narratives of Dream Memories.

    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table in ["table1", "table2"]:
        return pd.read_table(fp, index_col=0, header=[0, 1, 2])


def fetch_hawkins2017(table, version=None, load=True, **kwargs):
    """
    Hawkins II & Boyd, 2017, *Dreaming*,
    Such stuff as dreams are made on: Dream language, LIWC norms, and personality correlates,
    Dreams about COVID-19 versus normative dreams: Trends by gender,
    doi:`10.1037/drm0000049 <https://doi.org/10.1037/drm0000049>`_

    Table captions:

    * **Table 1:** Means and Standard Deviations (SDs) for the LIWC (2007) Linguistic Features of Dreams From Studies 1 to 3.

    .. note::
        2007 Norms are a subset of the norms published in the LIWC2007 manual.

    .. note::
        Ave. recent dream is UNWEIGHTED.

    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        return pd.read_table(fp, index_col=0, header=[0, 1]).astype("float64")


def fetch_mariani2023(table, version=None, load=True, **kwargs):
    """
    Mariani et al., 2023, *Psychoanal Psychol*,
    Referential processes in dreams: A brief report from a COVID-19 dreams analysis,
    doi:`10.1037/pap0000420 <https://doi.org/10.1037/pap0000420>`_

    Table captions
    --------------
    * **Table 1:** ANOVA One Way Between Dreams' Clusters and LIWC Text Analysis.

    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        return pd.read_table(fp, index_col=0)


def fetch_mcnamara2015(table, version=None, load=True, **kwargs):
    """
    McNamara et al., 2015, *Dreaming*,
    Aggression in nightmares and unpleasant dreams and in people reporting recurrent nightmares,
    doi:`10.1037/a0039273 <https://doi.org/10.1037/a0039273>`_

    Table captions
    --------------
    * **Table 1:** LIWC and Content Scale Means and SDs Across All Types of Dreams With LIWC Norms.
    * **Table 6:** Categorical Comparisons Between Nightmares That Woke A Dreamer Up to Nightmares Where the Dreamer Was Not Woken Up.

    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table6":
        return pd.read_table(fp, index_col=0)


def fetch_meador2022(table, version=None, load=True, **kwargs):
    """
    Meador et al., 2022, *Appl Cognit Psychol*,
    Lexical tendencies of high and low barrier personalities in narratives of everyday and dream memories,
    doi:`10.1002/acp.3976 <https://doi.org/10.1002/acp.3976>`_

    Table captions
    --------------
    * **Table 1:** Change in symptoms and language.

    Parameters
    ----------
    table : str
        Name of desired table. Available tables are ``table1``.
    version : str or None
        Version of zenodo repository. If None, defaults to latest version.
    **kwargs
        Optional keyword argument(s) passed to :meth:`~pooch.Pooch.fetch`.

    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        return pd.read_table(fp, index_col=0, skiprows=[5])


def fetch_niederhoffer2017(table, version=None, load=True, **kwargs):
    """
    Niederhoffer et al., 2017, *CLPsych*,
    In your wildest dreams: the language and psychological features of dreams
    doi:`10.18653/v1/W17-3102 <https://doi.org/10.18653/v1/W17-3102>`_

    PDF available at https://aclanthology.org/W17-3102.pdf

    Table captions
    --------------
    * **Table 1:** Linguistic Processes Categories in LIWC2015.
    * **Table 2:** Top and Bottom Five dream Topics on CDI continuum.
    * **Table 3:** Most positively and negatively-correlated topics for each emotion.
    * **Appendix A:** Full list of LDA topics.
    * **Appendix B:** Sample dreams by CDI.

    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.

    Notes
    -----
    I corrected a typo in Table 2 (``plave`` -> ``plane``).
    The correct spelling is "plane", as you can see it in the corresponding Topic in Appendix A.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        return pd.read_table(fp, index_col=0, header=[0, 1])
    elif table in ["table2", "table3", "appendixA"]:
        return pd.read_table(fp, index_col=0)
    elif table == "appendixB":
        return pd.read_table(fp, header=None)


def fetch_paquet2020(table, version=None, load=True, **kwargs):
    """
    Paquet et al., 2020, *Dreaming*,
    A quantitative text analysis approach to describing posttrauma nightmares in a treatment-seeking population,
    doi:`10.1037/drm0000128 <https://doi.org/10.1037/drm0000128>`_

    Table captions
    --------------
    * **Table 1:** Participant Demographics by Group.
    * **Table 2:** Psychological Diagnosis and Nightmare Qualities Experienced by Sample.
    * **Table 3:** Results Table of LIWC Variables.

    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table in ["table1", "table2", "table3"]:
        return pd.read_table(fp, index_col=0)


def fetch_pennebaker1999(table, version=None, load=True, **kwargs):
    """
    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        df = pd.read_table(fp)
        # Move Dimensions out from Categories
        df = df.rename(columns={"Dimension": "Category"})
        df["idx"] = df["Abbrev"].isna().cumsum()
        mapping = df[df["Abbrev"].isna()].set_index("idx")["Category"]
        df.insert(0, "dimension", df["idx"].map(mapping).str.title())
        df = df.dropna(subset="Abbrev")
        df = df.drop(columns="idx")
        df["dimension"] = df["dimension"].str.split(" ", n=1).str[1]
        df = df.rename(columns=
            {"# Words": "n_words", "Judge 1": "r1", "Judge 2": "r2"}
        )
        df = df.rename(columns=str.lower)
        df = df.astype(
            {
                "dimension": "string",
                "category": "string",
                "abbrev": "string",
                "examples": "string",
                "n_words": "float64",  # Int64/Int32
                "r1": "float64",
                "r2": "float64",  # Float64
            }
        )
        return df
    elif table == "table2":
        return pd.read_table(fp, index_col=0, header=[0, 1])
    elif table == "table3":
        return pd.read_table(fp, index_col=0)


def fetch_pennebaker2001(table, version=None, load=True, **kwargs):
    """
    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        df = pd.read_table(fp)
        # Move Dimensions out from Categories
        df = df.rename(columns={"Dimension": "Category"})
        df["idx"] = df["Abbrev"].isna().cumsum()
        mapping = df[df["Abbrev"].isna()].set_index("idx")["Category"]
        df.insert(0, "dimension", df["idx"].map(mapping).str.title())
        df = df.dropna(subset="Abbrev")
        df = df.drop(columns="idx")
        df["dimension"] = df["dimension"].str.split(" ", n=1).str[1]
        df = df.rename(columns=
            {"# Words": "n_words", "Judge 1": "r1", "Judge 2": "r2"}
        )
        df = df.rename(columns=str.lower)
        df = df.astype(
            {
                "dimension": "string",
                "category": "string",
                "abbrev": "string",
                "examples": "string",
                "n_words": "float64",  # Int64/Int32
                "r1": "float64",
                "r2": "float64",  # Float64
            }
        )
        return df
    elif table == "table2":
        return pd.read_table(fp, index_col=0, header=[0, 1])
    elif table == "table3":
        return pd.read_table(fp, index_col=0)


def fetch_pennebaker2007(table, version=None, load=True, **kwargs):
    """
    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        df = pd.read_table(fp)
        df["idx"] = df["Abbrev"].isna().cumsum()
        mapping = df[df["Abbrev"].isna()].set_index("idx")["Category"]
        df.insert(0, "dimension", df["idx"].map(mapping).str.title())
        df = df.dropna(subset="Abbrev")
        df = df.drop(columns="idx")
        df[["alpha_bin", "alpha_raw"]] = df["Alpha: Binary/raw"].str.split("/", expand=True)
        df = df.drop(columns=["Alpha: Binary/raw"])
        df = df.rename(columns={"Validity (judges)": "r"})
        df = df.rename(columns={"Words in category": "n_words"})
        df = df.rename(columns=str.lower)
        df = df.astype(
            {
                "dimension": "string",
                "category": "string",
                "abbrev": "string",
                "examples": "string",
                "n_words": "float64",  # Int64/Int32
                "r": "float64",
                "alpha_bin": "float64",
                "alpha_raw": "float64",  # Float64
            }
        )
        # df = df.set_index(["Dimension", "Category"]).sort_index()
        return df
    elif table == "table2":
        df = pd.read_table(fp, index_col=0)
        df = df.replace(r",", "", regex=True)
        df = df.astype("int64")
        df.index = df.index.str.lower().str.replace(" ", "_").astype("string")
        df = df.sort_index(axis=0).sort_index(axis=1)
        return df
    elif table == "table3":
        df = pd.read_table(fp)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        df = df.rename(columns={"grand_means": "grand_mean", "grand_sds": "grand_sd"})
        df["idx"] = df["grand_mean"].isna().cumsum()
        mapping = df[df["grand_mean"].isna()].set_index("idx")["category"]
        df.insert(0, "dimension", df["idx"].map(mapping).str.title())
        df = df.dropna(subset="grand_mean")
        df = df.drop(columns="idx")
        df = df.replace(r",", "", regex=True)
        df = df.astype(
            {
                "dimension": "string",
                "category": "string",
                "emotional_writing": "float64",
                "control_writing": "float64",
                "science_articles": "float64",
                "blogs": "float64",
                "novels": "float64",
                "grand_mean": "float64",
                "grand_sd": "float64",
            }
        )
        df = df.set_index(["dimension", "category"])
        df = df.sort_index(axis=0).sort_index(axis=1)
        return df



def fetch_pennebaker2015(table, version=None, load=True, **kwargs):
    """
    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        df = pd.read_table(fp, na_values="-")
        df = df.rename(
            columns={
                "Category": "category",
                "Abbrev": "abbrev",
                "Examples": "examples",
                "Words in category": "n_words",
                "Internal Consistency (Uncorrected alpha)": "alpha_uncorrected",
                "Internal Consistency (Corrected alpha)": "alpha_corrected",
            }
        )
        df["idx"] = df["abbrev"].isna().cumsum()
        mapping = df[df["abbrev"].isna()].set_index("idx")["category"]
        df.insert(0, "dimension", df["idx"].map(mapping).str.title())
        df = df.dropna(subset="abbrev")
        df = df.drop(columns="idx")
        df = df.astype(
            {
                "dimension": "string",
                "category": "string",
                "abbrev": "string",
                "examples": "string",
                "n_words": "float64",  # Int64/Int32
                "alpha_uncorrected": "float64",
                "alpha_corrected": "float64",  # Float64
            }
        )
        # df = df.set_index(["Dimension", "Category"]).sort_index()
        return df
    elif table == "table2":
        df = pd.read_table(fp, index_col=0)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        df = df.replace(r",", "", regex=True).replace("Unknown", None).astype("float64")
        df = df.sort_index(axis=0).sort_index(axis=1)
        return df
    elif table == "table3":
        df = pd.read_table(fp, na_values="-")
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        df = df.rename(columns={"grand_means": "grand_mean", "mean_sds": "grand_sd"})
        df["idx"] = df["grand_mean"].isna().cumsum()
        mapping = df[df["grand_mean"].isna()].set_index("idx")["category"]
        df.insert(0, "dimension", df["idx"].map(mapping).str.title())
        df = df.dropna(subset="grand_mean")
        df = df.drop(columns="idx")
        df = df.replace(r",", "", regex=True)
        df = df.astype(
            {
                "dimension": "string",
                "category": "string",
                "blogs": "float64",
                "expressive_writing": "float64",
                "novels": "float64",
                "natural_speech": "float64",
                "ny_times": "float64",
                "twitter": "float64",
                "grand_mean": "float64",
                "grand_sd": "float64",
            }
        )
        df = df.set_index(["dimension", "category"])
        df = df.sort_index(axis=0).sort_index(axis=1)
        return df
    elif table == "table4":
        df = pd.read_table(fp, na_values="-")
        df = df.rename(
            columns={
                "LIWC Dimension": "category",
                "Output Label": "abbrev",
                "LIWC2015 mean": "m1",
                "LIWC2007 mean": "m2",
                "LIWC 2015/2007 Correlation": "r",
            }
        )
        df["idx"] = df["abbrev"].isna().cumsum()
        mapping = df[df["abbrev"].isna()].set_index("idx")["category"]
        df.insert(0, "dimension", df["idx"].map(mapping).str.title())
        df = df.dropna(subset="abbrev")
        df = df.drop(columns="idx")
        df = df.replace(r",", "", regex=True)
        df = df.astype(
            {
                "dimension": "string",
                "category": "string",
                "abbrev": "string",
                "m1": "float64",
                "m2": "float64",
                "r": "float64",
            }
        )
        return df


def fetch_boyd2022(table, version=None, load=True, **kwargs):
    """
    Parameters
    ----------
    table : str
        Name of table to fetch.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """

    dataset = inspect.stack()[0][3].split("_")[-1]
    fp = _retrieve_table(dataset, table, version=version, **kwargs)
    if not load:
        return fp
    elif callable(load):
        return load(fp)
    elif table == "reference":
        return _read_bib(fp)
    elif table == "table1":
        df = pd.read_table(fp, na_values="-")
        # df[["m", "sd"]] = df["Word Count M (SD)"].str.rstrip(")").str.split(" (", expand=True, regex=False)
        df = df.join(df["Word Count M (SD)"].str.extract(r"(?P<m>\d+)\s\((?P<sd>\d+)\)"))
        df = df.drop(columns="Word Count M (SD)")
        df = df.rename(columns=str.lower)
        df = df.astype({"corpus": "string", "description": "string", "m": "float64", "sd": "float64"})
        df = df.set_index("corpus").sort_index(axis=0).sort_index(axis=1)
        return df
    elif table == "table2":
        """Read Table 2 from Boyd 2022 as a pandas DataFrame."""
        df = pd.read_table(fp, na_values="-")
        # df[["n_words", "n_entries"]] = df["Words/Entries in category"].str.split("/", expand=True)
        # n_words_entries = df["Words/Entries in category"].str.split("/", expand=True)
        df = df.rename(
            columns={
                "Category": "category",
                "Abbrev.": "abbrev",
                "Description/Most frequently used exemplars": "examples",
                "Words/Entries in category": "n_words/n_entries",
                "Internal Consistency: Cronbach's alpha": "alpha",
                "Internal Consistency: KR-20": "kr20",
            }
        )
        n_words_entries = df["n_words/n_entries"].str.extract(r"(?P<n_words>\d+)/?(?P<n_entries>\d+)?")
        df.insert(3, "n_words", n_words_entries["n_words"])
        df.insert(4, "n_entries", n_words_entries["n_entries"])
        df = df.drop(columns="n_words/n_entries")
        df["idx"] = df["abbrev"].isna().cumsum()
        mapping = df[df["abbrev"].isna()].set_index("idx")["category"]
        df.insert(0, "dimension", df["idx"].map(mapping).str.title())
        df = df.dropna(subset="abbrev")
        df = df.drop(columns="idx")
        df = df.astype(
            {
                "dimension": "string",
                "category": "string",
                "abbrev": "string",
                "examples": "string",
                "n_words": "float64",
                "n_entries": "float64",
                "alpha": "float64",
                "kr20": "float64",
            }
        )
        # df = df.set_index(["Dimension", "Category"]).sort_index()
        return df
    elif table == "table3":
        df = pd.read_table(fp)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        df = df.rename(columns={"grand_means": "grand_mean", "grand_sds": "grand_sd"})
        df["idx"] = df["grand_mean"].isna().cumsum()
        mapping = df[df["grand_mean"].isna()].set_index("idx")["category"]
        df.insert(0, "dimension", df["idx"].map(mapping).str.title())
        df = df.dropna(subset="grand_mean")
        df = df.drop(columns="idx")
        df = df.replace(r",", "", regex=True)
        df = df.astype(
            {
                "dimension": "string",
                "category": "string",
                "emotional_writing": "float64",
                "control_writing": "float64",
                "science_articles": "float64",
                "blogs": "float64",
                "novels": "float64",
                "grand_mean": "float64",
                "grand_sd": "float64",
            }
        )
        df = df.set_index(["dimension", "category"])
        df = df.sort_index(axis=0).sort_index(axis=1)
        return df
    elif table == "table4":
        df = pd.read_table(fp, index_col=0, header=[0, 1])
        df.columns = df.columns.map("_".join).str.replace("-", "").str.split().str[-1].str.replace("Correlation", "r")
        df.columns = df.columns.str.replace("Mean", "m").str.replace("SD", "sd")
        df = df.rename_axis("LIWC22_abbrev")
        df.index = df.index.astype("string")
        df = df.astype("float64")
    elif table == "tableA1":
        df = pd.read_table(fp)
        # df.columns = df.columns.str.lower().str.replace(" ", "_")
        df = df.rename(
            columns={
                "Corpus": "corpus",
                "Description": "description",
                "Test Kitchen N": "n_test_kitchen",
                "Years Written": "years_written",
                "Population N": "n_population",
            }
        )
        df["n_test_kitchen"] = df["n_test_kitchen"].str.replace(",", "")
        df["n_population"] = df["n_population"].str.replace(",", "")
        df = df.astype(
            {
                "corpus": "string",
                "description": "string",
                "n_test_kitchen": "int64",
                "years_written": "string",
                "n_population": "string",
            }
        )
        df = df.set_index("corpus").sort_index(axis=0).sort_index(axis=1)
        return df
