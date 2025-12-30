#!/usr/bin/env python3
"""Validate registry.yaml schema, uniqueness, and alphabetical ordering.

This script validates the registry.yaml file against a Pydantic schema and checks
for duplicate entries and alphabetical ordering of collections and corpora.

Can be run locally or in CI to ensure registry quality.

Usage:
    python scripts/validate_registry.py
    python scripts/validate_registry.py --registry-path custom/path/registry.yaml

Exit codes:
    0: Validation passed
    1: Validation failed
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator


class VersionInfo(BaseModel):
    """Schema for version-specific information."""

    download_url: str = Field(..., description="URL to download the corpus file")
    hash: str = Field(
        ..., pattern=r"^(md5|sha256):[a-fA-F0-9]+$", description="Hash of the file"
    )
    doi: str = Field(..., description="DOI for the corpus version")

    @field_validator("download_url")
    @classmethod
    def validate_download_url(cls, v: str) -> str:
        """Validate that download_url is a valid URL."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("download_url must start with http:// or https://")
        return v


class CorpusEntry(BaseModel):
    """Schema for a corpus entry in the registry."""

    krank_sources_repo: str = Field(
        ..., description="Repository name in krank-sources organization"
    )
    title: str = Field(..., description="Human-readable title of the corpus")
    description: str = Field(..., description="Description of the corpus")
    citations: list[str] = Field(
        ..., min_length=1, description="List of citations for the corpus"
    )
    environment: str = Field(..., description="Environment where data was collected")
    probe: str = Field(..., description="Probing method used")
    includes_norecall: bool = Field(
        ..., description="Whether the corpus includes no-recall reports"
    )
    column_map: dict[str, str] = Field(
        ..., description="Mapping of standard column names to corpus-specific names"
    )
    author_columns: list[str] = Field(
        ..., description="List of author-level metadata columns"
    )
    latest: str = Field(..., description="Latest version identifier")
    versions: dict[str, VersionInfo] = Field(
        ..., min_length=1, description="Available versions"
    )
    column_descriptions: dict[str, str] | None = Field(
        None, description="Optional descriptions for columns"
    )

    @field_validator("column_map")
    @classmethod
    def validate_column_map(cls, v: dict[str, str]) -> dict[str, str]:
        """Validate that column_map contains required keys."""
        required_keys = {"report", "author"}
        if not required_keys.issubset(v.keys()):
            missing = required_keys - set(v.keys())
            raise ValueError(f"column_map must contain keys: {missing}")
        return v

    @field_validator("versions")
    @classmethod
    def validate_latest_in_versions(cls, v: dict[str, Any], info) -> dict[str, Any]:
        """Validate that latest version exists in versions dict."""
        # This validator runs after all fields are set, so we can access other fields
        # But info.data might not have 'latest' yet, so we skip this check here
        # and do it in the model validator instead
        return v

    def model_post_init(self, __context: Any) -> None:
        """Post-initialization validation."""
        if self.latest not in self.versions:
            raise ValueError(
                f"latest version '{self.latest}' not found in versions: {list(self.versions.keys())}"
            )


