import json
from importlib.resources import files

import pandas as pd

from ._base import KrankRepo, generate_dreamer_id



class SDDb(KrankRepo):
    def __init__(self, version=1):
        super().__init__(repo_id="sddb")


    def _read_columns(self):
        fp = files("krank.repositories.data").joinpath("sddb-columns.json")
        with open(fp, "rt", encoding="utf-8") as f:
            columns = json.load(f)
        return columns

    def _read_surveys(self):
        fp = files("krank.repositories.data").joinpath("sddb-surveys.json")
        with open(fp, "rt", encoding="utf-8") as f:
            surveys = json.load(f)
        return surveys

    def read_file(self, fname, reader=None, **kwargs):
        """Read a raw repository file.

        .. important::

            This file comes from Zenodo repository.
            Provides version control.
            The version control only applies to the raw data, not processing here.

        Available files:

        * ``dream-export.csv``

        """
        fp = self.pup.fetch(fname)
        if reader is not None:
            return reader(fp, **kwargs)
        elif fname == "dream-export.csv":
            kwargs.setdefault("low_memory", False)
            return pd.read_csv(fp, **kwargs)


    def read_tidy(self, *, return_authors=True):
        """
        Slightly opinionated.
        - DREAMS ONLY in tidy format.
        - Fix errors.
        - Drop NA.
        - Rename columns.
        - Remove redundancies.
        - Set column datadtypes.
        - Replace values.
        """
        columns = self._read_columns()
        columns = {k: v for k, v in columns.items() if v["use"]}
        usecols = list(columns)
        dtypes = {k: v["dtype"].replace("int", "Int64") for k, v in columns.items()}
        df = self.read_file("dream-export.csv", usecols=usecols, dtype=dtypes)
        for k, v in columns.items():
            if v["categorical"]:
                df[k] = pd.Categorical(df[k], ordered=v["ordered"])
        replacements = {k: v["response_options"] for k, v in columns.items() if isinstance(v.get("response_options"), dict)}
        for col, repl in replacements.items():
            if col == "dream_entry_title":
                # Have to get out of Categories and recode bc it won't allow non-unique mapping
                df[col] = pd.Categorical(df[col].astype("string").replace(repl), ordered=columns[col]["ordered"])
            else:
                df[col] = df[col].cat.rename_categories(repl)
        # Apply minimal corrections.
        df.loc[df["survey"].eq("Anna"), "respondent"] = df.loc[df["survey"].eq("Anna"), "respondent"].bfill().ffill()
        df.loc[df["survey"].eq("Aristides"), "respondent"] = df.loc[df["survey"].eq("Aristides"), "respondent"].bfill().ffill()
        df["survey"] = pd.Categorical(df["survey"].astype("string"), ordered=columns["survey"]["ordered"])
        renamings = {k: v["short_name"] for k, v in columns.items()}
        df = df.rename(columns=renamings)
        df = df.dropna(how="all", axis=1)
        df = df.drop_duplicates()
        dreams = df.pop("Dream")
        df.insert(df.shape[1], "Dream", dreams)
        dreamers = df.pop("Dreamer")
        df.insert(0, "Dreamer", dreamers)
        datasets = df.pop("Dataset")
        df.insert(0, "Dataset", datasets)
        # new_names = {k: generate_dreamer_id(k) for k in df["Dreamer"].cat.categories}
        dreamer_map = {k: generate_dreamer_id(k) for k in df["Dreamer"].unique()}
        assert len(set(dreamer_map)) == len(set(dreamer_map.values()))
        df["Dreamer"] = df["Dreamer"].cat.rename_categories(dreamer_map)
        df = df.drop(columns=["WordCount", "UploadDate"])
        # I think RaceValues has all that's needed
        df = df.drop(columns=["Race", "RaceD", "RaceRecode", "RaceHispanic"])
        df = df.rename(columns={"RaceValues": "Race"})
        df = df.sort_values(["Dataset", "Dreamer"])
        df = df.reset_index(drop=True)
        ##
        dreams = df[["Dataset", "Dreamer", "Probe", "Dream"]].copy()
        dreamers = df.drop(columns=["Probe", "Dream"])
        dreams = dreams.reset_index(drop=True)
        dreamers = dreamers.reset_index(drop=True)
        if return_authors:
            return dreams, dreamers
        return dreams

    def read_dataset(self, dataset_id, *, return_authors=True):
        dreams, authors = self.read_tidy(return_authors=return_authors)
        dreams = dreams[dreams["Dataset"].eq(dataset_id)]
        authors = authors[authors["Dataset"].eq(dataset_id)]
        dreams = dreams.dropna(how="all", axis=1)
        authors = authors.dropna(how="all", axis=1)
        dreams = dreams.reset_index(drop=True)
        authors = authors.reset_index(drop=True)
        # TODO: Redo categories in case some trimmed
        if return_authors:
            return dreams, authors
        return dreams

    # def read_authors(self):
    #     # Read author info (if separate from dreams).
    #     df = self.read_dreams()
    #     author_columns = # those that are consistent across participant IDs

    #     # Read dreams
    #     # Make sure only using the authors still present in dreams.

