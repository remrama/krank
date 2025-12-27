# krank

**Fetch curated dream reports.**

krank provides easy access to curated, versioned dream text corpora for reproducible research.

## Why krank?

- **Curated**: Datasets are cleaned, documented, and vetted for quality
- **Versioned**: Pin exact versions for reproducible analyses
- **Accessible**: One-line access to any corpus

## Quick Start

```bash
pip install krank
```

```python
import krank

# See what's available
krank.list_corpora()

# Load a corpus
corpus = krank.load("zhang2019")

# Access dream reports
corpus.reports
```

[Get Started](getting-started.md)
