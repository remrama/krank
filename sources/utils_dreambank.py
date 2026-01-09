"""Utility functions for preparing DreamBank corpora."""

import os
import re
import tarfile

import pandas as pd
import pooch
from bs4 import BeautifulSoup
from tqdm import tqdm

__all__ = [
    "extract_file_content",
    "list_available_datasets",
    "parse_dreams",
    "parse_info",
    "parse_moreinfo",
    "read_dreambank",
    "retrieve_archive",
]

_HTML_ENCODING = "ISO-8859-1"
_CACHE_DIR = pooch.os_cache("pooch").joinpath("dreambank")
_REGISTRY = {
    "v2": {
        "url": "https://zenodo.org/records/18159468/files/dreambank.tar.xz?download=1",
        "hash": "md5:eb83bcb0828f9c8c248a5052b2ffc798",
    },
    "v1": {
        "url": "https://zenodo.org/records/18131750/files/dreambank.tar.xz?download=1",
        "hash": "md5:6ab629e9c13251d228db7ec1a93ffeb6",
    },
}


def extract_file_content(version: str, dataset: str, component: str) -> bytes:
    """Extracts the info.html, dreams.html, or moreinfo.html content for a given dataset from the archive."""
    assert component in {"dreams", "info", "moreinfo"}, (
        f"Invalid component: {component}"
    )
    fname = f"./{dataset}/{component}.html"
    archive_fname = retrieve_archive(version)
    with tarfile.open(archive_fname, "r:xz") as tar:
        with tar.extractfile(fname) as f:
            content = f.read()
    return content


