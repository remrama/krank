# krank

Fetch curated dream reports.

See the [online documentation](https://remrama.github.io/krank) for details.

## Installation

```shell
pip install --upgrade --force-reinstall krank
```

## Usage

```python
import krank

# View a list of available corpora.
krank.list_corpora()
# ['zhang2019']

# Print metadata about a single corpus.
>>> krank.info("zhang2019")
# Corpus: zhang2019
#   Title: Zhang & Wamsley 2019 Dream Reports
#   Description: Dream reports collected from an laboratory polysomnography study

# Load a corpus.
corpus = krank.load("zhang2019")
corpus
# Corpus('zhang2019')

# Return metadata as a dictionary.
for k, v in corpus.metadata.items():
  print(f"{k+':':>15}", v)
#          title: Zhang & Wamsley 2019 Dream Reports
#    description: Dream reports collected from an laboratory polysomnography study
#     column_map: {'report': 'Text of Report', 'author': 'Subject ID', 'age': 'Subject age', 'sex': 'Subject sex', 'time': 'Time of awakening', 'stage_intended': 'Intended last sleep stage', 'stage_actual': 'Actual last sleep stage', 'experience': 'Experience'}
#  author_fields: ['age', 'sex']
#        version: 1
#   download_url: https://zenodo.org/records/18050635/files/zhang2019.csv?download=1
#           hash: md5:a61a3c56f4ee8c14e4a6466044df88f8
          
# Return dream reports and their associated metadata in a tidy dataframe.
corpus.reports.head()
#    author      time stage_intended stage_actual  experience                                             report
# 0      10  07:17:27            REM      Morning        True  I umm I was with my parents and we're having a...
# 1      10  02:07:02             N2         NREM        True  Ummm... trying to put um everything together [...
# 2      10  03:50:48            REM          REM        True  Yes I'm ummm... I'm in an argument with a...wi...
# 3      10  00:16:08             N1           SO       False  What? I don't have a dream. What was your ques...
# 4      10  00:54:12             N2           SO        True  Uhuh. Umm let's see.. Running around...(silence).

# Return unique authors and their associated metadata in a tidy dataframe.
corpus.authors.head()
#    author  age     sex
# 0      10   23    Male
# 1      26   18    Male
# 2      30   19  Female
# 3      42   20    Male
# 4      83   20    Male
