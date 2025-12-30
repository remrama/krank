"""Pandera schemas for dataframe validation.

This module defines pandera schemas for validating dataframes used throughout
the krank package to ensure data quality and consistency.
"""

from pandera.pandas import DataFrameModel, Field
from pandera.typing import Series
from typing import Optional

__all__ = ["ReportsSchema", "AuthorsSchema", "AggregateReportsSchema"]


class ReportsSchema(DataFrameModel):
    """Schema for validating corpus reports dataframes.

    Reports dataframes contain dream reports and associated report-level metadata,
    excluding author-specific columns. The exact columns will vary by corpus.
    """

    author: Series["category"] = Field(coerce=True, nullable=False, unique=False)
    report: Series["string"] = Field(coerce=True, nullable=False, unique=False)

    class Config:
        """Configuration for ReportsSchema."""

        strict = False  # Allow additional columns beyond author and report
        coerce = True  # Coerce data types if possible


class AuthorsSchema(DataFrameModel):
    """Schema for validating corpus authors dataframes.

    Authors dataframes contain unique author IDs and their associated metadata.
    Each author appears only once.
    """

    author: Series["category"] = Field(coerce=True, nullable=False, unique=True)
    age: Optional[Series[int]] = Field(coerce=True, nullable=False, unique=False)
    sex: Optional[Series["category"]] = Field(coerce=True, nullable=False, unique=False)

    class Config:
        """Configuration for AuthorsSchema."""

        strict = False  # Allow additional author metadata columns
        coerce = True  # Coerce data types if possible


class AggregateReportsSchema(DataFrameModel):
    """Schema for validating aggregate reports dataframe.

    The aggregate reports dataframe combines all corpora into a single file
    for distribution as a release artifact.
    """

    corpus: Series[str] = Field(coerce=True, nullable=False)
    author: Series[str] = Field(coerce=True, nullable=False)
    report: Series[str] = Field(coerce=True, nullable=False)

    class Config:
        """Configuration for AggregateReportsSchema."""

        strict = True  # Only allow these three columns
        coerce = True  # Coerce data types if possible
