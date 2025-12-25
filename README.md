# krank

Load standardized (or source) dream datasets.

Detailed usage information is available in the [online documentation](https://dxelab.github.io/krank).


## Installation

```shell
pip install krank
```

## Quick start

```python
>>> import krank

>>> # Load a dataset
>>> dreams = krank.read_hadza()
>>> dreams.head()
         Author  Age     Sex                                              Dream
0  CGBFHIIHECGE   46    Male  I was an antelope in a stony landscape with br...
1  CGBFHIIHECGE   46    Male  I dreamt that theives came and were slaughteri...
2  CGBFHIIHECGE   46    Male  I dreamt a buffalo hit me. I was in Numbeya bu...
3  CGBFHIIHECGE   46    Male  I dreamt I fell into a well that is near the H...
4  CGGAADGJBEHH   38  Female  I remember being chased by an elephant in a lo...

>>> # Datasets are quality-controlled and read into Pandas with appropriate data types.
>>> dreams.info()
<class 'pandas.core.frame.DataFrame'>
Index: 51 entries, 0 to 50
Data columns (total 4 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   Author  51 non-null     category
 1   Age     51 non-null     int32
 2   Sex     51 non-null     category
 3   Dream   51 non-null     string
dtypes: category(2), int32(1), string(1)
memory usage: 1.9 KB

>>> # Load the metadata
>>> info = krank.get_hadza_info()
>>> info
```

## Advanced usage

Krank harmonizes datasets.
Access un-harmonized/raw datasets from the `repositories` module.

```python
>>> from krank.repositories import Samson2023

>>> repo = Samson2023()
>>> df = repo.read_dreamdataset3102023()
  ID Population  Age  ...  sqrt.neg  sqrt.anx                                              Dream
0  1      Hadza   46  ...  0.707107  0.707107  I was an antelope in a stony landscape with br...
1  1      Hadza   46  ...  0.707107  0.707107  I dreamt that theives came and were slaughteri...
2  1      Hadza   46  ...  0.707107  0.707107  I dreamt a buffalo hit me. I was in Numbeya bu...
3  1      Hadza   46  ...  0.707107  0.707107  I dreamt I fell into a well that is near the H...
4  2      Hadza   38  ...  0.707107  0.707107  I remember being chased by an elephant in a lo...

>>> # Customize loading by returning raw filepaths and loading manually.
>>> import pandas as pd
>>> fp = repo.fetch("dream.dataset_3.10.2023.csv")
>>> df = pd.read_csv(fp, index_col=["Population", "ID"])
>>> df.head()
               Age     Sex  ...  sqrt.anx                                              Dream
Population ID               ...
Hadza      1    46    Male  ...  0.707107  I was an antelope in a stony landscape with br...
           1    46    Male  ...  0.707107  I dreamt that theives came and were slaughteri...
           1    46    Male  ...  0.707107  I dreamt a buffalo hit me. I was in Numbeya bu...
           1    46    Male  ...  0.707107  I dreamt I fell into a well that is near the H...
           2    38  Female  ...  0.707107  I remember being chased by an elephant in a lo...
```

See the [online documentation](https://dxelab.github.io/krank) for more.
