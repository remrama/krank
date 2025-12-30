"""Tests for krank._corpus module."""

from pathlib import Path

import pandas as pd
import pytest

from krank import _corpus


def test_extract_author_year():
    """Test citation author and year extraction."""
    # Standard citation format
    assert "Smith, 2020" in _corpus._extract_author_year(
        "Smith, J. (2020). Title. Journal, 1(1), 1-10."
    )

    # Multiple authors with ampersand
    result = _corpus._extract_author_year(
        "Smith, J., & Doe, A. (2024). Title. Journal, 1(1), 1-10."
    )
    assert "et al." in result
    assert "2024" in result

    # Year after comma instead of parentheses
    result = _corpus._extract_author_year("Brown, B., 2023. Title. Journal.")
    assert "Brown" in result
    assert "2023" in result

    # No year - should return truncated citation
    result = _corpus._extract_author_year("Some citation without year")
    assert "citation" in result.lower()


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


def test_normalize_text_curly_quotes():
    """Test that curly quotes are converted to straight quotes."""
    df = pd.DataFrame(
        {
            "report": [
                "\u201cDouble curly quotes\u201d",  # Surrounding - will be stripped
                "\u2018Single curly quotes\u2019",  # Surrounding - will be stripped
                "Mixed \u201cleft\u201d and \u2018right\u2019 quotes",  # Internal - preserved
                "Text with \u201cquoted phrase\u201d inside",  # Internal - preserved
            ]
        }
    )

    result = _corpus._normalize_text(df, "report")

    expected = [
        "Double curly quotes",  # Surrounding quotes stripped
        "Single curly quotes",  # Surrounding quotes stripped
        "Mixed \"left\" and 'right' quotes",  # Internal quotes preserved and converted
        'Text with "quoted phrase" inside',  # Internal quotes preserved and converted
    ]

    assert result["report"].tolist() == expected


def test_normalize_text_ellipsis():
    """Test that ellipsis character is replaced with three dots."""
    df = pd.DataFrame(
        {
            "report": [
                "Text with\u2026 ellipsis",
                "Multiple\u2026 ellipses\u2026 here",
                "No ellipsis here",
            ]
        }
    )

    result = _corpus._normalize_text(df, "report")

    expected = [
        "Text with... ellipsis",
        "Multiple... ellipses... here",
        "No ellipsis here",
    ]

    assert result["report"].tolist() == expected


def test_normalize_text_surrounding_quotes():
    """Test that surrounding quotes are stripped."""
    df = pd.DataFrame(
        {
            "report": [
                '"Entire text in double quotes"',
                "'Entire text in single quotes'",
                'Text with "inner quotes" preserved',
                "No quotes",
                '"',  # Single quote char
            ]
        }
    )

    result = _corpus._normalize_text(df, "report")

    expected = [
        "Entire text in double quotes",
        "Entire text in single quotes",
        'Text with "inner quotes" preserved',
        "No quotes",
        '"',  # Single char not stripped
    ]

    assert result["report"].tolist() == expected


def test_normalize_text_quotes_with_whitespace():
    """Test that whitespace inside quotes is properly handled.

    This tests the specific case mentioned in PR feedback where whitespace
    within quotes should be removed after stripping the quotes.
    """
    df = pd.DataFrame(
        {
            "report": [
                '"  text with internal spaces  "',  # Whitespace inside quotes
                '  "text with external spaces"  ',  # Whitespace outside quotes
                '  "  text with both  "  ',  # Whitespace on both sides
                '"no extra spaces"',  # No extra whitespace
            ]
        }
    )

    result = _corpus._normalize_text(df, "report")

    expected = [
        "text with internal spaces",  # Internal whitespace stripped
        "text with external spaces",  # External whitespace stripped
        "text with both",  # Both types stripped
        "no extra spaces",  # Unchanged except quotes removed
    ]

    assert result["report"].tolist() == expected


def test_normalize_text_unicode_normalization():
    """Test that NFC unicode normalization is applied."""
    # Create text with decomposed unicode (NFD form)
    # café with decomposed é (e + combining acute accent)
    nfd_text = "cafe\u0301"  # NFD form
    nfc_text = "café"  # NFC form

    df = pd.DataFrame({"report": [nfd_text]})

    result = _corpus._normalize_text(df, "report")

    # Should be normalized to NFC
    assert result["report"].iloc[0] == nfc_text


def test_normalize_text_mojibake():
    """Test that mojibake is fixed."""
    # Example of mojibake: UTF-8 text incorrectly decoded as Latin-1
    df = pd.DataFrame(
        {
            "report": [
                "Ã©",  # Should be é
                "test text",  # Normal text should be unchanged
            ]
        }
    )

    result = _corpus._normalize_text(df, "report")

    # Mojibake should be fixed
    assert result["report"].iloc[0] == "é"
    assert result["report"].iloc[1] == "test text"


