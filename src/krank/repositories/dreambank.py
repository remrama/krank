import re

import pandas as pd
from bs4 import BeautifulSoup

from ._base import KrankRepo


class DreamBank(KrankRepo):
    """
    A tabular-formatted and version-controlled `DreamBank <https://dreambank.net>`_ access point.

    The secondary purpose is to provide a quick `DreamBank <https://dreambank.net>`_ data access point from Python.

    Any publications that utilized any of these datasets should cite the original DreamBank paper:
       Domhoff, G. W., & Schneider, A. (2008). Studying dream content using the archive and search engine on DreamBank.net. *Consciousness and Cognition*, 17(4), 1238-1247. doi:`10.1016/j.concog.2008.06.010 <https://doi.org/10.1016/j.concog.2008.06.010>`_

    """
    def __init__(self):
        super().__init__(repo_id="dreambank")


    def read_file(self, fname, reader=None, **kwargs):
        """Read a DreamBank HTML file.

        Parse DreamBank HTML info page for a given dataset into a dictionary.

        Parameters
        ----------
        dataset_id : str
            DreamBank info to load. Must be one of the available DreamBank datasets.

        Returns
        -------
        info : `dict`
            A `dict` with 3 with 3 columns.

            * ``short_name`` (`str`) - The dataset ID.
            * ``long_name`` (`str`) - The dataset title. A longer form of dataset ID.
            * ``n_dreams`` (`int`) - The total number of dreams in the dataset.
            * ``timeframe`` (`str`) - Provided year or timeframe of the dataset.
            * ``sex`` (`str`) - The provided sex of the dreamer.
            * ``description`` (`str`) - A long-form description of the dataset.
        """
        fp = self.pup.fetch(fname)
        if reader is not None:
            return reader(fp, **kwargs)
        with open(fp, "rb") as f:
            soup = BeautifulSoup(f, "html.parser", from_encoding="ISO-8859-1")
        if fname.endswith("dreams.html"):
            # Find all spans that do not have "comment" class labels.
            # Comments will already be present in the regular spans/dreams as bracketed content.
            data = []
            for span in soup.find_all("span", style=False, class_=lambda x: x != "comment"):
                span_text = span.get_text(separator=" ", strip=True)
                # Extract the dream number (and potentially date) from beginning of string
                match_ = re.match(r"^#(\S+) ((\(\S*\)) )?", span_text)
                assert match_ is not None, f"Did not find dream number match for dataset {dataset_id}, dream {dream_n}."
                dream_n = match_.group(1)  # The number of dream in the whole sequence
                dream_date = match_.group(3)  # will be None if not found
                # Remove the dream number (and potentially date) from the beginning of string
                dream_and_wc_text = re.sub(r"^#([0-9]+) ((\(\S*\)) )?", "", span_text)
                # Remove the word count from end of string
                n_wc_matches = len(re.findall(r"[ \n]?\([0-9]+ words\)$", dream_and_wc_text))
                assert n_wc_matches == 1, f"Found {n_wc_matches} WC match for dataset {dataset_id}, dream {dream_n} (expected 1)."
                dream_text = re.sub(r"[ \n]?\([0-9]+ words\)$", "", dream_and_wc_text)
                assert dream_n not in data, "Unexpected duplicate dream number"
                data.append(dict(n=dream_n, date=dream_date, dream=dream_text))
            # Make sure the correct number of dreams were extracted.
            # At the top of each page, DreamBank will say how many dreams are present in the
            # total dataset, as well as how many are displayed on the page. These, and the total
            # amount of dreams extracted, should all be the same.
            n_dreams_statement = soup.find("h4").find_next().get_text()
            n_dreams_total, n_dreams_displayed = re.findall(r"[0-9]+", n_dreams_statement)
            n_dreams_extracted = len(data)
            assert int(n_dreams_total) == int(n_dreams_displayed) == n_dreams_extracted
            dreams = pd.DataFrame(data).replace(dict(date={None: pd.NA})).astype(dict(n="string", date="string", dream="string")).dropna(how="all", axis=1).sort_index(axis=0)
            return dreams
        elif fname.endswith("info.html"):
            body = soup.find("body")
            long_name = body.find(string="Dream series:").next.get_text(strip=True)
            n_dreams = body.find(string="Number of dreams:").next.get_text(strip=True)
            timeframe = body.find(string="Year:").next.get_text(strip=True)
            sex = body.find(string="Sex of the dreamer(s):").next.get_text(strip=True)
            match_ = re.match(
                rf".*Sex of the dreamer\(s\): {sex}\n\n\n?(.*?)\s+(For the further analyses, click here.\n)?\[Back to search form\]\s+$",
                body.get_text(),
                flags=re.DOTALL
            )
            assert match_ is not None, f"Error parsing info description for dataset {dreambank_id}."
            description = match_.group(1)
            info = {
                "short_name": dreambank_id,
                "long_name": long_name,
                "n_dreams": n_dreams,
                "timeframe": timeframe,
                "sex": sex,
                "description": description,
            }
            return info


    def read_tidy(self, series_id, *, return_authors=True):
        dreams = self.read_file(f"{series_id}/dreams.html")
        authors = None
        return dreams, authors

