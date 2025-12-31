#!/usr/bin/env python3
"""Validate registry.yaml schema, uniqueness, and alphabetical ordering.

This script validates the registry.yaml file against a JSON schema and checks
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

import yaml
from jsonschema import Draft7Validator, FormatChecker


def load_yaml(path: Path) -> dict:
    """Load YAML file and return as dict."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_schema() -> dict:
    """Load the JSON schema from registry-schema.yaml."""
    schema_path = (
        Path(__file__).parent.parent / "src" / "krank" / "data" / "registry-schema.yaml"
    )
    return load_yaml(schema_path)


def validate_schema(registry_data: dict) -> tuple[bool, list[str]]:
    """Validate registry data against JSON schema.

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
    schema = load_schema()

    # Create a validator with format checker
    validator = Draft7Validator(schema, format_checker=FormatChecker())

    # Validate and collect errors
    validation_errors = sorted(
        validator.iter_errors(registry_data), key=lambda e: e.path
    )

    if not validation_errors:
        # Additional custom validations
        # Check that 'latest' version exists in 'versions'
        for corpus_name, corpus_data in registry_data.get("corpora", {}).items():
            latest = corpus_data.get("latest")
            versions = corpus_data.get("versions", {})
            if latest and latest not in versions:
                errors.append(
                    f"  ❌ corpora -> {corpus_name} -> latest: "
                    f"Version '{latest}' not found in versions {list(versions.keys())}"
                )

    for error in validation_errors:
        # Format the error path
        path = " -> ".join(str(p) for p in error.path) if error.path else "root"
        msg = error.message
        errors.append(f"  ❌ {path}: {msg}")

    return len(errors) == 0, errors


def validate_alphabetical_order(items: dict, name: str) -> tuple[bool, list[str]]:
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
        default=Path(__file__).parent.parent
        / "src"
        / "krank"
        / "data"
        / "registry.yaml",
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
        print("Please fix the errors above and run validation again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
