import pandas as pd

from ._base import KrankRepo


class Samson2023(KrankRepo):
    """Tidy data from Samson's OSF repository.

    This dataset includes raw dream reports from various populations.
    Modified LIWC scores are also provided. See the original publication for details.
    Data is fetched from the OSF repository.

    S
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
    def __init__(self):
        super().__init__(repo_id="samson2023")


    def read_file(self, fname, reader=None, **kwargs):
        """Read a file from the repository.

        Available files:

        * ``dream.dataset_3.10.2023.csv``

        Examples
        --------
        >>> from krank.repositories import Samson2023
        >>> df = Samson2023().read_file("dream.dataset_3.10.2023.csv")
        >>> df.head()
        """
        fp = self.pup.fetch(fname)
        if reader is not None:
            return reader(fp, **kwargs)
        elif fp.endswith(".csv"):
            return pd.read_csv(fp, **kwargs)


    def read_tidy(self, *, return_authors=True):
        """Ready all dreams and authors in tidy format.

        Examples
        --------
        >>> from krank.repositories import Samson2023
        >>> dreams, authors = Samson2023.read_tidy()
        >>> dreams.head()
        """
        columns = {
            "ID": "int",
            "Population": "string",
            "Age": "int",
            "Sex": "string",
            "Number": "int",
            "WC": "int",
            "sqrt.pro": "float",
            "sqrt.threat": "float",
            "sqrt.neg": "float",
            "sqrt.anx": "float",
            "Dream": "string",
        }
        df = self.read_file("dream.dataset_3.10.2023.csv", dtype=columns)
        df["ID"] = df["ID"].map("sub-{}".format)
        df["ID"] = pd.Categorical(df["ID"].astype("string"), ordered=False)
        df["Population"] = pd.Categorical(df["Population"].astype("string"), ordered=False)
        df["Sex"] = pd.Categorical(df["Sex"].astype("string"), ordered=False)
        df = df.rename(columns={"ID": "Dreamer"})
        df = df.drop(columns=["Number", "WC", "sqrt.pro", "sqrt.threat", "sqrt.neg", "sqrt.anx"])
        authors = df[["Dreamer", "Age", "Sex", "Population"]].drop_duplicates().reset_index(drop=True)
        dreams = df.drop(columns=["Age", "Sex", "Population"])
        if return_authors:
            return dreams, authors
        return dreams
