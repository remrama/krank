"""Tests for krank._corpus module."""

from pathlib import Path

import pandas as pd
import pytest

from krank import _corpus


def test_normalize_text():
    """Test text normalization function."""
    df = pd.DataFrame(
        {
            "report": [
                "Normal text",
                "Text  with   multiple   spaces",
                "Text\nwith\nnewlines",
                "Text\twith\ttabs",
                "  Leading and trailing  ",
                "Mixed\n  whitespace\t\t  types  ",
            ]
        }
    )

    result = _corpus._normalize_text(df, "report")

    expected = [
        "Normal text",
        "Text with multiple spaces",
        "Text with newlines",
        "Text with tabs",
        "Leading and trailing",
        "Mixed whitespace types",
    ]

    assert result["report"].tolist() == expected


def test_normalize_text_preserves_original():
    """Test that normalization doesn't modify original dataframe."""
    df = pd.DataFrame({"report": ["Text  with   spaces"]})
    original_value = df["report"].iloc[0]

    _corpus._normalize_text(df, "report")

    assert df["report"].iloc[0] == original_value


def test_corpus_init():
    """Test Corpus initialization."""
    metadata = {"title": "Test", "n_reports": 10}
    path = Path("/tmp/test.csv")

    corpus = _corpus.Corpus("test", metadata, path)

    assert corpus.name == "test"
    assert corpus.metadata == metadata
    assert corpus._path == path
    assert corpus._df is None


def test_corpus_repr():
    """Test Corpus string representation."""
    metadata = {"n_reports": 42}
    corpus = _corpus.Corpus("test", metadata, Path("/tmp/test.csv"))

    assert repr(corpus) == "Corpus('test', n_reports=42)"


def test_corpus_repr_without_n_reports():
    """Test Corpus repr when n_reports is missing."""
    corpus = _corpus.Corpus("test", {}, Path("/tmp/test.csv"))

    assert repr(corpus) == "Corpus('test', n_reports=?)"


def test_corpus_path_property():
    """Test Corpus path property."""
    path = Path("/tmp/test.csv")
    corpus = _corpus.Corpus("test", {}, path)

    assert corpus.path == path


def test_corpus_reports(mock_corpus_csv):
    """Test Corpus reports property."""
    metadata = {
        "column_map": {
            "report": "Report Text",
            "author": "Author ID",
            "age": "Age",
            "sex": "Sex",
        },
        "author_columns": ["age", "sex"],
    }

    corpus = _corpus.Corpus("test", metadata, mock_corpus_csv)
    reports = corpus.reports

    # Check that author columns are removed
    assert "age" not in reports.columns
    assert "sex" not in reports.columns
    assert "report" in reports.columns
    assert "author" in reports.columns

    # Check that text is normalized
    assert reports["report"].iloc[0] == "Dream 1"
    assert reports["report"].iloc[1] == "Dream 2 with spaces"
    assert reports["report"].iloc[2] == "Dream 3"


def test_corpus_authors(mock_corpus_csv):
    """Test Corpus authors property."""
    metadata = {
        "column_map": {
            "report": "Report Text",
            "author": "Author ID",
            "age": "Age",
            "sex": "Sex",
        },
        "author_columns": ["age", "sex"],
    }

    corpus = _corpus.Corpus("test", metadata, mock_corpus_csv)
    authors = corpus.authors

    # Check that only author columns are present
    assert list(authors.columns) == ["author", "age", "sex"]

    # Check deduplication (A1 appears twice in the CSV)
    assert len(authors) == 2
    assert set(authors["author"]) == {"A1", "A2"}


def test_corpus_authors_without_author_columns():
    """Test that authors property raises error without author_columns."""
    corpus = _corpus.Corpus("test", {}, Path("/tmp/test.csv"))

    with pytest.raises(AssertionError, match="author_columns"):
        _ = corpus.authors


def test_corpus_load_caching(mock_corpus_csv):
    """Test that dataframe is cached after first load."""
    metadata = {
        "column_map": {
            "report": "Report Text",
            "author": "Author ID",
            "age": "Age",
            "sex": "Sex",
        },
        "author_columns": ["age", "sex"],
    }

    corpus = _corpus.Corpus("test", metadata, mock_corpus_csv)

    # First access
    reports1 = corpus.reports
    # Second access should use cached data
    reports2 = corpus.reports

    # They should be different objects (copy), but same underlying cached data
    assert corpus._df is not None


def test_corpus_without_column_map(tmp_path):
    """Test Corpus with no column_map."""
    csv_path = tmp_path / "no_map.csv"
    df = pd.DataFrame({"report": ["Dream A"], "author": ["X1"]})
    df.to_csv(csv_path, index=False)

    metadata = {"author_columns": []}
    corpus = _corpus.Corpus("test", metadata, csv_path)
    reports = corpus.reports

    assert "report" in reports.columns
    assert reports["report"].iloc[0] == "Dream A"
