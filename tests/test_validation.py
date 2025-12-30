"""Tests for input validation and error messages."""

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

import krank
from krank import _corpus


class TestInfoValidation:
    """Test validation for the info function."""

    def test_info_with_non_string_name(self):
        """Test info raises TypeError for non-string name."""
        with pytest.raises(TypeError, match="Corpus name must be a string"):
            krank.info(123)

    def test_info_with_empty_string_name(self):
        """Test info raises ValueError for empty string name."""
        with pytest.raises(ValueError, match="Corpus name cannot be empty"):
            krank.info("")

    def test_info_error_message_includes_help(self):
        """Test error message includes helpful hint about list_corpora."""
        with pytest.raises(TypeError, match="list_corpora"):
            krank.info(None)


class TestListVersionsValidation:
    """Test validation for the list_versions function."""

    def test_list_versions_with_non_string_name(self):
        """Test list_versions raises TypeError for non-string name."""
        with pytest.raises(TypeError, match="Corpus name must be a string"):
            krank.list_versions(123)

    def test_list_versions_with_empty_string_name(self):
        """Test list_versions raises ValueError for empty string name."""
        with pytest.raises(ValueError, match="Corpus name cannot be empty"):
            krank.list_versions("")

    def test_list_versions_error_message_includes_help(self):
        """Test error message includes helpful hint about list_corpora."""
        with pytest.raises(TypeError, match="list_corpora"):
            krank.list_versions([])


class TestLoadValidation:
    """Test validation for the load function."""

    def test_load_with_non_string_name(self):
        """Test load raises TypeError for non-string name."""
        with pytest.raises(TypeError, match="Corpus name must be a string"):
            krank.load(123)

    def test_load_with_empty_string_name(self):
        """Test load raises ValueError for empty string name."""
        with pytest.raises(ValueError, match="Corpus name cannot be empty"):
            krank.load("")

    def test_load_with_non_string_version(self):
        """Test load raises TypeError for non-string version."""
        with pytest.raises(TypeError, match="Version must be a string or None"):
            krank.load("test_corpus", version=123)

    def test_load_with_empty_string_version(self):
        """Test load raises ValueError for empty string version."""
        with pytest.raises(ValueError, match="Version cannot be an empty string"):
            krank.load("test_corpus", version="")

    def test_load_name_error_message_includes_help(self):
        """Test error message includes helpful hint about list_corpora."""
        with pytest.raises(TypeError, match="list_corpora"):
            krank.load(None)

    def test_load_version_error_message_includes_help(self, mock_registry):
        """Test error message includes helpful hint about list_versions."""
        with patch("krank._registry.load_registry", return_value=mock_registry):
            with pytest.raises(TypeError, match="list_versions"):
                krank.load("test_corpus", version=123)

    def test_load_empty_version_error_message_includes_help(self, mock_registry):
        """Test error message for empty version includes helpful hints."""
        with patch("krank._registry.load_registry", return_value=mock_registry):
            with pytest.raises(
                ValueError, match="list_versions|omit the version parameter"
            ):
                krank.load("test_corpus", version="")


class TestCorpusValidation:
    """Test validation for the Corpus class."""

    def test_corpus_with_non_string_name(self):
        """Test Corpus raises TypeError for non-string name."""
        with pytest.raises(TypeError, match="Corpus name must be a string"):
            _corpus.Corpus(123, {}, Path("/tmp/test.csv"))

    def test_corpus_with_empty_string_name(self):
        """Test Corpus raises ValueError for empty string name."""
        with pytest.raises(ValueError, match="Corpus name cannot be empty"):
            _corpus.Corpus("", {}, Path("/tmp/test.csv"))

    def test_corpus_with_non_dict_metadata(self):
        """Test Corpus raises TypeError for non-dict metadata."""
        with pytest.raises(TypeError, match="Metadata must be a dictionary"):
            _corpus.Corpus("test", "not_a_dict", Path("/tmp/test.csv"))

    def test_corpus_with_non_path_path(self):
        """Test Corpus raises TypeError for non-Path path."""
        with pytest.raises(TypeError, match="Path must be a pathlib.Path object"):
            _corpus.Corpus("test", {}, "/tmp/test.csv")


class TestNormalizeTextValidation:
    """Test validation for the _normalize_text function."""

    def test_normalize_text_with_non_dataframe(self):
        """Test _normalize_text raises TypeError for non-DataFrame."""
        with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
            _corpus._normalize_text("not_a_dataframe", "report")

    def test_normalize_text_with_non_string_column(self):
        """Test _normalize_text raises TypeError for non-string column."""
        df = pd.DataFrame({"report": ["test"]})
        with pytest.raises(TypeError, match="text_column must be a string"):
            _corpus._normalize_text(df, 123)

    def test_normalize_text_with_missing_column(self):
        """Test _normalize_text raises ValueError for missing column."""
        df = pd.DataFrame({"report": ["test"]})
        with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
            _corpus._normalize_text(df, "nonexistent")

    def test_normalize_text_error_message_lists_available_columns(self):
        """Test error message includes list of available columns."""
        df = pd.DataFrame({"report": ["test"], "author": ["A1"]})
        with pytest.raises(ValueError, match="report, author"):
            _corpus._normalize_text(df, "nonexistent")


class TestValidationErrorMessages:
    """Test that validation error messages are informative and user-friendly."""

    def test_error_messages_include_type_information(self):
        """Test that TypeError messages include the actual type received."""
        with pytest.raises(TypeError, match="got int"):
            krank.info(123)

        with pytest.raises(TypeError, match="got list"):
            krank.list_versions([])

    def test_error_messages_suggest_alternative_actions(self):
        """Test that error messages suggest what users should do instead."""
        # Should suggest using list_corpora()
        with pytest.raises(TypeError, match="Use krank.list_corpora"):
            krank.info(None)

        # Should suggest using list_versions()
        with pytest.raises(TypeError, match="Use krank.list_versions"):
            krank.load("test_corpus", version=123)

    def test_error_messages_are_specific(self):
        """Test that error messages are specific to the problem."""
        # Empty string should have a different message than wrong type
        with pytest.raises(ValueError, match="cannot be empty"):
            krank.info("")

        with pytest.raises(TypeError, match="must be a string"):
            krank.info(123)
