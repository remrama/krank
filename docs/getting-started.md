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
# Corpus: zhang2019
#   Title: Zhang & Wamsley, 2019
#   Description: Dream reports collected from a laboratory polysomnography study
#   Version: 1
#   Citations: Zhang, J., & Wamsley, E. J. (2019); Wong, W., Herzog, R., ... (2025)

# Load a corpus
corpus = krank.load("zhang2019")

# Access the data
corpus.reports      # dream reports (tidy)
corpus.authors      # author metadata (deduplicated)
corpus.n_reports    # number of reports
corpus.n_authors    # number of unique authors
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
