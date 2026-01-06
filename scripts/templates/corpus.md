# {{ name }}

{{ long_description }}

## Overview

| Field | Value |
|------:|:------|
| **Title** | {{ title }} |
| **DOI** | [{{ doi }}](https://doi.org/{{ doi }}) |
| **Environment** | {{ environment }} |
| **Probe** | {{ probe }} |
| **_N_ reports** | {{ n_reports }} |
| **_N_ authors** | {{ n_authors }} |
| **_M_ report length** | {{ m_report_length }} words |
| **_Mdn_ report length** | {{ mdn_report_length }} words |

## Citation

{{ citation_text }}

## Columns

### Reports

| Column | Description |
|-------:|:------------|
| `author` | Unique author identifier |
| `report` | Text of dream report |
{{ report_columns_table }}

### Authors

| Column | Description |
|-------:|:------------|
| `author` | Unique author identifier |
{{ author_columns_table }}

## Source

- **Processing code**: [Notebook](notebooks/{{ name }}/prepare.ipynb)
- **Processed file**: [Zenodo](https://doi.org/{{ doi }})

## Version History

| Version | Hash | DOI |
|:-------:|:----:|:---:|
{{ version_table }}
