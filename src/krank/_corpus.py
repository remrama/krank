"""Corpus data container and text normalization utilities.

This module defines the Corpus class for managing loaded dream report corpora,
including lazy-loading of data, text normalization, and separation of report
and author metadata.
"""

from pathlib import Path

import pandas as pd

__all__ = ["Corpus"]


def _normalize_text(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """Apply universal text normalization to dream text column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing dream report text.
    text_column : str
        Name of the column containing text to normalize.

    Returns
    -------
    pd.DataFrame
        Copy of the DataFrame with normalized text in the specified column.

    Notes
    -----
    Normalization steps include:
    - Collapsing all whitespace (newlines, tabs, multiple spaces) to single spaces
    - Stripping leading and trailing whitespace
    """
    df = df.copy()

    # Collapse whitespace (newlines, tabs, multiple spaces) to single space
    df[text_column] = df[text_column].str.replace(r"\s+", " ", regex=True)

    # Strip leading/trailing whitespace
    df[text_column] = df[text_column].str.strip()

    return df


class Corpus:
    """Container for a loaded corpus with metadata.

    This class provides a lazy-loading interface for dream report corpora,
    with automatic text normalization and separation of report vs. author metadata.

    Parameters
    ----------
    name : str
        Name of the corpus.
    metadata : dict
        Dictionary containing corpus metadata including title, description,
        column mappings, and version information.
    path : Path
        Local file system path to the cached CSV file.

    Attributes
    ----------
    name : str
        Name of the corpus.
    metadata : dict
        Corpus metadata dictionary.
    path : Path
        Local path to the cached CSV file.
    reports : pd.DataFrame
        Report-level data without author metadata columns (lazy-loaded).
    authors : pd.DataFrame
        Deduplicated author-level metadata (lazy-loaded).

    Examples
    --------
    >>> import krank
    >>> corpus = krank.load("zhang2019")
    >>> corpus
    Corpus('zhang2019', n_reports=204)
    >>> corpus.reports.head()
    >>> corpus.authors.head()
    """

    def __init__(self, name: str, metadata: dict, path: Path):
        self.name = name
        self.metadata = metadata
        self._path = path
        self._df = None
        # self._df_core = None

    def __repr__(self) -> str:
        return f"Corpus('{self.name}', n_reports={self.metadata.get('n_reports', '?')})"

    @property
    def path(self) -> Path:
        """Local path to cached CSV file.

        Returns
        -------
        Path
            File system path to the corpus CSV file.
        """
        return self._path

    @property
    def reports(self) -> pd.DataFrame:
        """Report-level data (no author metadata columns).

        Lazy-loaded. Tidy format.

        Returns
        -------
        pd.DataFrame
            DataFrame containing dream reports and associated report-level metadata.
            Author-specific columns are excluded.

        Notes
        -----
        If you need the raw CSV without normalization or column mapping,
        access it via the .path attribute.

        If you want to load the data without accessing it,
        use _load_and_normalize() directly to load the dataframe in place.
        """
        df = self._load()
        author_columns = self.metadata.get("author_columns", [])
        return df.drop(columns=author_columns).copy()

    @property
    def authors(self) -> pd.DataFrame:
        """Deduplicated author-level metadata. Tidy format.

        Returns
        -------
        pd.DataFrame
            DataFrame containing unique author IDs and their associated metadata.
            Each author appears only once.

        Raises
        ------
        AssertionError
            If 'author_columns' is missing from the corpus metadata.
        """
        assert "author_columns" in self.metadata, (
            "Corpus metadata missing 'author_columns'"
        )
        df = self._load()
        author_columns = self.metadata.get("author_columns", [])
        cols = ["author"] + author_columns
        return df[cols].drop_duplicates().reset_index(drop=True)

    def _load(self) -> pd.DataFrame:
        """Load and normalize full dataframe. Called once, cached.

        Returns
        -------
        pd.DataFrame
            Fully loaded and normalized DataFrame with column mappings applied.

        Notes
        -----
        The decision to normalize text mandatorily here, as opposed to offering a
        boolean flag to disable it, is intentional to ensure consistency across
        corpora and replicable results within krank versions.
        The raw CSV is always accessible via the .path attribute if needed.
        """
        if self._df is None:
            df = pd.read_csv(self._path, encoding="utf-8")
            column_map = self.metadata.get("column_map", {})
            if column_map:
                column_map_reversed = {v: k for k, v in column_map.items()}
                df = df.rename(columns=column_map_reversed)
            df = _normalize_text(df, "report")
            self._df = df
        return self._df
