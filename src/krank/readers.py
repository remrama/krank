
import pandas as pd

from ._base import RepositoryManager, repo

import hashlib
import string


__all__ = [
    "read_aristides",
    "read_trump",
    "read_children",
    "read_demographic2010",
    "read_demographic2012",
    "read_demographic2013summer",
    "read_demographic2013winter",
    "read_krippner",
    "read_lucidjgb",
    "read_memorable",
    "read_miamihome",
    "read_miamilab",
    "read_obama",
    "read_online",
    "read_palliative",
    "read_pandemicapril",
    "read_research1",
    "read_research2",
    "read_scu1",
    "read_scu2",
    "read_sports",

    "read_bayaka",
    "read_hadza",
    "read_sad",
    "read_nightmare",
    "read_control",
]


def _author_old_to_new(author, last_idx=12):
    """
    Generates a unique id name
    refs:
    - md5: https://stackoverflow.com/questions/22974499/generate-id-from-string-in-python
    - sha3: https://stackoverflow.com/questions/47601592/safest-way-to-generate-a-unique-hash
    (- guid/uiid: https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python?noredirect=1&lq=1)
    """
    m = hashlib.md5()
    author_str = str(author).encode("utf-8")
    m.update(author_str)
    unique_digit_str = str(int(m.hexdigest(), 16))
    unique_letter_str = "".join(string.ascii_uppercase[int(x)] for x in unique_digit_str)
    return unique_letter_str[:last_idx]


###############################################################################
# Sleep and Dream Database
###############################################################################

@repo("SDDb")
def read_aristides():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Aristides")
    return df


@repo("SDDb")
def read_trump():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Trump")
    return df


@repo("SDDb")
def read_children():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Children")
    return df


@repo("SDDb")
def read_demographic2010():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Demographic2010")
    return df


@repo("SDDb")
def read_demographic2012():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Demographic2012")
    return df


@repo("SDDb")
def read_demographic2013summer():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Demographic2013Summer")
    return df


@repo("SDDb")
def read_demographic2013winter():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Demographic2013Winter")
    return df


@repo("SDDb")
def read_krippner():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Krippner")
    return df


@repo("SDDb")
def read_lucidjgb():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("LucidJGB")
    return df


@repo("SDDb")
def read_memorable():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Memorable")
    return df


@repo("SDDb")
def read_miamihome():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("MiamiHome")
    return df


@repo("SDDb")
def read_miamilab():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("MiamiLab")
    return df


@repo("SDDb")
def read_obama():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Obama")
    return df


@repo("SDDb")
def read_online():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Online")
    return df


@repo("SDDb")
def read_palliative():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Palliative")
    return df


@repo("SDDb")
def read_pandemicapril():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("PandemicApril")
    return df


@repo("SDDb")
def read_pandemicmay():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("PandemicMay")
    return df


@repo("SDDb")
def read_research1():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Research1")
    return df


@repo("SDDb")
def read_research2():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Research2")
    return df


@repo("SDDb")
def read_scu1():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("SCU1")
    return df


@repo("SDDb")
def read_scu2():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("SCU2")
    return df


@repo("SDDb")
def read_sports():
    sddb = RepositoryManager.get_repository()
    df = sddb.read_dataset("Sports")
    return df



###############################################################################
#
###############################################################################


@repo("Zhang2019")
def read_zhang():
    """Dreams from Zhang & Wamsley, 2019

    Steps

    * Parses sleep stage to an explicit column.
    * Converts Author IDs.
    * Converts Column names.
    * Removes redundant columns.
    """
    zhang2019 = RepositoryManager.get_repository()
    dreams, authors = zhang2019.read_tidy(return_authors=True)
    return dreams, authors
    # # authors = (df["Subject ID"]
    # #     .map(df["Subject ID"].cat.categories.tolist().index)
    # #     .map(lambda x: x+1).map("sub-{:03d}".format))
    # author_column = "Subject ID"
    # authors = df[author_column].map(_author_old_to_new).astype("string")
    # assert authors.nunique() == df[author_column].nunique()
    # # assert authors.cat.categories.nunique() == df["Subject ID"].cat.categories.nunique()
    # df.insert(0, "Author", pd.Categorical(authors))
    # df = df.drop(columns=[author_column, "Case ID", "Filename"])
    # df = df.rename(columns={"Text of Report": "Dream"})
    # return df

