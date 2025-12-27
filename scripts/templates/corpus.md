# {{ name }}

{{ description }}

## Overview

| Field | Value |
|-------|-------|
| **Title** | {{ title }} |
| **Reports** | {{ n_reports }} |
| **Language** | {{ language }} |
| **License** | {{ license }} |

## Citation
```
{{ citation }}
```

## Usage
```python
import krank

corpus = krank.load("{{ name }}")
corpus.reports
```

## Columns

### Reports

| Column | Description |
|--------|-------------|
{{ report_fields_table }}

### Authors

| Column | Description |
|--------|-------------|
| `author_id` | Unique author identifier |
{{ author_fields_table }}

## Source

- **Original**: [{{ source_url }}]({{ source_url }})
- **Download**: [Zenodo]({{ download_url }})

## Version History

| Version | Hash |
|---------|------|
{{ version_table }}
