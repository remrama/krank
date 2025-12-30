"""Tests for krank._schemas module."""

import pandas as pd
import pytest
from pandera.errors import SchemaError

from krank._schemas import AggregateReportsSchema, AuthorsSchema, ReportsSchema


class TestReportsSchema:
    """Tests for ReportsSchema validation."""

    def test_valid_reports_dataframe(self):
        """Test that a valid reports dataframe passes validation."""
        df = pd.DataFrame(
            {
                "author": ["A1", "A2", "A3"],
                "report": ["Dream 1", "Dream 2", "Dream 3"],
            }
        )
        result = ReportsSchema.validate(df)
        assert result is not None
        assert len(result) == 3

    def test_reports_with_additional_columns(self):
        """Test that reports dataframe can have additional columns."""
        df = pd.DataFrame(
            {
                "author": ["A1", "A2"],
                "report": ["Dream 1", "Dream 2"],
                "time": ["07:17:27", "02:07:02"],
                "stage": ["REM", "N2"],
            }
        )
        result = ReportsSchema.validate(df)
        assert result is not None
        assert "time" in result.columns
        assert "stage" in result.columns

    def test_reports_missing_author_column(self):
        """Test that reports dataframe without author column fails validation."""
        df = pd.DataFrame({"report": ["Dream 1", "Dream 2"]})
        with pytest.raises(SchemaError):
            ReportsSchema.validate(df)

    def test_reports_missing_report_column(self):
        """Test that reports dataframe without report column fails validation."""
        df = pd.DataFrame({"author": ["A1", "A2"]})
        with pytest.raises(SchemaError):
            ReportsSchema.validate(df)

    def test_reports_with_null_author(self):
        """Test that reports dataframe with null author fails validation."""
        df = pd.DataFrame(
            {
                "author": ["A1", None, "A3"],
                "report": ["Dream 1", "Dream 2", "Dream 3"],
            }
        )
        with pytest.raises(SchemaError):
            ReportsSchema.validate(df)

    def test_reports_with_null_report(self):
        """Test that reports dataframe with null report fails validation."""
        df = pd.DataFrame(
            {
                "author": ["A1", "A2", "A3"],
                "report": ["Dream 1", None, "Dream 3"],
            }
        )
        with pytest.raises(SchemaError):
            ReportsSchema.validate(df)

    def test_reports_coerces_types(self):
        """Test that reports dataframe coerces types as needed."""
        df = pd.DataFrame(
            {
                "author": [1, 2, 3],  # integers
                "report": ["Dream 1", "Dream 2", "Dream 3"],
            }
        )
        result = ReportsSchema.validate(df)
        assert result["author"].dtype.name == "category"  # coerced to categorical
        assert result["report"].dtype.name == "string"  # coerced to string


class TestAuthorsSchema:
    """Tests for AuthorsSchema validation."""

    def test_valid_authors_dataframe(self):
        """Test that a valid authors dataframe passes validation."""
        df = pd.DataFrame(
            {
                "author": ["A1", "A2", "A3"],
                "age": [25, 30, 35],
                "sex": ["M", "F", "M"],
            }
        )
        result = AuthorsSchema.validate(df)
        assert result is not None
        assert len(result) == 3

    def test_authors_with_minimal_columns(self):
        """Test that authors dataframe can have just author column."""
        df = pd.DataFrame({"author": ["A1", "A2", "A3"]})
        result = AuthorsSchema.validate(df)
        assert result is not None
        assert list(result.columns) == ["author"]

    def test_authors_missing_author_column(self):
        """Test that authors dataframe without author column fails validation."""
        df = pd.DataFrame({"age": [25, 30, 35], "sex": ["M", "F", "M"]})
        with pytest.raises(SchemaError):
            AuthorsSchema.validate(df)

    def test_authors_with_null_author(self):
        """Test that authors dataframe with null author fails validation."""
        df = pd.DataFrame({"author": ["A1", None, "A3"]})
        with pytest.raises(SchemaError):
            AuthorsSchema.validate(df)

    def test_authors_with_duplicate_author(self):
        """Test that authors dataframe with duplicate author fails validation."""
        df = pd.DataFrame(
            {
                "author": ["A1", "A2", "A1"],  # duplicate A1
                "age": [25, 30, 25],
            }
        )
        with pytest.raises(SchemaError):
            AuthorsSchema.validate(df)

    def test_authors_coerces_types(self):
        """Test that authors dataframe coerces types as needed."""
        df = pd.DataFrame({"author": [1, 2, 3]})  # integers
        result = AuthorsSchema.validate(df)
        assert result["author"].dtype.name == "category"  # coerced to categorical

    def test_authors_sex_categorical(self):
        """Test that sex column is coerced to categorical when present."""
        df = pd.DataFrame(
            {
                "author": ["A1", "A2", "A3"],
                "sex": ["M", "F", "M"],
            }
        )
        result = AuthorsSchema.validate(df)
        assert result["sex"].dtype.name == "category"