def parse_dreams(
    version: str,
    dataset_id: str,
    as_dataframe: bool = False,
) -> list[dict[str, any]]:
    """Parse DreamBank HTML dreams page for a given dataset.

    * Every dream starts with a #-padded number (e.g., #1) followed by a space.
        It's not always just numbers. Sometimes it has letters (e.g., #111a) or dashes
        (e.g., #B-055 in Jasmine's dreams; I think this is because it's in the Jasmine-all
        dataset and the B-055 indicates it's from her "B" series).
    * Dreams may optionally have a parenthetical between the number and the dream text.
        This parenthetical may contain a date, title, age, or other information.
        There is no standard format for what is in here and it will vary by dataset.
        It's surrounding by single spaces. There might be parenthesis inside the parenthetical.
    * The dream text follows.
    * Every dream ends with a word count in parentheses (e.g., (123 words)).
    * Every dream starts with a number sign (#) followed by the dream number in the whole sequence.
        This is not necessarily a pure integer, as some dreams have letter suffixes (e.g., 111a).
        This is not alway a full range of row numbers. E.g., HVdC datasets go up to 500, but
        there are some missing dreams. The missing numbers are between 1-500.
        Sometimes it has strings in it, e.g., #F21-5 in Peruvian dreams.
        Sometimes it has sex and age in it, e.g., #89 (F, age 18) in West Coast dreams.
        There are sometimes sup-parantheticals within the main parenthetical, but fortunatelly
        they are always at the end of the main parenthetical (e.g., #1027 (2007-01-22 (15))),
        which makes them easier to find.
    * Dreams may optionally have a date in parentheses after the dream number.
        The date, if present, can be in a variety of formats, sometimes separated by slashes or dashes.
        Also a question mark is there sometimes to indicate uncertainty (e.g., 1985?).
        There is sometimes another value in a sub-parenthetical within the date.
        E.g., a number that I think represents age in Izzy's dreams (e.g., #1027 (2007-01-22 (15)),
        or a period title in Madeline's dreams (e.g., #0771 (2003-19-12 (Post-Grad))).
    * Some dreams have a title following the date, in brackets and quotes (e.g., ["Outlaws Hiding"]).
        I've seen this in some Barb Sanders dreams.
    * Barbara baseline always ends with [BL] at end of report.
    """
    content = extract_file_content(version, dataset_id, "dreams")
    soup = BeautifulSoup(content, "html.parser", from_encoding=_HTML_ENCODING)
    # Find all spans that do not have "comment" class labels.
    # Comments will already be present in the regular spans/dreams as bracketed content.
    dreams = []
    dream_spans = soup.find_all("span", style=False, class_=lambda x: x != "comment")
    for span in dream_spans:
        span_text = span.get_text(separator=" ", strip=True)
        # Extract the dream number (and potentially date) from beginning of string
        # Sometimes dream number is a string, like 111a (e.g., Alta)
        # Date is sometimes present if provided by dreamer
        # Dream ID is always present and represents the number of the dream in the whole sequence
        # PREFACE_PATTERN = r"^#(?P<dream_id>\S+) (?P<metadata>\(.+?\){1,2} )?"
        PREFACE_PATTERN = r"^#(?P<dream_id>\S+) (\((?P<metadata>.{1,30}?)\) )?"
        preface_match = re.match(PREFACE_PATTERN, span_text)
        assert preface_match is not None, (
            f"Error parsing dream preface for dataset {dataset_id}, span text: {span_text}"
        )
        # There is always _supposed_ to be a space bewteen last word and word count paranthetical,
        # but this isn't always the case. Eg, alta #49, bay_area_girls_456 #219-11.
        # It's always supposed to be a return line before the word count paranthetical,
        # but looks like it is also a space sometimes, particularly when there is a bracketed
        # statement right before it (e.g., [BL] (87 words)).
        # So instead of a newline preceding, we will just look for any whitespace _optionally_.
        PROLOGUE_PATTERN = r"(\s+)?\((?P<word_count>[0-9]+) words\)$"
        prologue_match = re.search(PROLOGUE_PATTERN, span_text)
        # prologue_match = re.search(PROLOGUE_PATTERN, span_text)
        assert prologue_match is not None, (
            f"Error parsing dream prologue for dataset {dataset_id}, span text: {span_text}"
        )
        # n_wc_matches = len(re.findall(r"[ \n]?\([0-9]+ words\)$", dream_and_wc_text))

        # Extract the id_match from the span text
        # dream_n = match_.group(1)  # The number of dream in the whole sequence
        # dream_date = match_.group(3)  # will be None if not found
        # # Remove the dream number (and potentially date) from the beginning of string
        # dream_and_wc_text = re.sub(r"^#([0-9]+) ((\(\S*\)) )?", "", span_text)
        # # Remove the word count from end of string
        # n_wc_matches = len(re.findall(r"[ \n]?\([0-9]+ words\)$", dream_and_wc_text))
        # assert n_wc_matches == 1, f"Found {n_wc_matches} WC match for dataset {dataset}, dream {dream_n} (expected 1)."
        # dream_text = re.sub(r"[ \n]?\([0-9]+ words\)$", "", dream_and_wc_text)
        # assert dream_n not in data, f"Unexpected duplicate dream number: {dream_n} in dataset {dataset}."

        # Remove extracted preface and prologue from span text to get dream text
        dreams.append(
            {
                "dataset_id": dataset_id,
                "dream_id": preface_match.group("dream_id"),
                "metadata": pd.NA
                if preface_match.group("metadata") is None
                else preface_match.group("metadata"),
                "word_count": int(prologue_match.group("word_count")),
                "dream_text": re.sub(
                    PROLOGUE_PATTERN, "", re.sub(PREFACE_PATTERN, "", span_text)
                ),
            }
        )
    # Make sure the correct number of dreams were extracted.
    # At the top of each page, DreamBank will say how many dreams are present in the
    # total dataset, as well as how many are displayed on the page. These, and the total
    # amount of dreams extracted, should all be the same.
    n_dreams_statement = soup.find("h4").find_next().get_text()
    n_dreams_total, n_dreams_displayed = map(
        int, re.findall(r"[0-9]+", n_dreams_statement)
    )
    n_dreams_extracted = len(dreams)
    assert n_dreams_total == n_dreams_displayed == n_dreams_extracted
    if as_dataframe:
        dreams = pd.DataFrame.from_records(dreams)
    return dreams