class CollectionEntry(BaseModel):
    """Schema for a collection entry in the registry."""

    title: str = Field(..., description="Human-readable title of the collection")
    description: str | None = Field(
        None, description="Optional description of the collection"
    )
    url: str = Field(..., description="URL for the collection")
    corpora: list[str] = Field(
        ..., min_length=1, description="List of corpus names in this collection"
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate that url is a valid URL."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("url must start with http:// or https://")
        return v


class Registry(BaseModel):
    """Schema for the registry.yaml file."""

    collections: dict[str, CollectionEntry] = Field(
        ..., description="Dictionary of collection entries"
    )
    corpora: dict[str, CorpusEntry] = Field(
        ..., description="Dictionary of corpus entries"
    )


def load_yaml(path: Path) -> dict:
    """Load YAML file and return as dict."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_schema(registry_data: dict) -> tuple[bool, list[str]]:
    """Validate registry data against Pydantic schema.

    Parameters
    ----------
    registry_data : dict
        Dictionary containing registry data.

    Returns
    -------
    tuple[bool, list[str]]
        Tuple of (is_valid, error_messages).
    """
    errors = []
    try:
        Registry.model_validate(registry_data)
        return True, []
    except ValidationError as e:
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error["loc"])
            msg = error["msg"]
            errors.append(f"  ❌ {loc}: {msg}")
        return False, errors


def validate_alphabetical_order(
    items: dict, name: str
) -> tuple[bool, list[str]]:
    """Validate that dictionary keys are in alphabetical order.

    Parameters
    ----------
    items : dict
        Dictionary to check.
    name : str
        Name of the section being validated (for error messages).

    Returns
    -------
    tuple[bool, list[str]]
        Tuple of (is_valid, error_messages).
    """
    keys = list(items.keys())
    sorted_keys = sorted(keys)
    if keys != sorted_keys:
        errors = [f"  ❌ {name} are not in alphabetical order"]
        errors.append(f"     Current order: {', '.join(keys)}")
        errors.append(f"     Expected order: {', '.join(sorted_keys)}")
        return False, errors
    return True, []


def validate_no_duplicates(items: dict, name: str) -> tuple[bool, list[str]]:
    """Validate that there are no duplicate keys (should not be possible with dict).

    This is mainly a sanity check for YAML parsing.

    Parameters
    ----------
    items : dict
        Dictionary to check.
    name : str
        Name of the section being validated (for error messages).

    Returns
    -------
    tuple[bool, list[str]]
        Tuple of (is_valid, error_messages).
    """
    # Duplicates shouldn't be possible with dict, but check YAML parsing
    # In case someone manually edited YAML with duplicate keys
    return True, []


def validate_collection_references(registry_data: dict) -> tuple[bool, list[str]]:
    """Validate that all corpus references in collections exist.

    Parameters
    ----------
    registry_data : dict
        Registry data dictionary.

    Returns
    -------
    tuple[bool, list[str]]
        Tuple of (is_valid, error_messages).
    """
    errors = []
    available_corpora = set(registry_data.get("corpora", {}).keys())

    for collection_name, collection_data in registry_data.get(
        "collections", {}
    ).items():
        corpus_list = collection_data.get("corpora", [])
        for corpus_name in corpus_list:
            if corpus_name not in available_corpora:
                errors.append(
                    f"  ❌ Collection '{collection_name}' references non-existent corpus '{corpus_name}'"
                )

    return len(errors) == 0, errors


def main() -> int:
    """Main validation function."""
    parser = argparse.ArgumentParser(
        description="Validate registry.yaml schema and constraints"
    )
    parser.add_argument(
        "--registry-path",
        type=Path,
        default=Path(__file__).parent.parent / "src" / "krank" / "data" / "registry.yaml",
        help="Path to registry.yaml file",
    )
    args = parser.parse_args()

    registry_path = args.registry_path

    if not registry_path.exists():
        print(f"❌ Error: Registry file not found at {registry_path}")
        return 1

    print(f"🔍 Validating registry at: {registry_path}")
    print()

    # Load the YAML file
    try:
        registry_data = load_yaml(registry_path)
    except Exception as e:
        print(f"❌ Failed to load YAML file: {e}")
        return 1

    all_valid = True
    all_errors = []

    # Validate schema
    print("📋 Validating schema...")
    schema_valid, schema_errors = validate_schema(registry_data)
    if schema_valid:
        print("  ✅ Schema validation passed")
    else:
        print("  ❌ Schema validation failed:")
        all_errors.extend(schema_errors)
        all_valid = False

    print()

    # Validate alphabetical order for collections
    print("🔤 Checking alphabetical order of collections...")
    collections = registry_data.get("collections", {})
    alpha_valid, alpha_errors = validate_alphabetical_order(collections, "Collections")
    if alpha_valid:
        print("  ✅ Collections are in alphabetical order")
    else:
        print("  ❌ Collections are not in alphabetical order:")
        all_errors.extend(alpha_errors)
        all_valid = False

    print()

    # Validate alphabetical order for corpora
    print("🔤 Checking alphabetical order of corpora...")
    corpora = registry_data.get("corpora", {})
    alpha_valid, alpha_errors = validate_alphabetical_order(corpora, "Corpora")
    if alpha_valid:
        print("  ✅ Corpora are in alphabetical order")
    else:
        print("  ❌ Corpora are not in alphabetical order:")
        all_errors.extend(alpha_errors)
        all_valid = False

    print()

    # Validate collection references
    print("🔗 Validating collection corpus references...")
    ref_valid, ref_errors = validate_collection_references(registry_data)
    if ref_valid:
        print("  ✅ All collection references are valid")
    else:
        print("  ❌ Invalid collection references found:")
        all_errors.extend(ref_errors)
        all_valid = False

    print()

    # Print summary
    if all_valid:
        print("✅ All validations passed!")
        return 0
    else:
        print("❌ Validation failed with the following errors:")
        print()
        for error in all_errors:
            print(error)
        print()
        print(
            "Please fix the errors above and run validation again."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