class TestAggregateReportsSchema:
    """Tests for AggregateReportsSchema validation."""

    def test_valid_aggregate_dataframe(self):
        """Test that a valid aggregate reports dataframe passes validation."""
        df = pd.DataFrame(
            {
                "corpus": ["corpus1-v1", "corpus1-v1", "corpus2-v1"],
                "author": ["A1", "A2", "B1"],
                "report": ["Dream 1", "Dream 2", "Dream 3"],
            }
        )
        result = AggregateReportsSchema.validate(df)
        assert result is not None
        assert len(result) == 3

    def test_aggregate_missing_corpus_column(self):
        """Test that aggregate dataframe without corpus column fails validation."""
        df = pd.DataFrame(
            {
                "author": ["A1", "A2"],
                "report": ["Dream 1", "Dream 2"],
            }
        )
        with pytest.raises(SchemaError):
            AggregateReportsSchema.validate(df)

    def test_aggregate_missing_author_column(self):
        """Test that aggregate dataframe without author column fails validation."""
        df = pd.DataFrame(
            {
                "corpus": ["corpus1-v1", "corpus1-v1"],
                "report": ["Dream 1", "Dream 2"],
            }
        )
        with pytest.raises(SchemaError):
            AggregateReportsSchema.validate(df)

    def test_aggregate_missing_report_column(self):
        """Test that aggregate dataframe without report column fails validation."""
        df = pd.DataFrame(
            {
                "corpus": ["corpus1-v1", "corpus1-v1"],
                "author": ["A1", "A2"],
            }
        )
        with pytest.raises(SchemaError):
            AggregateReportsSchema.validate(df)

    def test_aggregate_with_extra_columns(self):
        """Test that aggregate dataframe with extra columns fails validation."""
        df = pd.DataFrame(
            {
                "corpus": ["corpus1-v1", "corpus1-v1"],
                "author": ["A1", "A2"],
                "report": ["Dream 1", "Dream 2"],
                "extra_column": ["value1", "value2"],
            }
        )
        with pytest.raises(SchemaError):
            AggregateReportsSchema.validate(df)

    def test_aggregate_with_null_corpus(self):
        """Test that aggregate dataframe with null corpus fails validation."""
        df = pd.DataFrame(
            {
                "corpus": [None, "corpus1-v1"],
                "author": ["A1", "A2"],
                "report": ["Dream 1", "Dream 2"],
            }
        )
        with pytest.raises(SchemaError):
            AggregateReportsSchema.validate(df)

    def test_aggregate_with_null_author(self):
        """Test that aggregate dataframe with null author fails validation."""
        df = pd.DataFrame(
            {
                "corpus": ["corpus1-v1", "corpus1-v1"],
                "author": ["A1", None],
                "report": ["Dream 1", "Dream 2"],
            }
        )
        with pytest.raises(SchemaError):
            AggregateReportsSchema.validate(df)

    def test_aggregate_with_null_report(self):
        """Test that aggregate dataframe with null report fails validation."""
        df = pd.DataFrame(
            {
                "corpus": ["corpus1-v1", "corpus1-v1"],
                "author": ["A1", "A2"],
                "report": ["Dream 1", None],
            }
        )
        with pytest.raises(SchemaError):
            AggregateReportsSchema.validate(df)

    def test_aggregate_coerces_types(self):
        """Test that aggregate dataframe coerces types as needed."""
        df = pd.DataFrame(
            {
                "corpus": [1, 2],  # integers
                "author": [100, 200],  # integers
                "report": ["Dream 1", "Dream 2"],
            }
        )
        result = AggregateReportsSchema.validate(df)
        assert result["corpus"].dtype == object  # coerced to string
        assert result["author"].dtype == object  # coerced to string
