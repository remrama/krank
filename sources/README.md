<h1 align="center">Krank sources collection</h1>

This folder houses the processing code for krank's curated collection of dream corpora.

Each repository here contains Python code that downloads, inspects, preprocesses, and repackages the dream reports into a single cleaned and validated csv file.

The output datasets are accessible as tabular CSV files through their respective Zenodo archive or as pandas dataframes through the Python package [krank](https://github.com/remrama/krank).

> 🤝 **Credits:** The structure and underlying code of this folder are modeled heavily after the those found within the [Fatiando a Terra FAIR data collection](https://github.com/fatiando-data). See the top-level krank [README](../README.md#contributing) for details.

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

---

<h2 align="center">Versioning</h2>

All output is stored in version-controlled Zenodo archives, where each Zenodo record has its own version history. They follow a general semver MAJOR.MINOR.PATCH structure, where:

* MAJOR releases involve changes to schema (new columns, renamed columns, changed semantics)
* MINOR releases involve new additions to data (more rews, new optional columns)
* PATCH releases involve small fixes (typos, encoding issues, metadata corrections)

Note this is not _strictly_ semver because any changes to the dataset (including MINOR and PATCH) are probably "breaking" as far as analyses and results go. Therefore, always stay up to date on new dataset versions, regardless of the release type.

While these rules do not relate directly to krank package versioning, they will inherently influence because the `registry.yaml` file in krank will need to be updated every time a corpus is added or bumped. See the krank [README](../README.md) for details on krank versioning.

* Major releases involve changes to HTML output
* Minor releases involve changes to tabular DreamBank output
* Patch releases involve changes to sub-corpora output (or any other non-functional changes)
