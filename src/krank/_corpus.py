from pathlib import Path

import pandas as pd


__all__ = ["Corpus"]


def _normalize_text(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """Apply universal text normalization to dream text column."""
    df = df.copy()
    
    # Collapse whitespace (newlines, tabs, multiple spaces) to single space
    df[text_column] = df[text_column].str.replace(r"\s+", " ", regex=True)
    
    # Strip leading/trailing whitespace
    df[text_column] = df[text_column].str.strip()
    
    return df


class Corpus:
    """Container for a loaded corpus with metadata."""
    
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
        """Local path to cached CSV file."""
        return self._path
    
    @property
    def reports(self) -> pd.DataFrame:
        """
        Report-level data (no author metadata columns).
        Lazy-loaded. Tidy format.
        
        Notes
        -----
        If you need the raw CSV without normalization or column mapping,
        access it via the .path attribute.
        
        If you want to load the data without accessing it,
        use _load_and_normalize() directly to load the dataframe in place.
        """
        df = self._load()
        author_fields = self.metadata.get("author_fields", [])
        return df.drop(columns=author_fields).copy()
    
    @property
    def authors(self) -> pd.DataFrame:
        """Deduplicated author-level metadata. Tidy format."""
        assert "author_fields" in self.metadata, "Corpus metadata missing 'author_fields'"
        df = self._load()
        author_fields = self.metadata.get("author_fields", [])
        cols = ["author"] + author_fields
        return df[cols].drop_duplicates().reset_index(drop=True)


    def _load(self) -> pd.DataFrame:
        """Load and normalize full dataframe. Called once, cached.
    
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
