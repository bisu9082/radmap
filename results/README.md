# Results

- `synth_anisotropy_CV.csv` — **archived results as reported** (basis of Fig. 7):
  anisotropy-ratio sensitivity, random vs spatial block CV, per method.
- `synth_anisotropy_CV_reproduced.csv` — output of
  `scripts/run_anisotropy_benchmark.py`. It reproduces the **qualitative pattern**
  of the archived results (anisotropy-aware Aniso_OK/TPS remain robust while
  isotropic OK and IDW degrade as anisotropy increases); exact values differ
  because each run draws a fresh synthetic Gaussian-random-field realization.
- `spatial_blockCV_summary.md` — random vs spatial block CV (HotSpot; Fukushima 2011/2020).
- `operational_validation.md` — zoning accuracy and route-regret vs the HotSpot reference field.
- `g3_remaining.md` — directional-perturbation sensitivity, realistic survey geometry, metric alternatives.

Add the full reconstructed dose-rate grids (e.g. `.npy`/`.csv`/GeoTIFF) here for
the Fukushima and HotSpot case studies.
