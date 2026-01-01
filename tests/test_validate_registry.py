"""Tests for registry validation script."""

# Import validation functions from the script
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from validate_registry import (
    validate_alphabetical_order,
    validate_collection_references,
    validate_schema,
)


@pytest.fixture
def valid_registry():
    """Create a valid registry structure for testing."""
    return {
        "collections": {
            "test_collection": {
                "title": "Test Collection",
                "brief_description": "A test collection",
                "long_description": "A test collection with detailed information.",
                "url": "https://example.com",
                "corpora": ["test_corpus"],
            }
        },
        "corpora": {
            "test_corpus": {
                "title": "Test Corpus",
                "brief_description": "A test corpus",
                "long_description": "A test corpus with detailed information.",
                "citations": ["Test citation"],
                "environment": "lab",
                "probe": "serial awakening",
                "includes_norecall": True,
                "column_map": {
                    "report": "Report Text",
                    "author": "Author ID",
                },
                "author_columns": ["age", "sex"],
                "latest": "1",
                "versions": {
                    "1": {
                        "download_url": "https://example.com/test.csv",
                        "hash": "md5:5d41402abc4b2a76b9719d911017c592",
                        "doi": "10.1234/test",
                    }
                },
            }
        },
    }


def test_validate_schema_valid(valid_registry):
    """Test schema validation with valid registry."""
    is_valid, errors = validate_schema(valid_registry)
    assert is_valid
    assert len(errors) == 0


def test_validate_schema_missing_required_field(valid_registry):
    """Test schema validation with missing required field."""
    # Remove required field
    del valid_registry["corpora"]["test_corpus"]["title"]
    is_valid, errors = validate_schema(valid_registry)
    assert not is_valid
    assert len(errors) > 0
    assert any("title" in error.lower() for error in errors)


def test_validate_schema_invalid_column_map(valid_registry):
    """Test schema validation with invalid column_map."""
    # Remove required key from column_map
    valid_registry["corpora"]["test_corpus"]["column_map"] = {"report": "Report Text"}
    is_valid, errors = validate_schema(valid_registry)
    assert not is_valid
    assert len(errors) > 0


def test_validate_schema_invalid_hash_format(valid_registry):
    """Test schema validation with invalid hash format."""
    valid_registry["corpora"]["test_corpus"]["versions"]["1"]["hash"] = "invalid_hash"
    is_valid, errors = validate_schema(valid_registry)
    assert not is_valid
    assert len(errors) > 0


def test_validate_schema_invalid_url(valid_registry):
    """Test schema validation with invalid URL."""
    valid_registry["collections"]["test_collection"]["url"] = "not-a-url"
    is_valid, errors = validate_schema(valid_registry)
    assert not is_valid
    assert len(errors) > 0


def test_validate_schema_latest_not_in_versions(valid_registry):
    """Test schema validation when latest version doesn't exist in versions."""
    valid_registry["corpora"]["test_corpus"]["latest"] = "999"
    is_valid, errors = validate_schema(valid_registry)
    assert not is_valid
    assert len(errors) > 0


def test_validate_alphabetical_order_valid():
    """Test alphabetical order validation with valid order."""
    items = {"aaa": {}, "bbb": {}, "ccc": {}}
    is_valid, errors = validate_alphabetical_order(items, "test")
    assert is_valid
    assert len(errors) == 0


def test_validate_alphabetical_order_invalid():
    """Test alphabetical order validation with invalid order."""
    items = {"ccc": {}, "aaa": {}, "bbb": {}}
    is_valid, errors = validate_alphabetical_order(items, "test")
    assert not is_valid
    assert len(errors) > 0


def test_validate_collection_references_valid(valid_registry):
    """Test collection reference validation with valid references."""
    is_valid, errors = validate_collection_references(valid_registry)
    assert is_valid
    assert len(errors) == 0


def test_validate_collection_references_invalid(valid_registry):
    """Test collection reference validation with invalid references."""
    valid_registry["collections"]["test_collection"]["corpora"].append(
        "nonexistent_corpus"
    )
    is_valid, errors = validate_collection_references(valid_registry)
    assert not is_valid
    assert len(errors) > 0
    assert any("nonexistent_corpus" in error for error in errors)


def test_actual_registry_is_valid():
    """Test that the actual registry.yaml file is valid."""
    registry_path = (
        Path(__file__).parent.parent / "src" / "krank" / "data" / "registry.yaml"
    )
    with open(registry_path, encoding="utf-8") as f:
        registry_data = yaml.safe_load(f)

    # Schema validation
    is_valid, errors = validate_schema(registry_data)
    assert is_valid, f"Schema validation failed: {errors}"

    # Alphabetical order for collections
    collections = registry_data.get("collections", {})
    is_valid, errors = validate_alphabetical_order(collections, "Collections")
    assert is_valid, f"Collections not in alphabetical order: {errors}"

    # Alphabetical order for corpora
    corpora = registry_data.get("corpora", {})
    is_valid, errors = validate_alphabetical_order(corpora, "Corpora")
    assert is_valid, f"Corpora not in alphabetical order: {errors}"

    # Collection references
    is_valid, errors = validate_collection_references(registry_data)
    assert is_valid, f"Invalid collection references: {errors}"
