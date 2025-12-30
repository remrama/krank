"""Corpus data container and text normalization utilities.

This module defines the Corpus class for managing loaded dream report corpora,
including lazy-loading of data, text normalization, and separation of report
and author metadata.
"""

import warnings
from pathlib import Path

import ftfy
import pandas as pd
from ftfy import TextFixerConfig

from ._schemas import AuthorsSchema, ReportsSchema

__all__ = ["Corpus"]


def _extract_author_year(citation: str) -> str:
    """Extract author(s) and year from a citation string.

    Parameters
    ----------
    citation : str
        Full citation string.

    Returns
    -------
    str
        Shortened citation with just author(s) and year (e.g., "Smith et al., 2020").

    Notes
    -----
    Extracts the portion of the citation before the first ")." which typically
    contains the authors and year. Falls back to first 50 chars if not found.
    """
    # Split by first ")." to get author(s) and year
    if ")." in citation:
        return citation.split(").")[0] + ")"
    # If we can't parse it, return first 50 chars
    return citation[:50] + "..." if len(citation) > 50 else citation


# Configure ftfy with all options explicitly set
# This provides a single config location for most normalization decisions
# Defined at module level for performance (avoid recreating on each call)
_FTFY_CONFIG = TextFixerConfig(
    unescape_html="auto",  # Unescape HTML entities when safe
    remove_terminal_escapes=True,  # Remove ANSI terminal escapes
    fix_encoding=True,  # Fix mojibake
    restore_byte_a0=True,  # Restore non-breaking spaces
    replace_lossy_sequences=True,  # Handle � replacement characters
    decode_inconsistent_utf8=True,  # Fix mixed encoding issues
    fix_c1_controls=True,  # Fix C1 control characters
    fix_latin_ligatures=True,  # Fix ligatures like ﬁ → fi
    fix_character_width=True,  # Fix full-width characters
    uncurl_quotes=True,  # Replace curly quotes with straight quotes
    fix_line_breaks=True,  # Normalize line breaks
    fix_surrogates=True,  # Fix surrogate pairs
    remove_control_chars=True,  # Remove control characters
    normalization="NFC",  # Apply NFC unicode normalization
    max_decode_length=1000000,  # Max segment length for processing
    explain=False,  # Don't generate explanations (for performance)
)


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

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame or text_column is not a string.
    ValueError
        If text_column is not in the DataFrame, or if any dream reports are
        empty strings after normalization.

    Warnings
    --------
    UserWarning
        If replacement characters (�) remain after normalization, indicating
        unrecoverable text corruption.

    Notes
    -----
    Normalization steps applied in order:

    1. Apply ftfy text fixing with explicit configuration:
       - Fix mojibake (text decoded in wrong encoding)
       - Replace curly quotes with straight quotes
       - Apply NFC unicode normalization
       - Handle replacement characters (�) in lossy sequences where possible
       - Fix various encoding issues and control characters

    2. Replace ellipsis character (…) with three dots (...)

    3. Collapse all whitespace (newlines, tabs, multiple spaces) to single spaces

    4. Strip leading and trailing whitespace

    5. Strip surrounding quotes (single or double) from the entire report

    6. Strip leading and trailing whitespace again (to remove any whitespace
       that was inside the surrounding quotes)

    7. Check for remaining replacement characters (�) and warn if present

    8. Verify no empty dream reports remain

    The ftfy library handles most text normalization with a single config.
    See https://ftfy.readthedocs.io for details on each configuration option.

    **Note that dream reports loaded via krank may look slightly different than
    those downloaded directly from source archives due to this normalization.**
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"df must be a pandas DataFrame, got {type(df).__name__}"
        )
    if not isinstance(text_column, str):
        raise TypeError(
            f"text_column must be a string, got {type(text_column).__name__}"
        )
    if text_column not in df.columns:
        raise ValueError(
            f"Column '{text_column}' not found in DataFrame. "
            f"Available columns: {', '.join(df.columns)}"
        )
    df = df.copy()

    # Apply ftfy text fixing using module-level config
    df[text_column] = df[text_column].apply(
        lambda text: ftfy.fix_text(text, _FTFY_CONFIG)
    )

    # Replace ellipsis character with three dots
    # (ftfy preserves ellipsis, but we want consistent three-dot representation)
    df[text_column] = df[text_column].str.replace("\u2026", "...", regex=False)

    # Collapse whitespace (newlines, tabs, multiple spaces) to single space
    df[text_column] = df[text_column].str.replace(r"\s+", " ", regex=True)

    # Strip leading/trailing whitespace
    df[text_column] = df[text_column].str.strip()

    # Strip surrounding quotes (both single and double)
    # Only strip if the entire text is quoted (starts and ends with matching quotes)
    # Using regex for vectorized operation: match quoted strings and capture inner content
    df[text_column] = df[text_column].str.replace(r'^(["\'])(.+)\1$', r"\2", regex=True)

    # Strip leading/trailing whitespace again
    # This handles whitespace that was inside the surrounding quotes
    df[text_column] = df[text_column].str.strip()

    # Check for remaining replacement characters (�)
    # These indicate unrecoverable text corruption that ftfy couldn't fix
    replacement_char_mask = df[text_column].str.contains("\ufffd", na=False)
    replacement_count = replacement_char_mask.sum()
    if replacement_count > 0:
        warnings.warn(
            f"Found {replacement_count} dream report(s) containing replacement "
            f"characters (�) after normalization. These indicate unrecoverable "
            f"text corruption in the source data.",
            UserWarning,
            stacklevel=2,
        )

    # Verify no empty dream reports
    empty_count = (df[text_column] == "").sum()
    if empty_count > 0:
        raise ValueError(
            f"Found {empty_count} empty dream report(s) after normalization. "
            "Dream reports cannot be empty strings."
        )

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
    """

    def __init__(self, name: str, metadata: dict, path: Path):
        if not isinstance(name, str):
            raise TypeError(f"Corpus name must be a string, got {type(name).__name__}")
        if not name:
            raise ValueError("Corpus name cannot be empty")
        if not isinstance(metadata, dict):
            raise TypeError(
                f"Metadata must be a dictionary, got {type(metadata).__name__}"
            )
        if not isinstance(path, Path):
            raise TypeError(
                f"Path must be a pathlib.Path object, got {type(path).__name__}"
            )
        self.name = name
        self.metadata = metadata
        self._path = path
        self._df = None
        # self._df_core = None

    def __repr__(self) -> str:
        return f"Corpus('{self.name}')"

    def __str__(self) -> str:
        """Return descriptive string representation of corpus metadata.

        Returns
        -------
        str
            Multi-line string containing corpus metadata from the metadata dict.
            Does not load reports or authors data.
        """
        lines = [f"Corpus: {self.name}"]

        # Add required metadata fields
        lines.append(f"  Title: {self.metadata['title']}")
        lines.append(f"  Description: {self.metadata['description']}")
        lines.append(f"  Version: {self.metadata['version']}")

        # Add optional citations field
        citations = self.metadata.get("citations")
        if citations:
            # Show all citations with only authors and year, separated by semicolons
            short_citations = [_extract_author_year(cit) for cit in citations]
            citation_str = "; ".join(short_citations)
            lines.append(f"  Citations: {citation_str}")

        return "\n".join(lines)

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
        author_columns = self.metadata["author_columns"]
        reports_df = df.drop(columns=author_columns).copy()
        # Validate the reports dataframe with pandera
        reports_df = ReportsSchema.validate(reports_df)
        return reports_df

    @property
    def authors(self) -> pd.DataFrame:
        """Deduplicated author-level metadata. Tidy format.

        Returns
        -------
        pd.DataFrame
            DataFrame containing unique author IDs and their associated metadata.
            Each author appears only once.
        """
        df = self._load()
        author_columns = self.metadata["author_columns"]
        cols = ["author"] + author_columns
        authors_df = df[cols].drop_duplicates().reset_index(drop=True)
        # Validate the authors dataframe with pandera
        authors_df = AuthorsSchema.validate(authors_df)
        return authors_df

    @property
    def n_reports(self) -> int:
        """Number of reports in the corpus.

        Returns
        -------
        int
            Total number of dream reports in the corpus.

        Notes
        -----
        This property loads the reports data if not already loaded.
        """
        return len(self.reports)

    @property
    def n_authors(self) -> int:
        """Number of unique authors in the corpus.

        Returns
        -------
        int
            Total number of unique authors in the corpus.

        Notes
        -----
        This property loads the authors data if not already loaded.
        """
        return len(self.authors)

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
            column_map = self.metadata["column_map"]
            column_map_reversed = {v: k for k, v in column_map.items()}
            df = df.rename(columns=column_map_reversed)
            df = _normalize_text(df, "report")
            self._df = df
        return self._df
