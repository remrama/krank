# krank

Steal sleep and dreams from other researchers.

Uses [Pooch](https://www.fatiando.org/pooch) for simple and reliable downloading. Similar to [Ensaio](https://www.fatiando.org/ensaio) but for sleep.


```python
import krank
import yasa

raw, hypno = krank.fetch_dreemh(subject=8)

sf = raw.info["sfreq"]
data = raw.get_data(picks="F3_F4", units="uV")[0]

hypno_up = yasa.hypno_upsample_to_data(hypno, 1/30, data, sf)
fig = yasa.plot_spectrogram(data, sf, hypno_up, cmap="Spectral_r")
```


## Development

To make a new dataset available through Krank:
1. Download the dataset locally.
2. Use Pooch to create a registry file.
3. Add the dataset metadata.
4. Add a function to the `krank.fetch` module (follow docstring guidelines closely, as they are used to generate docs site).


## Metadata format

BIDS-based json descriptor. Select from the following keywords: [`overnight`, `nap`, `dreams`, `hypnograms`, `multiple raters`, `HD-EEG`, `EEG`, `PSG`]