def parse_info(
    version: str,
    dataset_id: str,
    process_description: bool = True,
) -> dict[str, any]:
    """Parse DreamBank HTML info page for a given dataset into a dictionary.

    This is the little window that pops up if you hit "MORE INFO" on the dataset search page.
    The free text is same as what is on the Grid page, but the structured fields are not there.
    The structured fields are also present in moreinfo page.
    ```
    Dream series: Alta: a detailed dreamer
    Number of dreams: 422
    Year: 1985-1997
    Sex of the dreamer(s): female

    Alta is an adult woman who wrote down her dreams in the late 1980s and early 1990s, and added a few in 1997 when she called to offer the dreams to us. This series has not been heavily studied yet.
    ```
    * long_name (str): The dataset title.
    * n_dreams (int): The total number of dreams in the dataset.
    * timeframe (str): Provided year or timeframe of the dataset.
    * sex (str): The provided sex of the dreamer.
    * description (str): A long-form description of the dataset.

    Notes
    -----
    The more info (extended descriptions) are often very detailed with extensive HTML formatting.
    So for now I'm leaving them out. Best way to view them honestly is just to go to the link.
    And the link is the same for everyone so including the link in the dataset CSV is redundant.
    But for now a half solution is to add a column that clarifies if there is more info available online.

    Not every dataset has more info, but they all have a more info _page_. It just
    might say no more info is available.

    This is the little window that pops up whenever you hit "click here" in the initial
    info page. I think it only applies to dream series??
    The structured fields are duplicated here, but the free text from info is different than here.
    That's like a brief description and this is a detailed thing, sometimes with extensive character
    info and tables and stuff.
    Not everyone has a direct link to this page, but if they have no more info and you go
    directly to the link it will still have the structured fields, just say
    "Sorry, no additional info is available for this series."

    """
    content = extract_file_content(version, dataset_id, "info")
    soup = BeautifulSoup(content, "html.parser", from_encoding=_HTML_ENCODING)
    body = soup.find("body")
    name = body.find(string="Dream series:").next.get_text(strip=True)
    n_dreams = body.find(string="Number of dreams:").next.get_text(strip=True)
    timeframe = body.find(string="Year:").next.get_text(strip=True)
    sex = body.find(string="Sex of the dreamer(s):").next.get_text(strip=True)
    BODY_RE = r"^.*Sex of the dreamer\(s\): (?:fe)?male\n\n\n?(?P<body>.*?)\s+(For the further analyses, click here.\n)?\[Back to search form\]\s+$"
    body_match = re.fullmatch(BODY_RE, body.get_text(), flags=re.DOTALL)
    assert body_match is not None, f"Error parsing info for dataset {dataset_id}"
    body_text = body_match.group("body")
    if process_description:
        # Clean up whitespace in description.
        body_text = re.sub(r"\s+", " ", body_text)
        # Optionally replace click here with markdown style link to url.
        # url = f"https://dreambank.net/more_info.cgi?further=1&series={dataset}"
    info = {
        "dataset_id": dataset_id,
        "name": re.sub(
            r"\s+", " ", name
        ),  # remove extra spaces in long name (e.g., "Izzy,  age 14")
        "timeframe": timeframe,
        "sex": sex,
        "n_dreams": int(n_dreams),
        "description": body_text,
    }
    return info


