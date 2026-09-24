"""Controlled synthetic anisotropic benchmark (paper Section 4 / Figure 7).

A smooth anisotropic dose-rate field is generated as a Gaussian random field
(GRF) with a geometric anisotropy ratio R = major/minor correlation length
(downwind vs crosswind). The four reconstructors are evaluated under random and
spatial block cross-validation across R in {2,5,10,20}. Isotropic OK and IDW are
expected to degrade as R grows, while anisotropy-aware Aniso_OK and (smooth) TPS
remain comparatively robust -- the central message of Figure 7.
"""
from __future__ import annotations
import numpy as np
from . import interpolation as itp
from . import metrics as mt
from .cross_validation import random_folds, spatial_block_folds, cross_validate


def anisotropic_grf(n_grid: int, R: float, base_range: float, seed: int):
    """Generate one GRF realization on an n_grid x n_grid unit domain with an
    anisotropic Gaussian covariance whose downwind (x) range is R times the
    crosswind (y) range. Returns (X, Y, Z_positive)."""
    rng = np.random.default_rng(seed)
    g = np.linspace(0.0, 1.0, n_grid)
    X, Y = np.meshgrid(g, g)
    pts = np.column_stack([X.ravel(), Y.ravel()])
    ax, ay = R * base_range, base_range
    dx = (pts[:, 0][:, None] - pts[:, 0][None, :]) / ax
    dy = (pts[:, 1][:, None] - pts[:, 1][None, :]) / ay
    C = np.exp(-(dx ** 2 + dy ** 2))                    # anisotropic Gaussian cov
    C += 1e-8 * np.eye(C.shape[0])
    L = np.linalg.cholesky(C)
    field = L @ rng.standard_normal(C.shape[0])
    Z = np.exp(1.5 * (field - field.mean()) / (field.std() + 1e-12))  # positive, multi-order
    return X.ravel(), Y.ravel(), Z


def _reconstructors(R):
    """Method closures. Aniso_OK is given the (known) anisotropy ratio R along
    the x-axis; in practice this is estimated from directional variograms."""
    base = 0.18
    # Isotropic OK assumes a single range (mis-specified under anisotropy).
    vp_iso = {"sill": 1.0, "range": base, "nugget": 0.02}
    # Aniso_OK: after PyKrige isotropises the coordinates (y scaled by R), the
    # effective range in the transformed space is ~base*R.
    vp_ani = {"sill": 1.0, "range": base * R, "nugget": 0.02}
    return {
        "IDW":      lambda xt, yt, zt, xq, yq: itp.idw(xt, yt, zt, xq, yq, power=2.0),
        "OK":       lambda xt, yt, zt, xq, yq: itp.ordinary_kriging(xt, yt, zt, xq, yq,
                        variogram_model="gaussian", variogram_parameters=vp_iso),
        "Aniso_OK": lambda xt, yt, zt, xq, yq: itp.anisotropic_kriging(xt, yt, zt, xq, yq,
                        anisotropy_scaling=R, anisotropy_angle=0.0, variogram_model="gaussian",
                        variogram_parameters=vp_ani),
        "TPS":      lambda xt, yt, zt, xq, yq: np.clip(itp.tps(xt, yt, zt, xq, yq, smoothing=1e-3),
                        zt.min()/10, zt.max()*10),
    }


def run(ratios=(2, 5, 10, 20), n_grid: int = 28, n_sample: int = 220,
        k: int = 5, seed: int = 42):
    """Run the benchmark; returns a list of dict rows
    (anisotropy_R, mode, method, R2, log10_RMSE)."""
    rng = np.random.default_rng(seed)
    rows = []
    for R in ratios:
        X, Y, Z = anisotropic_grf(n_grid, float(R), base_range=0.18, seed=seed + int(R))
        sel = rng.choice(len(X), size=min(n_sample, len(X)), replace=False)
        x, y, z = X[sel], Y[sel], Z[sel]
        folds = {"random": random_folds(len(x), k, seed),
                 "spatial": spatial_block_folds(x, y, k, seed)}
        for mode, fl in folds.items():
            for name, fn in _reconstructors(float(R)).items():
                try:
                    yt, yp = cross_validate(x, y, z, fn, fl)
                    rows.append(dict(anisotropy_R=R, mode=mode, method=name,
                                     R2=round(mt.r2_score(yt, yp), 4),
                                     log10_RMSE=round(mt.log10_rmse(yt, yp), 4)))
                except Exception as e:  # numerical failure -> record as collapse
                    rows.append(dict(anisotropy_R=R, mode=mode, method=name,
                                     R2=float("nan"), log10_RMSE=float("nan")))
    return rows
