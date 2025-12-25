
import krank
import pandas as pd
from tqdm import tqdm


# datasets = [x.split("_")[1] for x in krank.readers.__all__]
datasets = [
    "bayaka",
    "children",
    "control",
    "demographic2010",
    "demographic2012",
    "demographic2013summer",
    "demographic2013winter",
    "hadza",
    "krippner",
    "lucidjgb",
    "memorable",
    "miamihome",
    "miamilab",
    "nightmare",
    "obama",
    "online",
    "palliative",
    "pandemicapril",
    "research1",
    "research2",
    "sad",
    "scu1",
    "scu2",
    "sports",
    "trump",
]


 # dreams, authors = zip(*[krank.read(d) for d in datasets[:3]])
dreams_list = []
authors_list = []
for d in (pbar := tqdm(datasets)):
    pbar.set_description(f"Reading {d}")
    dreams, authors = krank.read(d)
    dreams_list.append(dreams)
    authors_list.append(authors)


dreams = pd.concat(dreams_list, axis=0)
dreamers = pd.concat(authors_list, axis=0)



import unicodedata


def check_df(df):
    assert df.columns.upper()
    assert df.columns[0] == "Author"
    assert df.columns[-1] == "Dream"
    assert not df["Author"].isna().any()
    assert not df["Dream"].isna().any()
    assert df["Author"].str.len().gt(0).all()
    assert df["Dream"].str.len().gt(0).all()
    assert df["Author"].dtype.name == "category"
    assert df["Dream"].dtype.name == "string"
    assert df["Author"].dtype.categories.dtype.name == "string"
    assert df.dtypes.map(lambda x: x.name).ne("object").all()


def remove_na(df):
    return df.dropna(how="any", axis=0)
    
# def remove_outer_quotes():
#     pattern = r"^(?:[\'\"])(.*?)(?:[\'\"])$"
#     dreams_clean.str.extract(pattern, expand=False).combine_first(dreams_clean)

def clean_dreams(dreams):
    replacements = {
        r"[\u201C\u201D]": '"',  # Double quotes
        r"[\u2018\u2019]": "'",  # Single quotes
        r"[\u2013]": "—",        # En dash to em dash
        r"[\u2014]": "—",        # Em dash
        r"[\u2212]": "-",        # Minus sign to hyphen-minus
        r"[\u2010\u002d]": "-",  # Various hyphens to hyphen-minus
        r"[\u00A0]": " ",        # Non-breaking space to space
        r"[\u200B]": " ",        # Zero width space to space
        r"[\u2026]": "...",      # Ellipsis
    }
    dreams_clean = (dreams
        .str.strip()
        .replace(replacements, regex=True)
        .str.replace("''", '"')
        .map(lambda x: unicodedata.normalize("NFC", x))
        .replace("", pd.NA, regex=False)
    )
    return dreams_clean



