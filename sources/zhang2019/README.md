# zhang2019

Processing code for the curated `zhang2019` dataset, `krank` access point.

The `zhang2019` dataset is a collection of dream reports from a serial awakening study with an emphasis on NREM dreams.

## About this repository

This is a place to format and prepare the original dataset for use in [krank](https://github.com/remrama/krank).

It includes the source code that prepares the datasets for redistribution ln Zenodo by consolidating relevant files, trimming excess metadata, validating values, standardizing text, etc.

The goal is to provide a single-file access point that is stable, versioned, and quality controlled.

## Data details

| | Source data |
|--:|:--|
| File | `Zhang & Wamsley 2019.zip` |
| Size | `1000.56` MB |
| MD5 | `md5:5854cfea4925f57d4d0a440518f4b72a` |
| SHA256 | `sha256:00b17e29bd1776a4b77fa978b018a21969b3ad588fd76b0a15998126ef90b64c` |
| Source | [figshare](https://doi.org/10.6084/m9.figshare.22226692) |
| Direct download | [figshare](https://figshare.com/ndownloader/files/39504757) |
| Version | [v1](https://doi.org/10.6084/m9.figshare.22226692.v1) |
| License | [CC BY](https://creativecommons.org/licenses/by/4.0) |
| References | Zhang & Wamsley, 2019, _Psychophysiology_, EEG predictors of dreaming outside of REM sleep. doi:[10.1111/psyp.13368](https://doi.org/10.1111/psyp.13368)<br>Wong et al., 2025, _Nat Commun_, A dream EEG and mentation database. doi:[10.1038/s41467-025-61945-1](https://doi.org/10.1038/s41467-025-61945-1) |

| | Krank data |
|--:|:--|
| File | `zhang2019.csv` |
| Size | `0.09` MB |
| MD5 | `md5:a61a3c56f4ee8c14e4a6466044df88f8` |
| SHA256 | `sha256:7474a34fa01c7313315434fd96b044660f397cf780ff37d8d8e30fdceb616773` |
| Version | `v1-alpha.1` |
| Archive | [Zenodo](https://zenodo.org/records/18050635) |
| DOI | [10.5281/zenodo.18050635](https://doi.org/10.5281/zenodo.18050635) |
| License | [CC BY](https://creativecommons.org/licenses/by/4.0) |
| Processing code | [`prepare.ipynb`](./prepare.ipynb) |

## Processing details

See the [krank sources README](../README.md) for typical processing checks and corrections. For specific changes applied to this dataset during processing, see the [prepare.ipynb](./prepare.ipynb) notebook.
