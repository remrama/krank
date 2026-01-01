# sddb

Dream reports collected from a variety of sources and aggregated in the public
[Sleep and Dream Database](https://sleepanddreamdatabase.org).

| | Summary |
|--:|:--|
| Source | [Sleep and Dream Database](https://sleepanddreamdatabase.org) |
| References | Bulkeley, K. (2014). Digital dream analysis: A revised method. _Conscious Cogn_. doi:[10.1016/j.concog.2014.08.015](https://doi.org/10.1016/j.concog.2014.08.015) <br> Bulkeley, K. (2023). New approaches in the empirical study of dreams. _Poligrafi_. doi:[10.35469/poligrafi.2023.412](https://doi.org/10.35469/poligrafi.2023.412) |
| Processing code | [`prepare.ipynb`](prepare.ipynb) |
| Processing environment | [`environment.yaml`](environment.yaml) |

# Raw (original source) data

The SDDb source file comes from a [Zenodo archive](https://doi.org/10.5281/zenodo.18076716). See the description there for details on how the data was initially collected.

For older versions with less dream reports but more metadata (as columns), see access points mentioned in [this GitHub Issue](https://github.com/remrama/sddb/issues/1) and [./compare.ipynb](./compare.ipynb). The current version has 2 additional datasets and ~5k more dream reports than the previous versions, but again with less metadata.

## Changes made

> These are the changes made to the original dataset.

* Remove excess metadata columns
* Clean/standardize dream report text
* Merge related datasets and authors
* Rename datasets
* Remove entries with extreme word counts
* Remove datasets with small sample sizes
