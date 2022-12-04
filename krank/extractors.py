"""Loading raw dataset files in standardized ways.
EEG data as mne.Raw objects.
Hypnograms as YASA Hypnogram classes
Dream reports as strings?
BIDS-ish naming schemes.

These are called within fetching module so not needed by user.
"""

from pathlib import Path

import h5py
import mne
import numpy as np


def extract_raw_dreemh(path, downsample=True) -> (mne.io.Raw, np.ndarray):
    """Load a single subject of already-downloaded data.
    # Dreem hd5 files have 3 key, attributes pairs. 'events', 'hypnogram', 'signals'
    """
    assert isinstance(path, (str, Path))

    path = Path(path)
    assert path.is_file() and path.suffix == ".h5"

    # Construct EEG info from published metadata.
    channels = {
        "ECG": "emg",
        "EMG": "emg",
        "EOG1": "eog",
        "EOG2": "eog",
        "C3_M2": "eeg",
        "F3_F4": "eeg",
        "F3_M2": "eeg",
        "F3_O1": "eeg",
        "F4_M1": "eeg",
        "F4_O2": "eeg",
        "FP1_F3": "eeg",
        "FP1_M2": "eeg",
        "FP1_O1": "eeg",
        "FP2_F4": "eeg",
        "FP2_M1": "eeg",
        "FP2_O2": "eeg",
    }
    n_channels = len(channels)
    sampling_freq = 200  # in Hertz
    description = "DREEM dataset is..."
    montage = None
    ch_names = list(channels)
    ch_names, ch_types = zip(*channels.items())
    info = mne.create_info(ch_names, ch_types=ch_types, sfreq=sampling_freq)
    info.set_montage(montage)
    info["description"] = description
    # info["bads"] = ["01"]  # Names of bad channels

    with h5py.File(path, "r") as f:

        # Extract the human-scored hypnogram.
        hypno = f["hypnogram"][()]  # () = as array

        # Extract all PSG data.
        signal_arrays = []
        for name_, type_ in channels.items():
            signal = f["signals"][type_][name_][()]
            signal_arrays.append(signal)
        data = np.row_stack(signal_arrays)

    raw = mne.io.RawArray(data, info)
    if downsample and sampling_freq > 100:
        raw.resample(100)

    return raw, hypno
