# Analysis code (`radmap` package)

Importable package under `src/radmap/` implementing the study pipeline:

| Module | Contents |
|---|---|
| `interpolation.py` | IDW, ordinary/universal kriging (PyKrige), anisotropic OK, TPS (SciPy RBF); all in log10 space; kriging predictions clamped to the training range |
| `metrics.py` | R^2, **log10-RMSE** (principal criterion), MAPE, median absolute log-error (MedALE) |
| `cross_validation.py` | random k-fold and **spatial block** (contiguous-region) k-fold; parameters re-fit on training only |
| `directional_variogram.py` | data-driven anisotropy ratio & principal-axis estimation; method-selection rule |
| `agcf_sbpl.py` | segmented broken power-law fit to FM 3-3-1 Table 5-3 (AGCF(150 m)=8.2) |
| `temporal_normalization.py` | half-life decay (accident) and Way-Wigner/Kaufmann t^-n (detonation) |
| `operational_metrics.py` | hazard-zone IoU, false-negative/false-positive area, boundary displacement, route regret (Dijkstra) |
| `synthetic_benchmark.py` | controlled anisotropic GRF benchmark across ratios {2,5,10,20} (paper Fig. 7) |

Run from the repo root:
```
pip install -r requirements.txt
python scripts/smoke_test.py                 # module self-test (AGCF, decay, metrics)
python scripts/run_anisotropy_benchmark.py   # -> results/synth_anisotropy_CV_reproduced.csv
```
The Fukushima and HotSpot analyses use these same modules on the input data placed
under `data/` (see `data/README.md`); wire them together per `config/params.yaml`.
