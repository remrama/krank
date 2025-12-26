# zhang2019

Dream reports collected during a laboratory polysomnography study.

## Overview

| Field | Value |
|-------|-------|
| **Title** | Zhang & Wamsley 2019 Dream Reports |
| **Reports** | 10+ |
| **License** | CC-BY-4.0 |

## Citation
```
Zhang, W., & Wamsley, E. J. (2019). ...
```

## Usage
```python
import krank

corpus = krank.load("zhang2019")
corpus.reports
```

## Columns

### Reports

| Column | Description |
|--------|-------------|
| `dream` | Dream report text |
| `author_id` | Unique author identifier |
| ... | ... |

### Authors

| Column | Description |
|--------|-------------|
| `author_id` | Unique author identifier |
| `age` | Author age |
| `sex` | Author sex |

## Source

- **Original**: [Figshare](https://figshare.com/...)
- **Processed**: [Zenodo](https://zenodo.org/...)
- **Processing code**: [krank-sources/zhang2019](https://github.com/krank-sources/zhang2019)

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2024-XX-XX | Initial release |
