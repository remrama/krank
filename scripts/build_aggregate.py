"""Build aggregate CSV of all corpora for release artifact.

This script compiles all available corpora into a single CSV file for distribution
as a release artifact. Each report is tagged with its source corpus and version.
"""

from csv import QUOTE_NONNUMERIC

import pandas as pd

import krank


def compile_single_corpus(corpus_name: str) -> pd.DataFrame:
    """Load a single corpus and return its reports DataFrame.

    Parameters
    ----------
    corpus_name : str
        Name of the corpus to load.

    Returns
    -------
    pd.DataFrame
        DataFrame containing all reports from the corpus with an added
        'corpus_version' column identifying the source.
    """
    print(f"Loading {corpus_name}...")
    corpus = krank.load(corpus_name)
    df = corpus.reports.copy()
    version = corpus.metadata["version"]
    corpus_string = f"{corpus_name}-v{version}"
    df.insert(0, "corpus_version", corpus_string)
    return df


def build_aggregate(output_path: str = "reports.csv") -> None:
    """Load all corpora reports and combine into single CSV.

    Parameters
    ----------
    output_path : str, default="reports.csv"
        Path where the aggregate CSV file should be written.

    Notes
    -----
    The output CSV uses UTF-8-BOM encoding for improved Excel compatibility
    and numeric quoting for all fields.
    """
    corpora = krank.list_corpora()

    df = pd.concat([compile_single_corpus(name) for name in corpora], ignore_index=True)

    df.to_csv(
        path_or_buf=output_path,
        index=False,
        sep=",",
        mode="x",
        encoding="utf-8-sig",  # for improved Excel compatibility
        lineterminator="\n",
        quoting=QUOTE_NONNUMERIC,
        quotechar='"',
        doublequote=True,
    )
    print(f"Wrote {len(df)} reports from {len(corpora)} corpora to {output_path}")


if __name__ == "__main__":
    build_aggregate()
