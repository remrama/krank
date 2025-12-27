# Getting Started

## Installation
```bash
pip install krank
```

## Basic Usage
```python
import krank

# List available corpora
krank.list_corpora()
# ['zhang2019']

# Get info about a corpus without downloading
krank.info("zhang2019")

# Load a corpus
corpus = krank.load("zhang2019")

# Access the data
corpus.reports      # dream reports (tidy)
corpus.authors      # author metadata (deduplicated)
corpus.metadata     # corpus metadata dict
```

## Versioning

krank corpora are versioned. By default, you get the latest version:
```python
corpus = krank.load("zhang2019")
```

Pin a specific version for reproducibility:
```python
corpus = krank.load("zhang2019", version="1")
```

List available versions:
```python
krank.list_versions("zhang2019")
```
