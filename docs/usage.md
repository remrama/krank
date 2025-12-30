# Usage

## Discovering Corpora
```python
import krank

# List all available corpora
krank.list_corpora()

# Filter by language
krank.list_corpora(language="en")

# Get metadata without downloading
krank.info("zhang2019")
# Corpus: zhang2019
#   Title: Zhang & Wamsley, 2019
#   Description: Dream reports collected from a laboratory polysomnography study
#   Version: 1
#   Citations: Zhang, J., & Wamsley, E. J. (2019); Wong, W., Herzog, R., ... (2025)
```

## Loading Data
```python
corpus = krank.load("zhang2019")

# Print corpus info
print(corpus)
# Corpus: zhang2019
#   Title: Zhang & Wamsley, 2019
#   Description: Dream reports collected from a laboratory polysomnography study
#   Version: 1
#   Citations: Zhang, J., & Wamsley, E. J. (2019); Wong, W., Herzog, R., ... (2025)
```

The data is not downloaded until you access it:
```python
corpus.reports  # triggers download on first access
```

## Corpus Attributes

| Attribute | Description |
|-----------|-------------|
| `corpus.reports` | DataFrame of dream reports (tidy format) |
| `corpus.authors` | DataFrame of author metadata (deduplicated) |
| `corpus.n_reports` | Number of reports in corpus |
| `corpus.n_authors` | Number of unique authors in corpus |
| `corpus.metadata` | Dict of corpus metadata from registry |
| `corpus.path` | Local path to cached file |
| `corpus.name` | Corpus name |

## Collections

Some corpora belong to collections (e.g., DreamBank):
```python
# List collections
krank.list_collections()

# Get collection info
krank.collection_info("dreambank")
```

## Caching

Downloaded files are cached locally. krank uses `pooch` for caching, storing files in your system's default cache directory.
