"""Tests for krank main module."""

from pathlib import Path
from unittest.mock import patch

import pytest

import krank


def test_info(mock_registry, capsys):
    """Test info function prints corpus metadata."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        with patch("krank._registry.get_entry") as mock_get_entry:
            mock_get_entry.return_value = {
                "title": "Test Corpus",
                "description": "A test corpus",
                "n_reports": 100,
                "citation": "Test citation",
                "version": "1",
                "collection": "test_collection",
            }

            krank.info("test_corpus")
            captured = capsys.readouterr()

            assert "Corpus: test_corpus" in captured.out
            assert "Title: Test Corpus" in captured.out
            assert "Description: A test corpus" in captured.out
            assert "Reports: 100" in captured.out
            assert "Citation: Test citation" in captured.out
            assert "Version: 1" in captured.out
            assert "Collection: test_collection" in captured.out


def test_info_missing_fields(mock_registry, capsys):
    """Test info function with missing metadata fields."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        with patch("krank._registry.get_entry") as mock_get_entry:
            mock_get_entry.return_value = {}

            krank.info("test_corpus")
            captured = capsys.readouterr()

            # Should show N/A for missing fields
            assert "Title: N/A" in captured.out
            assert "Description: N/A" in captured.out


def test_list_collections(mock_registry):
    """Test list_collections function."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        collections = krank.list_collections()

        assert isinstance(collections, list)
        assert "test_collection" in collections
        assert collections == sorted(collections)


def test_list_corpora(mock_registry):
    """Test list_corpora function."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        corpora = krank.list_corpora()

        assert isinstance(corpora, list)
        assert "test_corpus" in corpora
        assert corpora == sorted(corpora)


def test_list_versions(mock_registry):
    """Test list_versions function."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        versions = krank.list_versions("test_corpus")

        assert isinstance(versions, list)
        assert "1" in versions
        assert "2" in versions
        assert versions == sorted(versions)


def test_list_versions_invalid_corpus(mock_registry):
    """Test list_versions with invalid corpus name."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        with pytest.raises(KeyError, match="Corpus 'nonexistent' not found"):
            krank.list_versions("nonexistent")


def test_load(mock_registry, mock_corpus_csv):
    """Test load function."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        with patch("krank._registry.get_entry") as mock_get_entry:
            with patch("krank._registry.fetch_corpus", return_value=mock_corpus_csv):
                mock_get_entry.return_value = {
                    "title": "Test Corpus",
                    "column_map": {
                        "report": "Report Text",
                        "author": "Author ID",
                    },
                    "author_columns": ["age", "sex"],
                }

                corpus = krank.load("test_corpus")

                assert isinstance(corpus, krank._corpus.Corpus)
                assert corpus.name == "test_corpus"


def test_load_with_version(mock_registry, mock_corpus_csv):
    """Test load function with specific version."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        with patch("krank._registry.get_entry") as mock_get_entry:
            with patch("krank._registry.fetch_corpus", return_value=mock_corpus_csv):
                mock_get_entry.return_value = {
                    "title": "Test Corpus",
                    "version": "2",
                    "column_map": {
                        "report": "Report Text",
                        "author": "Author ID",
                    },
                    "author_columns": [],
                }

                corpus = krank.load("test_corpus", version="2")

                assert corpus.metadata["version"] == "2"
                mock_get_entry.assert_called_with("test_corpus", version="2")


def test_version_constant():
    """Test that __version__ is defined."""
    assert hasattr(krank, "__version__")
    assert isinstance(krank.__version__, str)


def test_all_exports():
    """Test that __all__ contains expected functions."""
    expected = ["info", "list_collections", "list_corpora", "list_versions", "load"]
    assert krank.__all__ == expected
