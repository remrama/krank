"""
Fetchers for Krank's LIWC module.

The LIWC module fetches LIWC scores/output that from previous publications or
raw data repositories.

Fetch functions in the LIWC module differ slightly from others in that they
are often dependent on the Tables module, since that's where I put some tables
of LIWC scores that I extracted from publications.
"""
import pandas as pd

from . import tables


__all__ = [
    "fetch_barrett2020",
    "fetch_cariola2010",
]


################################################################################
# Specific fetching functions
################################################################################


def fetch_barrett2020(version=None, load=True, target_dic=None, **kwargs):
    """
    LIWC scores reported in Barrett, 2020, *Dreaming*,
    Dreams about COVID-19 versus normative dreams: Trends by gender,
    doi:`10.1037/drm0000149 <https://doi.org/10.1037/drm0000149>`_.

    These LIWC scores were reported in Table 1 and Table 2 of
    `10.1037/drm0000149 <https://doi.org/10.1037/drm0000149>`_.

    .. seealso:: Table 1 from :func:`extracts.fetch_barrett2020`

    This Table was manually extracted and deposited in the
    `Extracts from Barrett, 2020, Dreaming <https://zenodo.org/doi/10.5281/zenodo.11300322>`_
    dataset, deposited in the `Extracts Data Repository <https://zenodo.org/communities/extracts>`_
    Zenodo Community.


    * **Originally published in:** Barrett, 2020, *Dreaming*
    * **Source:** 
    """
    fp = tables.fetch_barrett2020("table1", version=version, load=False, **kwargs)
    if not load:
        return fp
    elif callable(load):
        args = inspect.getfullargspec(loader).args
        assert len(args) == 1 and args[0] == "fp"
        df = loader(fp)
        return df
    ## Custom processing ##
    return pd.read_table(fp)


def fetch_cariola2010(version=None, load=True, target_dic=None, **kwargs):
    """
    Fetch (download) the Cariola 2010 dataset and preprocess it for LIWC analysis.
    This dataset comes from the *Extracts* curated collection of datasets.
    All *Extracts* datasets are available from the `Extracts Zenodo Community
    <https://zenodo.org/communities/extracts>`_ and easy access is provided via
    the :py:mod:`krank.extracts` module.

    This dataset includes the following ``LIWC2007`` categories:
    ``posemo``, ``negemo`, and ``cause`` applied to dream reports.

    See `Cariola 2010 <https://site.com>`_ for more details.
    See `Zenodo Community Site <https://doi.org/>`_ for the tables.
    LIWC dictionary used: ``LIWC2007``
    Original language: ``English``

    * **LIWC dictionary:** ``LIWC2007``
    * **Category:** Dreams
    * **Probe:** A recent dream report

    Parameters
    ----------
    dataset : str
        Name of dataset (i.e., lexicon).
        Refer to the :mod:`~krank.lexicons` documentation for a list of all available datasets.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
        Refer to the :mod:`~krank.lexicons` documentation for a list of all available versions within each dataset.
    load : bool or callable
        If ``False`` (default), fetch the file and return the local filepath.
        If ``True``, fetch the file and load it as a :class:`pandas.DataFrame`.
        If a callable, fetch the file an load it with the custom callable.
    target_dic : str or None
        If ``None`` (default), LIWC categories remain in their original format.
        If not ``None``, LIWC categories are converted from the source dictionary
        (whatever was used in the original study) to the specified ``target_dic``.
        If ``target_dic`` is the same as the source dictionary, no action is taken.
        If not ``None``, must be one of ``LIWC1999``, ``LIWC2001``, ``LIWC2007``,
        ``LIWC2015``, or ``LIWC-22``.

        .. warning:: This feature is experimental.

            Categories change between versions of LIWC, and so these are far
            from comparable. Some categories will not be present in both source
            and target dictionaries, and thus removed from the returned dataframe.
            Other categories might have close-but-imperfect fits or might have
            changed drastically between LIWC versions. In this case, the conversions
            are still provided, so be careful with interpretations. A useful
            resource if wanting to use scores pooled across LIWC versions would
            be the `LIWC manuals <https://www.liwc.app/help/psychometrics-manuals>`_,
            where comparisons between LIWC versions are described in detail and
            analyses comparing output across LIWC versions are presented.

    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    fp = tables.fetch_cariola2010("table1", version=version, load=False, **kwargs)
    if not load:
        return fp
    elif callable(load):
        args = inspect.getfullargspec(loader).args
        assert len(args) == 1 and args[0] == "fp"
        df = loader(fp)
        return df
    ## Custom processing ##
    source_dic = "LIWC2007"
    read_kwargs = {"index_col": None, "usecols": ["Linguistic processes", "Mean", "SD"]}
    df = pd.read_table(fp, **read_kwargs)
    # Raw-to-long
    # Get all LIWC categories to be exact long-format names of the relevant dictionary
    raw_to_long = {
        r"emotions$": "emotion",
        r"clusion$": "clusive",
        r"iveness$": "ive",
        r"^Sight$": "See",
        r"person singular pronouns$": "pers singular",
    }
    df["Linguistic processes"] = df["Linguistic processes"].replace(raw_to_long, regex=True)
    # for k, v in raw_to_long.items():
    #     df.index = df.index.str.replace(k, v, regex=True)
    # Long-to-short
    # Convert all long-format LIWC category names to short-format (abbreviation) names
    long_to_short = utils.get_abbrev_mapping(source_dic)
    df["Linguistic processes"] = df["Linguistic processes"].map(long_to_short)
    # df.index = df.index.map(long_to_short)
    # Short-to-short
    # If desired, convert all short-format LIWC names to short-format LIWC names from a new dictionary
    if target_dic is not None:
        assert isinstance(target_dic, str), "`target_dic` must be a string or None"
        assert target_dic in liwc_dictionaries, f"{target_dic} is not one of the available dictionaries"
        source_to_target = get_liwc_catmap(source_dic, target_dic)
        df["Linguistic processes"] = df["Linguistic processes"].map(source_to_target)
        df = df.dropna(subset=["Linguistic processes"])
        # Log the number that were dropped
    df = sanitize_dataframe(df)
    return df

# def fetch_hawkins2017(, load=True):

# def load_hawkins():
#     fp = fetch_hawkins2017("table1", version="latest")
#     df = pd.read_table(fp, index_col=0, header=[0, 1])
#     return df

# import pandas as pd

# hawkins_2017 
# def load_hawkins2017(fp, version="latest", **kwargs):
#     if table == "table1":


# # A DataFrame for mapping between abbreviations across LIWC versions
# cat_to_cat_map = None

# # A DataFrame for mapping between categories across LIWC versions
# abbrev_to_abbrev_map = None


# def categ_to_abbrev(cat):
#     raise NotImplementedError

# def abbrev_to_cat(abbrev):
#     raise NotImplementedError

# def abbrev_to_abbrev(source_dic, target_dic):
#     raise NotImplementedError

# def categ_to_categ(source_dic, target_dic):
#     raise NotImplementedError