@repo("DreamBank")
def read_alta():
    dreambank = RepositoryManager.get_repository()
    dreams, authors = dreambank.read_tidy("alta")
    return dreams, authors


@repo("DreamBank")
def read_bosnak():
    dreambank = RepositoryManager.get_repository()
    dreambank = RepositoryManager.get_repository()
    dreams, authors = dreambank.read_tidy("bosnak")
    return dreams, authors


@repo("DreamBank")
def read_izzy():
    dreambank = DreamBank()
    dreams, authors = dreambank.read_tidy("izzy1")
    dreams, authors = dreambank.read_tidy("izzy2")
    izzy = pd.concat([izzy1, izzy2])
    return izzy



@repo("Samson2023")
def read_hadza():
    """Hadza dreams from Samson et al., 2023

    See Also
    --------
    read_control
    read_nightmares
    """
    samson2023 = RepositoryManager.get_repository()
    dreams, authors = samson2023.read_tidy()
    authors = authors.query("Population == 'Hadza'")
    dreams = dreams.loc[dreams["Dreamer"].isin(authors["Dreamer"])]
    return dreams, authors


@repo("Samson2023")
def read_bayaka():
    """
    See Also
    --------
    read_control
    read_nightmares
    """
    samson2023 = RepositoryManager.get_repository()
    dreams, authors = samson2023.read_tidy()
    authors = authors.query("Population == 'BaYaka'")
    dreams = dreams.loc[dreams["Dreamer"].isin(authors["Dreamer"])]
    return dreams, authors


@repo("Samson2023")
def read_sad():
    """
    See Also
    --------
    read_control
    read_nightmares
    """
    samson2023 = RepositoryManager.get_repository()
    dreams, authors = samson2023.read_tidy()
    authors = authors.query("Population == 'SAD'")
    dreams = dreams.loc[dreams["Dreamer"].isin(authors["Dreamer"])]
    return dreams, authors


@repo("Samson2023")
def read_nightmare():
    """
    See Also
    --------
    read_control
    read_nightmares
    """
    samson2023 = RepositoryManager.get_repository()
    dreams, authors = samson2023.read_tidy()
    authors = authors.query("Population == 'Nightmare'")
    dreams = dreams.loc[dreams["Dreamer"].isin(authors["Dreamer"])]
    return dreams, authors


@repo("Samson2023")
def read_control():
    """
    See Also
    --------
    read_control
    read_nightmares
    """
    samson2023 = RepositoryManager.get_repository()
    dreams, authors = samson2023.read_tidy()
    authors = authors.query("Population == 'Control'")
    dreams = dreams.loc[dreams["Dreamer"].isin(authors["Dreamer"])]
    return dreams, authors


@repo("Samson2023")
def read_students():
    """
    See Also
    --------
    read_control
    read_nightmares
    """
    samson2023 = RepositoryManager.get_repository()
    dreams, authors = samson2023.read_tidy()
    authors = authors.query("Population == 'Students'")
    dreams = dreams.loc[dreams["Dreamer"].isin(authors["Dreamer"])]
    return dreams, authors


@repo("Scala2024")
def read_scala2024():
    scala2024 = RepositoryManager.get_repository()
    df = scala2024.read_dreams()
    author_column = "author"
    authors = df[author_column].map(_author_old_to_new).astype("string")
    assert authors.nunique() == df[author_column].nunique()
    df.insert(0, "Author", pd.Categorical(authors))
    df = df.drop(columns=[author_column, "series_number", "is_control", "session_number", "number"])
    df = df.rename(columns={"dream": "Dream"})
    return df
