"""Functions for fetching individual subjects from individual datasets.
"""

import pkgutil

import pooch

from krank.extractors import *


def _set_data_dir(path: str) -> None:
    """Set the KRANK_DATA_DIR environment variable.
    
    Setting a KRANK_DATA_DIR environment variable will override the default
    download location. If not set, Pooch uses a cache folder that can be
    viewed with :py:func:`pooch.os_cache` or the `abspath` or `path` attribute of a
    :py:func:`pooch.Pooch` instance.
    """
    path = Path(path)
    assert path.is_dir()
    os.environ["KRANK_DATA_DIR"] = str(path.absolute())


def _get_fetcher(dataset: str) -> pooch.Pooch:
    """Return a :py:class:`pooch.Pooch` instance for a specific dataset."""
    from krank import __version__

    if dataset == "dreemh":
        # Link to remote data, will download if not present locally.
        base_url = "https://dreem-dod-h.s3.eu-west-3.amazonaws.com/"
        registry = {
            "095d6e40-5f19-55b6-a0ec-6e0ad3793da0.h5": "a5eb768eacb44aa07cbd0857623dc2d65ca9b9672d778fa15e0c1517a18bb27a",
        }
        # # Get registry file from package_data
        # registry_file = pkgutil.get_data(__name__, "registries/dreemh.txt")

    # Fetcher
    POOCH = pooch.create(
        # Use the default cache folder for the operating system
        path=pooch.os_cache("krank"),
        base_url=base_url,
        version=__version__,
        # If this is a development version, get the data from the "main" branch
        # version_dev="main",
        registry=registry,
        # The name of an environment variable that can overwrite the path
        env="KRANK_DATA_DIR",
    )
    # # Load this registry file
    # POOCH.load_registry(registry_file)

    return POOCH


def fetch_dreemh(subject: int) -> (mne.io.Raw, np.ndarray):
    """
    # The file will be downloaded automatically the first time this is run

    # returns the file path to the downloaded file. Afterwards, Pooch finds
    # it in the local cache and doesn't repeat the download.
    # The "fetch" method returns the full path to the downloaded data file.
    # All we need to do now is load it with our standard Python tools.
    """
    # Validate input.
    assert isinstance(subject, int)
    
    # Get list of subject filenames for this dataset.
    fetcher = _get_fetcher("dreemh")
    n_subjects = len(fetcher.registry_files)
    assert 0 <= subject < n_subjects

    # Get path to file and download it if not present.
    name = fetcher.registry_files[subject]
    path = fetcher.fetch(name, progressbar=True)

    # Turn the raw file into something good.
    raw, hypno = extract_raw_dreemh(path)
    return raw, hypno
