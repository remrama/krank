"""Build aggregate CSV of all corpora for release artifact."""

from csv import QUOTE_NONNUMERIC

import pandas as pd

import krank


def compile_single_corpus(corpus_name: str) -> pd.DataFrame:
    """Load a single corpus and return its reports DataFrame."""
    print(f"Loading {corpus_name}...")
    corpus = krank.load(corpus_name)
    df = corpus.reports.copy()
    version = corpus.metadata["version"]
    corpus_string = f"{corpus_name}-v{version}"
    df.insert(0, "corpus_version", corpus_string)
    return df

def build_aggregate(output_path: str = "reports.csv") -> None:
    """Load all corpora reports and combine into single CSV."""
    corpora = krank.list_corpora()
    
    df = pd.concat([ compile_single_corpus(name) for name in corpora ], ignore_index=True)
    
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
