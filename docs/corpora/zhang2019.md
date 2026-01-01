# zhang2019

This corpus contains dream reports collected from participants in a laboratory polysomnography study conducted by Zhang and Wamsley and published in 2019. The dreams were collected using the serial awakening method, where participants were awakened during different sleep stages to report their dreams. The dataset includes various metadata about the participants and the sleep conditions.

## Overview

| Field | Value |
|------:|:------|
| **Title** | Zhang & Wamsley, 2019 |
| **DOI** | [10.5281/zenodo.18050635](https://doi.org/10.5281/zenodo.18050635) |
| **Environment** | lab |
| **Probe** | serial awakening |
| **_N_ reports** | 308 |
| **_N_ authors** | 28 |
| **_M_ report length** | 46 words |
| **_Mdn_ report length** | 31 words |

## Citation

- Zhang, J., & Wamsley, E. J. (2019). EEG predictors of dreaming outside of REM sleep. Psychophysiology, 56(7), e13368. [https://doi.org/10.1111/psyp.13368](https://doi.org/10.1111/psyp.13368)

- Wong, W., Herzog, R., Andrade, K. C., Andrillon, T., De Araujo, D. B., Arnulf, I., ... & Tsuchiya, N. (2025). A dream EEG and mentation database. Nature Communications, 16(1), 7495. [https://doi.org/10.1038/s41467-025-61945-1](https://doi.org/10.1038/s41467-025-61945-1)


## Columns

### Reports

| Column | Description |
|-------:|:------------|
| `author` | Unique author identifier |
| `report` | Text of dream report |
| `time` | Time of awakening for dream report |
| `stage_intended` | Sleep stage the experimenter intended to awaken the participant from |
| `stage_actual` | Sleep stage the participant was actually in when awakened |
| `experience` | True if the report contains any conscious experience, otherwise False |

### Authors

| Column | Description |
|-------:|:------------|
| `author` | Unique author identifier |
| `age` | Reported age of author at time of report |
| `sex` | Reported sex of author at time of report |

## Source

- **Processing code**: [Notebook](http://github.com/remrama/krank/blob/main/sources/zhang2019/prepare.ipynb)
- **Processed file**: [Zenodo](https://doi.org/10.5281/zenodo.18050635)

## Version History

| Version | Hash | DOI |
|:-------:|:----:|:---:|
| 1 (latest) | `md5:a61a3c56f4ee8c14e4a6466044df88f8` | [`10.5281/zenodo.18050635`](https://doi.org/10.5281/zenodo.18050635) |
