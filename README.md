[![PyPI](https://img.shields.io/pypi/v/krank)](https://pypi.org/project/krank)
[![Downloads](https://pepy.tech/badge/krank)](https://pepy.tech/badge/krank)
[![codecov](https://codecov.io/gh/remrama/krank/branch/main/graph/badge.svg)](https://codecov.io/gh/remrama/krank)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

# krank

Fetch curated dream reports.

See the [online documentation](https://remrama.github.io/krank) for details.

## Installation

```shell
pip install --upgrade krank
```

## Usage

```python
import krank

# View a list of available corpora.
krank.list_corpora()
# ['hvdc', 'zhang2019']

# View a list of available versions for a corpus.
krank.list_versions("zhang2019")
# ['1']

# Print metadata about a single corpus.
krank.info("zhang2019")
# Corpus: zhang2019
#   Title: Zhang & Wamsley, 2019
#   Description: Dream reports collected from a laboratory polysomnography study
#   Version: 1
#   Citations: Zhang, J., & Wamsley, E. J. (2019); Wong, W., Herzog, R., ... (2025)

# Load a corpus.
corpus = krank.load("zhang2019")
corpus
# Corpus('zhang2019')

# Print corpus info (same as krank.info()).
print(corpus)
# Corpus: zhang2019
#   Title: Zhang & Wamsley, 2019
#   Description: Dream reports collected from a laboratory polysomnography study
#   Version: 1
#   Citations: Zhang, J., & Wamsley, E. J. (2019); Wong, W., Herzog, R., ... (2025)

# Get number of reports and authors.
corpus.n_reports
# 120
corpus.n_authors
# 16

# Return metadata as a dictionary.
corpus.metadata["title"]
# 'Zhang & Wamsley 2019 Dream Reports'
corpus.metadata["hash"]
# 'md5:a61a3c56f4ee8c14e4a6466044df88f8'
corpus.metadata["description"]
# 'Dream reports collected from a laboratory polysomnography study'

# Return unique authors and their associated metadata in a tidy dataframe.
corpus.authors.head()
#    author  age     sex
# 0      10   23    Male
# 1      26   18    Male
# 2      30   19  Female
# 3      42   20    Male
# 4      83   20    Male

# Return dream reports and their associated metadata in a tidy dataframe.
corpus.reports.head()
#    author      time stage_intended stage_actual  experience                                             report
# 0      10  07:17:27            REM      Morning        True  I umm I was with my parents and we're having a...
# 1      10  02:07:02             N2         NREM        True  Ummm... trying to put um everything together [...
# 2      10  03:50:48            REM          REM        True  Yes I'm ummm... I'm in an argument with a...wi...
# 3      10  00:16:08             N1           SO       False  What? I don't have a dream. What was your ques...
# 4      10  00:54:12             N2           SO        True  Uhuh. Umm let's see.. Running around...(silence).
```

## Contributing

Open an [Issue](https://github.com/remrama/krank/issues) to request a new corpus (or for any other reason).

Adding a new corpus does not require any changes to underlying code. It only needs to be added to the [registry.yaml](./src/krank/data/registry.yaml) file (and one line to [mkdocs.yaml](./docs/mkdocs.yaml)). Browse that for other corpora and see what would need to be filled out for the new dataset. To keep things separate, most of the corpus curation code is over in the [krank sources collection](https://github.com/krank-sources), a set of repositories under a single organization heading. But if you want a new dataset there, place an Issue here in this repository.

The registry follows a JSON schema defined in [registry-schema.yaml](./src/krank/data/registry-schema.yaml). This file documents all required and optional fields with descriptions.

### Validating Registry Changes

After making changes to the registry, validate them locally using:

```shell
python scripts/validate_registry.py
```

This script checks:
- Schema compliance (all required fields present with correct types)
- Alphabetical ordering of collections and corpora
- Valid references from collections to corpora
- Proper hash formats and URLs

The validation runs automatically as part of the test suite in CI.

## Credits

This project would not be possible without the work of the [**Fatiando a Terra Project**](https://www.fatiando.org), namely a heavy dependency on [pooch](https://www.github.com/fatiando/pooch), an inspiration from [ensaio](https://www.github.com/fatiando/ensaio), and a structural model from the [Fatiando a Terra FAIR data collection](https://github.com/fatiando-data).

> Uieda, L., V. C. Oliveira Jr, and V. C. F. Barbosa (2013), Modeling the Earth with Fatiando a Terra, _Proceedings of the 12th Python in Science Conference_, pp. 91-98. doi:[10.25080/Majora-8b375195-010](https://doi.org/10.25080/Majora-8b375195-010)
