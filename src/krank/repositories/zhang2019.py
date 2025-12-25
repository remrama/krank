import zipfile
import pandas as pd

from ._base import KrankRepo


class Zhang2019(KrankRepo):
    """
    paper - https://doi.org/10.1111/psyp.13368
    dataset - https://doi.org/10.6084/m9.figshare.22226692
    metadata -
    Warning, this zip file is 1gb bc psg.
    # "Zhang & Wamsley 2019/Records.csv"
    # "Zhang & Wamsley 2019/ExperimentalDescription.txt"
    """
    def __init__(self, version=1):
        super().__init__(repo_id="zhang2019")

    def read_file(self, fname, reader=None, **kwargs):
        # "ExperimentalDescription.txt"
        # "Records.csv"
        # "Data/Reports.csv"
        fp = self.pup.fetch("Zhang & Wamsley 2019.zip")
        if reader is not None:
            return reader(fp, **kwargs)
        with zipfile.ZipFile(fp) as zf:
            archive_fname = f"Zhang & Wamsley 2019/{fname}"
            with zf.open(archive_fname, "r") as f:
                if fname.endswith(".txt"):
                    return f.read().decode("utf-8")
                elif fname.endswith(".csv"):
                    return pd.read_csv(f, **kwargs)

    def read_tidy(self, *, return_authors=False):
        report_columns = {
            "Subject ID": "int",
            "Case ID": "string",
            "Filename": "string",
            "Text of Report": "string",
        }
        # Leaving out three empty columns
        # "Treatment group", "Proportion artifacts", "Remarks"
        records_columns = {
            "Filename": "string",
            "Case ID": "string",
            "Subject ID": "int",
            "Experience": "bool",  # 0=False, 1=True, see ExperimentalDescription.txt
            "Duration": "int",
            "EEG sample rate": "int",
            "Number of EEG channels": "int",
            "Last sleep stage": "int",
            "Has EOG": "bool",
            "Has EMG": "bool",
            "Has ECG": "bool",
            "Time of awakening": "string",
            "Subject age": "int",
            "Subject sex": "bool",
            "Subject healthy": "bool",
            "Has more data": "bool"
        }
        reports = self.read_file("Data/Reports.csv", dtype=report_columns)
        records = self.read_file("Records.csv", usecols=list(records_columns)).astype(records_columns)
        # records = records.dropna(how="all", axis=1)
        df = records.merge(reports, on=["Subject ID", "Case ID", "Filename"], how="left", validate="1:1")
        # Subject ID is present in 3 places.
        # Ensure there are no conflicts.
        # subject_from_case = df["Case ID"].str.split("_").str[0].astype("str")
        from_case = df["Case ID"].str.extract(r"^(?P<subject>[0-9]+)_(?P<stage>[A-Za-z]+)[0-9]*$")
        from_fname = df["Filename"].str.extract(r"^subject0?(?P<subject>[0-9]+)_(?P<stage>[A-Za-z]+)[0-9]*(?=\.edf$)")
        assert df["Subject ID"].astype("string").eq(from_case["subject"]).all()
        assert df["Subject ID"].astype("string").eq(from_fname["subject"]).all()
        assert from_case["stage"].eq(from_fname["stage"]).all()
        df.insert(1, "StageAttempt", from_case["stage"])
        # Replace last stage values with strings and make categorical
        last_stage_values = {0: "WAKE", 1: "N1", 2: "N2", 3: "N3", 5: "REM"}
        df["Last sleep stage"] = df["Last sleep stage"].replace(last_stage_values)
        sex_values = {False: "male", True: "female"}
        df["Subject sex"] = df["Subject sex"].replace(sex_values)
        df["Subject ID"] = df["Subject ID"].map("sub-{}".format)
        df = df.drop(columns=
            [
                "Filename",  # redundant
                "Case ID",  # redundant
                "Duration",  # constant
                "EEG sample rate",  # constant
                "Number of EEG channels",  # constant
                "Has EOG",  # constant
                "Has EMG",  # constant
                "Has ECG",  # constant
                "Subject healthy",  # constant
                "Has more data",  # constant
            ]
        )
        df = df.rename(columns=
            {
                "Subject ID": "Dreamer",
                "Last sleep stage": "StageScored",
                "Time of awakening": "Time",
                "Subject age": "Age",
                "Subject sex": "Sex",
                "Text of Report": "Dream",
            }
        )
        # Set categorical columns
        df["Dreamer"] = pd.Categorical(df["Dreamer"].astype("string"), ordered=False)
        df["StageScored"] = pd.Categorical(df["StageScored"].astype("string"), ordered=False)
        df["StageAttempt"] = pd.Categorical(df["StageAttempt"].astype("string"), ordered=False)
        df["Sex"] = pd.Categorical(df["Sex"].astype("string"), ordered=False)
        authors = df[["Dreamer", "Age", "Sex"]].drop_duplicates().reset_index(drop=True)
        dreams = df.drop(columns=["Age", "Sex"])
        dreams = dreams[["Dreamer", "Time", "StageAttempt", "StageScored", "Experience", "Dream"]].copy()
        if return_authors:
            return dreams, authors
        return dreams
