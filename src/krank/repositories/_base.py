from importlib.resources import files
import pandas as pd
import pooch
from bs4 import BeautifulSoup
from docx import Document

# class KrankPup:
#     def __init__(self, repo_id):
#         self.repo_id = repo_id
#     def get_registry_path(self):
#         return f"./registries/{self.repo_id}.txt"
# repo = KrankPup("dreambank")

import json
import string
import hashlib
import zipfile
from pathlib import Path


def generate_dreamer_id(old_dreamer_id, last_idx=12):
    """
    Generates a unique id name
    refs:
    - md5: https://stackoverflow.com/questions/22974499/generate-id-from-string-in-python
    - sha3: https://stackoverflow.com/questions/47601592/safest-way-to-generate-a-unique-hash
    (- guid/uiid: https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python?noredirect=1&lq=1)
    """
    m = hashlib.md5()
    author_str = str(old_dreamer_id).encode("utf-8")
    m.update(author_str)
    unique_digit_str = str(int(m.hexdigest(), 16))
    unique_letter_str = "".join(string.ascii_uppercase[int(x)] for x in unique_digit_str)
    return unique_letter_str[:last_idx]


class KrankRepo:

    def __init__(self, repo_id, **pup_kwargs):
        self._repo_id = repo_id
        self._init_pup(**pup_kwargs)

    def __repr__(self):
        return f"Krank Repository: {self.repo_id}"

    def __str__(self):
        return self.__repr__

    @property
    def repo_id(self):
        return self._repo_id

    @property
    def pup(self):
        return self._pup


    def _init_pup(self, **kwargs):
        kwargs.setdefault("base_url", "")
        kwargs.setdefault("path", pooch.os_cache("krank").joinpath(self.repo_id))
        self._base_url = ""
        self._pup = pooch.create(**kwargs)
        if "registry" not in kwargs:
            registry_path = files("krank.repositories.data.registries").joinpath(f"{self.repo_id}.txt")
            self._pup.load_registry(registry_path)


    def read_file(self, fname, *args, reader=None, **kwargs):
        """Read a file from the repository.

        Available files:

        * ``dream.dataset_3.10.2023.csv``

        Examples
        --------
        >>> from krank.repositories import Samson2023
        >>> df = Samson2023().read_file("dream.dataset_3.10.2023.csv")
        >>> df.head()
        """
        fp = self.pup.fetch(fname)
        suffix = Path(fp).suffix
        if reader is not None:
            return reader(fp, *args, **kwargs)
        elif suffix == ".csv":
            return pd.read_csv(fp, *args, **kwargs)
        elif suffix == ".tsv":
            return pd.read_table(fp, *args, **kwargs)
        elif suffix == ".txt":
            with open(fp, "r", **kwargs) as f:
                return f.read()
        elif suffix in [".doc", ".docx"]:
            return Document(fp, *args, **kwargs)
        elif suffix == ".json":
            with open(fp, "r", **kwargs) as f:
                return json.load(f)
        elif suffix == ".html":
            with open(fp, "rb") as f:
                return BeautifulSoup(f, *args, **kwargs)
        raise ValueError

    def read_archive(self, fname, archive_fname, *args, reader=None, **kwargs):
        suffix = Path(archive_fname).suffix
        fp = self.pup.fetch(fname)
        with zipfile.ZipFile(fp) as zf:
            with zf.open(archive_fname, "r") as f:
                if reader is not None:
                    return reader(f, *args, **kwargs)
                if suffix == ".txt":
                    return f.read().decode("utf-8")
                elif suffix == ".csv":
                    return pd.read_csv(f, *args, **kwargs)
                elif suffix == ".tsv":
                    return pd.read_table(f, *args, **kwargs)
                raise ValueError
