"""Corpus data container and text normalization utilities.

This module defines the Corpus class for managing loaded dream report corpora,
including lazy-loading of data, text normalization, and separation of report
and author metadata.
"""

from pathlib import Path

import ftfy
import pandas as pd
from ftfy import TextFixerConfig

from ._schemas import AuthorsSchema, ReportsSchema

__all__ = ["Corpus"]


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
    ValueError
        If any dream reports are empty strings after normalization.

    Notes
    -----
    Normalization steps applied in order:
    
    1. Apply ftfy text fixing with explicit configuration:
       - Fix mojibake (text decoded in wrong encoding)
       - Replace curly quotes with straight quotes
       - Apply NFC unicode normalization
       - Handle replacement characters (�) in lossy sequences
       - Fix various encoding issues and control characters
    
    2. Replace ellipsis character (…) with three dots (...)
    
    3. Collapse all whitespace (newlines, tabs, multiple spaces) to single spaces
    
    4. Strip leading and trailing whitespace
    
    5. Strip surrounding quotes (single or double) from the entire report
    
    6. Verify no empty dream reports remain
    
    The ftfy library handles most text normalization with a single config.
    See https://ftfy.readthedocs.io for details on each configuration option.
    
    Note that dream reports loaded via krank may look slightly different than
    those downloaded directly from source archives due to this normalization.
    """
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
    df[text_column] = df[text_column].str.replace(
        r'^(["\'])(.+)\1$', r'\2', regex=True
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
        self.name = name
        self.metadata = metadata
        self._path = path
        self._df = None
        # self._df_core = None

    def __repr__(self) -> str:
        return f"Corpus('{self.name}')"

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
        authors_df = df[cols].drop_duplicates().reset_index(drop=True)
        # Validate the authors dataframe with pandera
        authors_df = AuthorsSchema.validate(authors_df)
        return authors_df

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
