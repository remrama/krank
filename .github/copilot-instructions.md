# Copilot Instructions for krank

## Repository Summary

**krank** is a Python library for accessing dream report corpora for sleep/dream research. It provides a unified interface to download and load standardized dream report datasets from a central registry. The library is built around pandas DataFrames and includes text normalization utilities.

- **Language**: Python 3.11+
- **Build Tool**: setuptools (PEP 517/518 compliant)
- **Package Type**: pip-installable library
- **Size**: Small (~400 lines of source code + tests)

## Build and Development Commands

### Installation (Required First Step)

Always install in development mode before running any commands:

```bash
pip install -e ".[dev]"
```

This installs all dependencies including: pandas, pooch, ftfy, pandera, PyYAML, pytest, pytest-cov, ruff, jsonschema.

### Testing

Run all tests (~1 second):

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=krank --cov-report=term-missing
```

Run a specific test file:

```bash
pytest tests/test_corpus.py
```

### Linting

Check code style:

```bash
ruff check .
```

Auto-fix linting issues:

```bash
ruff check --fix .
```

Check formatting:

```bash
ruff format --check .
```

Apply formatting:

```bash
ruff format .
```

### Registry Validation

Validate the registry.yaml file (run from repo root):

```bash
python scripts/validate_registry.py
```

This validates: schema compliance, alphabetical ordering, and collection-corpus reference integrity.

### Documentation

Install documentation dependencies:

```bash
pip install -e ".[docs]"
```

Build documentation locally:

```bash
mkdocs build --config-file docs/mkdocs.yaml
```

Serve documentation locally (with live reload):

```bash
mkdocs serve --config-file docs/mkdocs.yaml
```

The documentation site is output to `site/`.

## Project Layout

```
krank/
├── src/krank/              # Main package source
│   ├── __init__.py         # Public API (info, load, list_corpora, list_versions, list_collections)
│   ├── _corpus.py          # Corpus class and text normalization
│   ├── _registry.py        # Registry loading and corpus fetching
│   ├── _schemas.py         # Pandera DataFrame schemas
│   └── data/
│       └── registry.yaml   # Central corpus registry (YAML)
├── tests/                  # pytest test files
│   ├── test_corpus.py      # Corpus class tests
│   ├── test_init.py        # Public API tests
│   ├── test_registry.py    # Registry loading tests
│   ├── test_schemas.py     # DataFrame schema tests
│   ├── test_validate_registry.py  # Registry validation tests
│   └── test_validation.py  # Input validation tests
├── docs/                   # MkDocs documentation source
│   ├── mkdocs.yaml         # MkDocs configuration
│   ├── index.md            # Homepage
│   ├── getting-started.md  # Getting started guide
│   ├── usage.md            # Usage documentation
│   ├── CHANGELOG.md        # Changelog
│   ├── corpora/            # Per-corpus documentation pages
│   └── images/             # Documentation images
├── sources/                # Raw corpus curation code
│   ├── README.md           # Curation guidelines and versioning
│   └── <corpus_name>/      # Per-corpus processing (e.g., hvdc/, ucsc1996/)
│       └── prepare.ipynb   # Jupyter notebook to download, clean, validate data
├── scripts/
│   └── validate_registry.py  # Registry validation script (used in CI)
├── pyproject.toml          # Project configuration (deps, pytest, ruff)
└── README.md               # User documentation
```

### Configuration Files

- **pyproject.toml**: All project configuration (build system, dependencies, pytest, ruff, coverage)
- No separate setup.py, setup.cfg, requirements.txt, or tox.ini files

## CI/GitHub Workflows

### tests.yaml (Primary CI)

Runs on: push, pull requests

Matrix: Python 3.11, 3.12, 3.13, 3.14 on Ubuntu, macOS, Windows

Steps:

1. Checkout repository
2. Setup Python (matrix version)
3. Install package: `pip install -e ".[dev]"`
4. Run tests: `pytest tests/ --cov --cov-branch --cov-report=xml`
5. Upload coverage to Codecov

### ruff.yaml (Linting)

Runs on: push, pull requests

Steps:

1. Checkout repository
2. Run linting: `ruff check --output-format=github`
3. Run formatting check: `ruff format --check --diff`

### docs.yaml (Documentation)

Runs on: push to main, pull requests to main

Steps:

1. Checkout repository
2. Setup Python 3.11
3. Install docs dependencies: `pip install .[docs]`
4. Build docs: `mkdocs build --config-file docs/mkdocs.yaml`
5. Deploy to GitHub Pages (on main branch only)

## Key Implementation Details

### Registry Format

The `registry.yaml` file must:

- Have corpora and collections in **alphabetical order**
- Each corpus must have: title, brief_description, long_description, citations, environment, probe, includes_norecall, column_map (with report and author keys), author_columns, latest, versions
- Each version must have: download_url, hash (format: `md5:...` or `sha256:...`), doi
- Collections reference corpora by ID; all referenced corpora must exist

### Data Schemas (pandera)

- **ReportsSchema**: requires `author` and `report` columns
- **AuthorsSchema**: requires `author` column (must be unique)
- **AggregateReportsSchema**: requires `corpus`, `author`, `report` columns (strict, no extra columns)

### Text Normalization

The `_normalize_text()` function in `_corpus.py` uses `ftfy` for Unicode normalization and handles curly quotes, ellipses, and mojibake.

### Corpus Curation (sources/)

Each corpus has a subdirectory in `sources/` containing:

- `prepare.ipynb`: Jupyter notebook that downloads, cleans, and validates raw data
- Output: Cleaned CSV uploaded to Zenodo with versioning (MAJOR.MINOR.PATCH)

Curation applies: UTF-8 encoding fixes (ftfy), whitespace cleanup, empty cell removal, duplicate checks, and metadata validation. See `sources/README.md` for full guidelines.

## Testing Patterns

Tests use pytest fixtures defined in `tests/conftest.py`:

- `mock_registry`: Creates a mock registry with one corpus and one collection
- `mock_csv_file`: Creates a temporary CSV file for corpus loading tests

Use `unittest.mock.patch` to mock registry loading and file operations.

## Common Errors and Solutions

1. **ModuleNotFoundError**: Run `pip install -e ".[dev]"` first
2. **Registry validation fails**: Ensure alphabetical ordering, check hash format (`md5:...`), verify all collection corpus references exist
3. **Ruff errors**: Run `ruff check --fix .` to auto-fix, then `ruff format .` for formatting

## Validation Checklist

Before submitting changes:

1. `pip install -e ".[dev]"` - Install package
2. `ruff check .` - Pass linting
3. `ruff format --check .` - Pass formatting
4. `pytest` - All tests pass
5. `python scripts/validate_registry.py` - Pass (if modifying registry.yaml)

Trust these instructions. Only search the codebase if information is incomplete or found to be incorrect.
