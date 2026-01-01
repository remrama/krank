<h1 align="center">Krank sources collection</h1>

This folder houses the processing code for krank's curated collection of dream corpora.

Each repository here contains Python code that downloads, inspects, preprocesses, and repackages the dream reports into a single cleaned and validated csv file.

The output datasets are accessible as tabular CSV files through their respective Zenodo archive or as pandas dataframes through the Python package [krank](https://github.com/remrama/krank).

> [!NOTE]
> **Credits:** The structure and underlying code of these folders are modeled heavily after the [Fatiando a Terra FAIR data collection](https://github.com/fatiando-data). This overall project would not be possible without other products from the [**Fatiando a Terra Project**](https://www.fatiando.org), namely [pooch](https://www.github.com/fatiando/pooch) for data access and [ensaio](https://www.github.com/fatiando/ensaio) as inspiration for the broader [krank](https://github.com/remrama/krank) project.
> 
> > Uieda, L., V. C. Oliveira Jr, and V. C. F. Barbosa (2013), Modeling the Earth with Fatiando a Terra, _Proceedings of the 12th Python in Science Conference_, pp. 91-98. doi:[10.25080/Majora-8b375195-010](https://doi.org/10.25080/Majora-8b375195-010)

---

<h2 align="center">Curation</h2>

Each source dataset is processed using a combination of automated and manual merges, conversions, checks, and corrections.

* If dream reports are included across multiple individual files, they are merged into a single csv file.
* If dream reports have associated metadata in other files, the metadata and dream reports are merged into a single csv file.
* If dream reports are included in a much larger source file, they are extracted out for easier access.
* If source files are in a non-csv format, they are converted to csv.

The dream reports are adjusted as needed to pass the following checks:

* ✅ Strict UTF-8 encoding (e.g., no mojibake) (fixes applied with [ftfy](https://github.com/rspeer/python-ftfy))
* ✅ Simplified UTF-8 encoding (e.g., no curly quotes) (fixes applied with [ftfy](https://github.com/rspeer/python-ftfy))
* ✅ No extraneous surrounding whitespace
* ✅ No extraneous surrounding quotes
* ✅ No empty cells
* ✅ No extreme word lengths (unless sensible)
* ✅ No duplicated dream reports (unless sensible)
* ✅ General quality inspection

The metadata, if present, is adjusted as needed to pass the following checks:

* ✅ No derived columns (i.e., those with values derivable from another column)
* ✅ No categorical values represented as integers
* ✅ Sensible values (e.g., typos, positive age values)
* ✅ Consistency across authors
