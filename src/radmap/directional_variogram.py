"""Data-driven anisotropy detection via directional experimental variograms.

Estimates the geometric anisotropy ratio and principal-axis direction from the
sparse sample ALONE (no reference-field information), supporting the automatic
method-selection rule (apply anisotropy-aware reconstruction when the estimated
ratio exceeds a threshold).
"""
from __future__ import annotations
import numpy as np


def directional_variogram(x, y, z, angle_deg, n_lags=12, lag_tol=None, ang_tol=22.5):
    """Experimental semivariogram along `angle_deg` (degrees from +x)."""
    x, y, z = map(lambda a: np.asarray(a, float), (x, y, z))
    n = len(x)
    dx = x[:, None] - x[None, :]; dy = y[:, None] - y[None, :]
    dist = np.hypot(dx, dy)
    ang = np.degrees(np.arctan2(dy, dx)) % 180.0
    a = angle_deg % 180.0
    dang = np.minimum(np.abs(ang - a), 180 - np.abs(ang - a))
    iu = np.triu_indices(n, 1)
    d, da = dist[iu], dang[iu]
    gamma = 0.5 * (z[:, None] - z[None, :])[iu] ** 2
    m = da <= ang_tol
    d, gamma = d[m], gamma[m]
    if d.size == 0:
        return np.array([]), np.array([])
    lag_tol = lag_tol or (np.max(d) / n_lags)
    lags = (np.arange(1, n_lags + 1)) * lag_tol
    gh = np.array([gamma[np.abs(d - L) <= lag_tol / 2].mean()
                   if np.any(np.abs(d - L) <= lag_tol / 2) else np.nan for L in lags])
    return lags, gh


def estimate_anisotropy(x, y, z, angles=(0, 45, 90, 135), n_lags=12):
    """Estimate principal-axis angle and anisotropy ratio from the directional
    ranges (proxied by the lag at which each directional variogram reaches ~95%
    of its sill). Returns dict(principal_angle_deg, ratio, ranges)."""
    ranges = {}
    for a in angles:
        lags, gh = directional_variogram(x, y, z, a, n_lags=n_lags)
        if lags.size == 0 or np.all(np.isnan(gh)):
            ranges[a] = np.nan; continue
        sill = np.nanmax(gh)
        idx = np.where(gh >= 0.95 * sill)[0]
        ranges[a] = lags[idx[0]] if idx.size else lags[-1]
    valid = {a: r for a, r in ranges.items() if np.isfinite(r)}
    if len(valid) < 2:
        return dict(principal_angle_deg=0.0, ratio=1.0, ranges=ranges)
    amax = max(valid, key=valid.get); amin = min(valid, key=valid.get)
    ratio = valid[amax] / valid[amin] if valid[amin] > 0 else 1.0
    return dict(principal_angle_deg=float(amax), ratio=float(ratio), ranges=ranges)


def select_method(ratio, threshold=1.5):
    """Simple decision rule used in the paper: anisotropy-aware reconstruction
    when the estimated ratio exceeds `threshold`, else isotropic."""
    return "anisotropic" if ratio > threshold else "isotropic"
