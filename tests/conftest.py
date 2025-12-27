"""Shared pytest fixtures for krank tests."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def mock_registry():
    """Mock registry data for testing."""
    return {
        "collections": {
            "test_collection": {
                "title": "Test Collection",
                "description": "A test collection",
                "corpora": ["test_corpus"],
            }
        },
        "corpora": {
            "test_corpus": {
                "title": "Test Corpus",
                "description": "A test corpus",
                "citations": ["Test citation"],
                "column_map": {
                    "report": "Report Text",
                    "author": "Author ID",
                    "age": "Age",
                    "sex": "Sex",
                },
                "author_columns": ["age", "sex"],
                "latest": "1",
                "versions": {
                    "1": {
                        "download_url": "https://example.com/test.csv",
                        "hash": "md5:abc123",
                    },
                    "2": {
                        "download_url": "https://example.com/test_v2.csv",
                        "hash": "md5:def456",
                    },
                },
            }
        },
    }


@pytest.fixture
def mock_corpus_csv(tmp_path):
    """Create a mock CSV file for testing corpus loading."""
    csv_path = tmp_path / "test_corpus.csv"
    df = pd.DataFrame(
        {
            "Report Text": ["Dream 1", "Dream 2  with  spaces\n\n", "  Dream 3  "],
            "Author ID": ["A1", "A2", "A1"],
            "Age": [25, 30, 25],
            "Sex": ["M", "F", "M"],
        }
    )
    df.to_csv(csv_path, index=False)
    return csv_path
