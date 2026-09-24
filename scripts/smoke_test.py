#!/usr/bin/env python3
"""Quick self-test: verifies each module runs and the AGCF reproduces FM 3-3-1."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from radmap import interpolation as itp, metrics as mt, agcf_sbpl, temporal_normalization as tn
from radmap.directional_variogram import estimate_anisotropy
from radmap.operational_metrics import iou, false_negative_area

rng = np.random.default_rng(0)
x, y = rng.random(120), rng.random(120)
z = np.exp(2*x + 0.5*y)                       # smooth positive field
zq = itp.tps(x, y, z, x[:10], y[:10])
assert np.all(np.isfinite(zq))
assert abs(agcf_sbpl.agcf(150) - 8.2) < 1e-6, "AGCF(150) must equal FM 3-3-1 value 8.2"
assert np.isclose(tn.decay_normalize(1.0, 0.0, 30.17, 30.17), 0.5, atol=1e-6)  # one half-life
truth = (np.add.outer(np.arange(20), np.arange(20)) > 18).astype(float)
recon = (np.add.outer(np.arange(20), np.arange(20)) > 17).astype(float)
assert 0 <= iou(recon, truth, 0.5) <= 1
print("smoke_test OK: AGCF(150)=8.2, decay half-life check, interpolation & metrics run.")
