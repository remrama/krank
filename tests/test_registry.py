"""Tests for krank._registry module."""

from pathlib import Path
from unittest.mock import patch

import pytest

from krank import _registry


def test_load_registry():
    """Test loading registry from YAML file."""
    registry = _registry.load_registry()
    assert isinstance(registry, dict)
    assert "corpora" in registry
    assert "collections" in registry


def test_load_registry_caching():
    """Test that registry is cached after first load."""
    # Reset cache
    _registry._registry_cache = None

    # First load
    registry1 = _registry.load_registry()

    # Second load should return the same cached object
    registry2 = _registry.load_registry()

    assert registry1 is registry2


def test_get_entry_valid_corpus(mock_registry):
    """Test getting a valid corpus entry."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        entry = _registry.get_entry("test_corpus")

        assert entry["title"] == "Test Corpus"
        assert entry["version"] == "1"
        assert entry["download_url"] == "https://example.com/test.csv"
        assert entry["hash"] == "md5:abc123"
        assert "versions" not in entry
        assert "latest" not in entry


def test_get_entry_with_version(mock_registry):
    """Test getting a corpus entry with specific version."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        entry = _registry.get_entry("test_corpus", version="2")

        assert entry["version"] == "2"
        assert entry["download_url"] == "https://example.com/test_v2.csv"
        assert entry["hash"] == "md5:def456"


def test_get_entry_invalid_corpus(mock_registry):
    """Test getting a corpus that doesn't exist."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        with pytest.raises(KeyError, match="Corpus 'nonexistent' not found"):
            _registry.get_entry("nonexistent")


def test_get_entry_invalid_version(mock_registry):
    """Test getting a corpus with invalid version."""
    with patch("krank._registry.load_registry", return_value=mock_registry):
        with pytest.raises(KeyError, match="Version '99' not found"):
            _registry.get_entry("test_corpus", version="99")


def test_fetch_corpus(mock_registry, tmp_path):
    """Test fetching a corpus file."""
    mock_path = tmp_path / "test_corpus_v1.csv"
    mock_path.write_text("Report Text,Author ID\nTest,A1\n")

    with patch("krank._registry.load_registry", return_value=mock_registry):
        with patch("krank._registry.get_entry") as mock_get_entry:
            with patch("pooch.retrieve", return_value=str(mock_path)) as mock_retrieve:
                mock_get_entry.return_value = {
                    "version": "1",
                    "download_url": "https://example.com/test.csv",
                    "hash": "md5:abc123",
                }

                path = _registry.fetch_corpus("test_corpus")

                assert isinstance(path, Path)
                assert path == mock_path
                mock_retrieve.assert_called_once()
                assert (
                    mock_retrieve.call_args[1]["url"] == "https://example.com/test.csv"
                )
                assert mock_retrieve.call_args[1]["known_hash"] == "md5:abc123"
                assert mock_retrieve.call_args[1]["fname"] == "test_corpus_v1.csv"
