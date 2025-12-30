# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0.dev2] - 2025-12-30

### Added
- Corpus info messages (#25)
- Pretty-print corpus metadata with `krank.info()` function
- String representation for Corpus objects displaying metadata

### Changed
- Improved user experience when inspecting corpus information

## [0.0.1.dev3]

### Added
- Initial development release
- Core functionality to fetch curated dream reports
- Support for loading versioned corpora
- Registry system for managing corpus metadata
- Functions: `list_corpora()`, `list_versions()`, `load()`, `list_collections()`
- Initial corpus support: hvdc, urbina1975, zhang2019
- Data validation with Pandera schemas
- Automatic corpus downloading and caching with Pooch
- Documentation site with MkDocs Material

[Unreleased]: https://github.com/remrama/krank/compare/v0.1.0.dev2...HEAD
[0.1.0.dev2]: https://github.com/remrama/krank/releases/tag/v0.1.0.dev2
[0.0.1.dev3]: https://github.com/remrama/krank/releases/tag/v0.0.1.dev3
