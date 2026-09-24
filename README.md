# radmap — Spatiotemporally Corrected Radiological Contamination Mapping Platform

Reproducibility repository for:

> **A Spatiotemporally Corrected Radiological Contamination Mapping Platform for Multi-Scenario Nuclear and Radiological Emergencies**
> Hyunsung Kim, Myeongsik Shin, Ku Kang. *Journal of Environmental Radioactivity* (JENVRAD-D-26-00618).

This repository archives the analysis code, processed datasets, reconstructed dose-rate grids,
configuration files, and random seeds supporting the study. It is released under **CC-BY-4.0**.

## What this study does
Five spatial interpolation methods — inverse distance weighting (IDW), ordinary kriging (OK),
universal kriging (UK), anisotropic OK (Aniso_OK), and thin-plate spline (TPS) — are compared for
2-D dose-rate field reconstruction under two scenarios: a 2,000 kT nuclear surface burst
(HotSpot 3.1.2) and the Fukushima Daiichi NPP accident (JAEA airborne surveys, 2011–2025).
The pipeline also covers altitude correction (AGCF/SBPL), scenario-dependent temporal normalization,
spatial block cross-validation, anisotropy-ratio sensitivity, directional variograms, and an
operational decision-quality evaluation (hazard-zone IoU, false-negative area, boundary
displacement, minimum-dose route regret).

## Repository structure
```
radmap/
├── README.md
├── LICENSE                 # CC-BY-4.0
├── CITATION.cff
├── requirements.txt        # Python dependencies (pin your exact versions)
├── src/                    # analysis code  (add your scripts here)
├── config/                 # variogram/method parameters and random seeds
├── data/                   # processed inputs; raw JAEA data via EMDB link (see data/README.md)
└── results/                # reconstructed grids and metric outputs (summaries included)
```

## Reproducing the results
1. Create the environment: `pip install -r requirements.txt` (Python 3).
2. Obtain the input data (see `data/README.md`): JAEA airborne survey products from EMDB and the
   HotSpot 3.1.2 detonation output.
3. Run the pipeline scripts in `src/` with the configuration and seeds in `config/`.
   The reported metrics are summarised in `results/` (spatial block-CV, operational validation,
   anisotropy sensitivity).

## Data availability
- **HotSpot detonation reference field:** generated with HotSpot Health Physics Codes v3.1.2.
- **Fukushima airborne survey data:** publicly available from the JAEA Database for Radioactive
  Substance Monitoring Data (EMDB): https://radioactivity.nra.go.jp/emdb/ — used in accordance with
  its original licence. Raw JAEA data are linked to their official source rather than redistributed here.

## Methods / libraries
Interpolation and geostatistics in Python 3 (e.g., `pykrige` for OK/UK/anisotropic kriging,
`scipy` `RBFInterpolator` for TPS, `numpy`/`pandas` for data handling, `matplotlib` for figures).
Pin the exact versions you used in `requirements.txt` for full reproducibility.

## License
This work is licensed under a Creative Commons Attribution 4.0 International License (CC-BY-4.0).
See `LICENSE`.

## Citation
See `CITATION.cff`. Please cite the paper above when using this repository.