def test_normalize_text_replacement_character():
    """Test handling of replacement character (�) with warning."""
    df = pd.DataFrame(
        {
            "report": [
                "Text with replacement \ufffd character",
                "Normal text",
            ]
        }
    )

    # Should emit a warning about remaining replacement characters
    with pytest.warns(UserWarning, match="replacement characters"):
        result = _corpus._normalize_text(df, "report")

    # The replacement character remains (ftfy can't fix it)
    assert "\ufffd" in result["report"].iloc[0]
    assert isinstance(result["report"].iloc[1], str)


def test_normalize_text_empty_reports_error():
    """Test that empty reports after normalization raise an error."""
    df = pd.DataFrame(
        {
            "report": [
                "Valid text",
                "   ",  # Only whitespace - becomes empty after strip
                "Another valid text",
            ]
        }
    )

    with pytest.raises(ValueError, match="empty dream report"):
        _corpus._normalize_text(df, "report")


def test_normalize_text_empty_reports_initially_empty():
    """Test that initially empty reports raise an error."""
    df = pd.DataFrame(
        {
            "report": [
                "Valid text",
                "",  # Empty string
            ]
        }
    )

    with pytest.raises(ValueError, match="empty dream report"):
        _corpus._normalize_text(df, "report")


def test_normalize_text_combined_issues():
    """Test normalization with multiple issues in single text."""
    df = pd.DataFrame(
        {
            "report": [
                '  "\u201cMixed\u201d issues\u2026  with   spaces\nand newlines"  ',
            ]
        }
    )

    result = _corpus._normalize_text(df, "report")

    # Should have:
    # - Stripped outer whitespace
    # - Stripped surrounding quotes (the outer ")
    # - Converted curly quotes to straight
    # - Replaced ellipsis with ...
    # - Collapsed whitespace
    expected = '"Mixed" issues... with spaces and newlines'

    assert result["report"].iloc[0] == expected


def test_corpus_init():
    """Test Corpus initialization."""
    metadata = {"title": "Test"}
    path = Path("/tmp/test.csv")

    corpus = _corpus.Corpus("test", metadata, path)

    assert corpus.name == "test"
    assert corpus.metadata == metadata
    assert corpus._path == path
    assert corpus._df is None


def test_corpus_repr():
    """Test Corpus string representation."""
    metadata = {"title": "Test"}
    corpus = _corpus.Corpus("test", metadata, Path("/tmp/test.csv"))

    assert repr(corpus) == "Corpus('test')"


def test_corpus_str():
    """Test Corpus __str__ method shows descriptive metadata."""
    metadata = {
        "title": "Test Corpus",
        "description": "A test corpus for unit testing",
        "version": "1",
        "doi": "10.5281/zenodo.12345",
        "citations": [
            "Smith, J., & Doe, A. (2024). Test dreams. Journal of Dreams, 1(1), 1-10.",
            "Brown, B. (2023). More test dreams. Sleep Research, 2(2), 20-30.",
        ],
    }
    corpus = _corpus.Corpus("test", metadata, Path("/tmp/test.csv"))

    result = str(corpus)

    assert "Corpus: test" in result
    assert "Title: Test Corpus" in result
    assert "Description: A test corpus for unit testing" in result
    assert "Version: 1" in result
    assert "DOI: https://doi.org/10.5281/zenodo.12345" in result
    assert "Citations:" in result
    assert "Smith" in result
    assert "2024" in result
    assert "Brown" in result
    assert "2023" in result
    assert ";" in result  # Citations should be separated by semicolons


def test_corpus_str_missing_fields():
    """Test Corpus __str__ with missing metadata fields."""
    metadata = {}
    corpus = _corpus.Corpus("test", metadata, Path("/tmp/test.csv"))

    result = str(corpus)

    assert "Corpus: test" in result
    assert "Title: N/A" in result
    assert "Description: N/A" in result
    assert "Version: N/A" in result
    assert "DOI: N/A" in result
    # Citations is optional, so it shouldn't show N/A


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
    _ = corpus.reports
    # Second access should use cached data
    _ = corpus.reports

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


def test_corpus_n_reports(mock_corpus_csv):
    """Test n_reports property returns correct count."""
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

    assert corpus.n_reports == 3


def test_corpus_n_authors(mock_corpus_csv):
    """Test n_authors property returns correct count."""
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

    # Should be 2 unique authors (A1 and A2)
    assert corpus.n_authors == 2