def parse_moreinfo(version: str, dataset_id: str) -> dict[str, any]:
    # Just like the info page, we need to extract the description from the rest of the text.
    # The search pattern is very similar, with just a slight difference in the trailing text.
    content = extract_file_content(version, dataset_id, "moreinfo")
    soup = BeautifulSoup(content, "html.parser", from_encoding=_HTML_ENCODING)
    body = soup.find("body")
    # Parse header details
    name = body.find(string="Dream series:").next.get_text(strip=True)
    n_dreams = body.find(string="Number of dreams:").next.get_text(strip=True)
    timeframe = body.find(string="Year:").next.get_text(strip=True)
    sex = body.find(string="Sex of the dreamer(s):").next.get_text(strip=True)
    # Parse extended description
    BODY_RE = r"^.*Sex of the dreamer\(s\): (?:fe)?male\n\n\n?(?P<body>.*?)\s+$"
    body_match = re.fullmatch(BODY_RE, body.get_text(), flags=re.DOTALL)
    assert body_match is not None, f"Error parsing moreinfo for dataset {dataset_id}."
    body_ = body_match.group("body")
    moreinfo_available = (
        body_ != "Sorry, no additional info is available for this series."
    )
    moreinfo = {
        "dataset_id": dataset_id,
        "name": re.sub(
            r"\s+", " ", name
        ),  # remove extra spaces in long name (e.g., "Izzy,  age 14")
        "sex": sex,
        "timeframe": timeframe,
        "n_dreams": int(n_dreams),
        "moreinfo": body_,
        "moreinfo_available": moreinfo_available,
    }
    return moreinfo


def list_available_datasets(
    version: str,
    english_only: bool = False,
    verbose: bool = True,
) -> list[str]:
    """Get a list of all available datasets in the DreamBank archive."""
    fname = retrieve_archive(version)
    datasets = []
    with tarfile.open(fname, "r:xz") as tar:
        for member in tar.getmembers():
            if member.isdir() and member.name != ".":
                datasets.append(os.path.basename(member.name))
    if english_only:
        # Drop non-english datasets.
        for ds in datasets[:]:
            if "." in ds:
                datasets.remove(ds)
                if verbose:
                    print(f"Dropping non-English dataset: {ds}")
    return sorted(datasets)


def read_dreambank(
    version: str,
    dataset_ids: list[str] | None = None,
    english_only: bool = False,
    verbose: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Main function to extract all datasets and dreams from DreamBank archive."""
    if dataset_ids is None:
        dataset_ids = list_available_datasets(version, english_only=english_only, verbose=verbose)
    all_info = []
    all_dreams = []
    all_moreinfo = []
    iterator = tqdm(dataset_ids, ncols=90) if verbose else dataset_ids
    for dataset in iterator:
        if verbose:
            iterator.set_description(f"Processing dataset {dataset}")
        info = parse_info(version, dataset)
        dreams = parse_dreams(version, dataset)
        moreinfo = parse_moreinfo(version, dataset)
        for k in set(info.keys()).intersection(set(moreinfo.keys())):
            assert info[k] == moreinfo[k], f"{k} mismatch in dataset {dataset}"
        all_info.append(info)
        all_dreams.extend(dreams)
        all_moreinfo.append(moreinfo)
    datasets = pd.DataFrame.from_records(all_info)
    dreams = pd.DataFrame.from_records(all_dreams)
    moreinfo = pd.DataFrame.from_records(all_moreinfo)
    datasets = datasets.merge(
        moreinfo[["name", "moreinfo_available"]], on="name", how="left"
    )
    # There will be a lot of duplicates because some dreams are subsets of others.
    # But there shouldn't be any duplicates within datasets.
    assert not dreams.duplicated().any()
    assert not dreams.duplicated(subset=["dataset_id", "dream_id"]).any()
    assert not dreams.drop(columns=["metadata"]).isna().any(axis=None)
    assert not datasets.isna().any(axis=None)
    assert not datasets.duplicated().any()
    assert datasets["dataset_id"].is_unique
    return datasets, dreams


def retrieve_archive(version: str, **kwargs) -> str:
    """Retrieve the DreamBank archive file using pooch."""
    assert version in _REGISTRY, f"Invalid DreamBank version: {version}"
    url = _REGISTRY[version]["url"]
    known_hash = _REGISTRY[version]["hash"]
    kwargs.setdefault("path", _CACHE_DIR)
    kwargs.setdefault("progressbar", True)
    fname = pooch.retrieve(url, known_hash, **kwargs)
    return fname
