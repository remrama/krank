[![PyPI](https://img.shields.io/pypi/v/krank)](https://img.shields.io/pypi/v/krank)
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
# ['zhang2019']

# Print metadata about a single corpus.
krank.info("zhang2019")
# Corpus: zhang2019
#   Title: Zhang & Wamsley 2019 Dream Reports
#   Description: Dream reports collected from an laboratory polysomnography study

# Load a corpus.
corpus = krank.load("zhang2019")
corpus
# Corpus('zhang2019')

# Return metadata as a dictionary.
corpus.metadata["title"]
# 'Zhang & Wamsley 2019 Dream Reports'
corpus.metadata["hash"]
# 'md5:a61a3c56f4ee8c14e4a6466044df88f8'
corpus.metadata["description"]
# 'Dream reports collected from an laboratory polysomnography study'

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

Open an [Issue](https://github.com/remrama/krank) to request a new corpus (or for any other reason).

Adding a new corpus does not require any changes to underlying code. It only needs to be added to the [registry.yaml](./src/krank/data/registry.yaml) file (and one line to [mkdocs.yaml](./docs/mkdocs.yaml)). Browse that for other corpora and see what would need to be filled out for the new dataset. To keep things separate, most of the corpus curation code is over in the [krank sources collection], a set of repositories under a single organization heading. But if you want a new dataset there, place an Issue here in this repository.
