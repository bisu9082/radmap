# Analysis code

Add the study scripts here. Suggested organisation (rename to match your originals):
- `interpolation.py`      — IDW, OK, UK, anisotropic OK (pykrige), TPS (scipy RBFInterpolator)
- `spatial_block_cv.py`   — contiguous-region (spatial block) 5-fold CV; parameters re-estimated on training only
- `anisotropy_sensitivity.py` — synthetic anisotropy-ratio benchmark (ratios 2/5/10/20)
- `directional_variogram.py`  — data-driven anisotropy ratio & principal-axis estimation
- `operational_metrics.py`    — zoning (IoU, false-negative area, boundary displacement) and route regret
- `agcf_sbpl.py`          — segmented broken power-law fit to FM 3-3-1 altitude-correction factors
- `temporal_normalization.py` — half-life decay / Kaufmann (Way–Wigner) power-law
Keep all random seeds in `../config/` so runs are reproducible.
