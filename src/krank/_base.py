"""
Top-level Krank functions for retrieving an arbitrary dataset from each module.
"""
from . import lexicons
from . import liwc
from . import tables


__all__ = [
    "fetch_lexicon",
    "fetch_liwc",
    "fetch_table",
]


def fetch_table(dataset, table, version=None, load=True, **kwargs):
    """
    Fetch a manually-extracted table as a :class:`pandas.DataFrame`.

    Calling this function will always retrieve/download the file from its remote
    source if it has not already been retrieved (via :func:`pooch.retrieve`).

    Refer to the online :mod:`krank.tables` documentation for more details about
    the module and available tables.

    .. note:: Custom loading

        The default :mod:`krank` loader is minimal. To apply custom loading,
        either (1) set ``load=False`` to return the local filepath and load the
        file in subsequent steps, or (2) pass a callable function to ``load``
        and it will be used to load the file instead of the :mod:`krank` default
        loader.

    .. seealso::

        This is a top-level wrapper around dataset-specific functions in the
        :mod:`krank.tables` module. For example, calling
        ``krank.fetch_table("barrett2020", "table1")`` is identical to calling
        ``krank.tables.fetch_barrett2020("table1")``.

    Parameters
    ----------
    dataset : str
        Name of dataset (i.e., publication).
        Refer to the :mod:`~krank.tables` documentation for a list of all available datasets.
    table : str
        Name of table from within the dataset.
        Refer to the :mod:`~krank.tables` documentation for a list of all available tables within each dataset.
    version : str or None
        Name of version. If ``None`` (default), fetches the latest version.
        Refer to the :mod:`~krank.tables` documentation for a list of all available versions within each dataset.
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
    if (fetch_function := getattr(extracts, f"fetch_{dataset}")) is None:
        raise ValueError(f"Could not find fetching function for {dataset} Tables dataset")
    return fetch_function(table=table, version=version, load=load, **kwargs)


def fetch_lexicon(dataset, version=None, load=True, **kwargs):
    """
    Fetch a lexicon as a :class:`pandas.DataFrame`.

    Calling this function will always retrieve/download the file from its remote
    source if it has not already been retrieved (via :func:`pooch.retrieve`).

    Refer to the online :mod:`krank.lexicons` documentation for more details about
    the module and available lexicons.

    .. note:: Custom loading

        To apply custom loading, either (1) set ``load=False`` to return the
        local filepath and load the file in subsequent steps, or (2) pass a
        callable function to ``load`` and it will be used to load the file
        instead of the :mod:`krank` default loader.

    .. seealso::

        This is a top-level wrapper around dataset-specific functions in the
        :mod:`krank.lexicons` module. For example, calling
        ``krank.fetch_lexicon("threat")`` is identical to calling
        ``krank.tables.fetch_threat()``.

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
    **kwargs : dict, optional
        Additional keyword arguments are passed to :func:`pooch.retrieve`.

    Returns
    -------
    str or :class:`~pandas.DataFrame`
        Path of retrieved file if ``load`` is False, or :class:`pandas.DataFrame` if ``load`` is True.
    """
    fetch_function = getattr(lexicons, f"fetch_{dataset}", None)
    if fetch_function is None:
        raise ValueError(f"Could not find fetching function for {dataset} lexicon")
    return fetch_function(version=version, loader=loader, **kwargs)


def fetch_liwc(dataset, version=None, load=True, target_dic=None, **kwargs):
    """
    Fetch a LIWC scores dataset as a :class:`pandas.DataFrame`.

    Calling this function will always retrieve/download the file from its remote
    source if it has not already been retrieved (via :func:`pooch.retrieve`).

    Refer to the online :mod:`krank.liwc` documentation for more details about
    the module and available LIWC scores datasets.

    .. note:: Custom loading

        To apply custom loading, either (1) set ``load=False`` to return the
        local filepath and load the file in subsequent steps, or (2) pass a
        callable function to ``load`` and it will be used to load the file
        instead of the :mod:`krank` default loader.

    .. seealso::

        This is a top-level wrapper around dataset-specific functions in the
        :mod:`krank.lexicons` module. For example, calling
        ``krank.fetch_liwc("barrett2020")`` is identical to calling
        ``krank.tables.fetch_barrett2020()``.

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
    fetch_function = getattr(liwc, f"fetch_{dataset}", None)
    if fetch_function is None:
        raise ValueError(f"Could not find fetching function for {dataset} lexicon")
    return fetch_function(version=version, load=load, **kwargs)
