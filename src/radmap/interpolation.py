"""Spatial interpolation methods compared in the study.

Five reconstructors share a common signature ``fit_predict(x, y, z, xq, yq)``:
inverse distance weighting (IDW), ordinary kriging (OK), universal kriging (UK),
anisotropic ordinary kriging (Aniso_OK), and thin-plate spline (TPS).

Kriging uses PyKrige; TPS uses SciPy's RBFInterpolator. All interpolation is
performed in log10 space (the fields span several orders of magnitude), then
back-transformed, unless ``log_space=False`` is passed.
"""
from __future__ import annotations
import numpy as np
from scipy.interpolate import RBFInterpolator
from pykrige.ok import OrdinaryKriging
from pykrige.uk import UniversalKriging

_EPS = 1e-9


def _to_log(z, log_space):
    return np.log10(np.clip(z, _EPS, None)) if log_space else np.asarray(z, float)


def _from_log(z, log_space):
    return np.power(10.0, z) if log_space else z


def idw(x, y, z, xq, yq, power: float = 2.0, k: int | None = None, log_space: bool = True):
    """Inverse distance weighting. `k` limits to the k nearest neighbours."""
    x, y, z = map(np.asarray, (x, y, z)); zl = _to_log(z, log_space)
    xq, yq = np.asarray(xq, float), np.asarray(yq, float)
    out = np.empty(xq.shape[0])
    for i, (qx, qy) in enumerate(zip(xq, yq)):
        d = np.hypot(x - qx, y - qy)
        if np.any(d < _EPS):
            out[i] = zl[np.argmin(d)]; continue
        idx = np.arange(d.size) if k is None else np.argsort(d)[:k]
        w = 1.0 / d[idx] ** power
        out[i] = np.sum(w * zl[idx]) / np.sum(w)
    return _from_log(out, log_space)


def _clip_to_train(pred, zl, pad=1.0):
    """Clamp predictions to the training-value range (+/- pad in log space).
    A standard safeguard that prevents kriging extrapolation blow-ups from
    producing non-physical dose rates."""
    lo, hi = zl.min() - pad, zl.max() + pad
    return np.clip(pred, lo, hi)


def _krige(model_cls, x, y, z, xq, yq, log_space, **kw):
    zl = _to_log(z, log_space)
    mdl = model_cls(np.asarray(x, float), np.asarray(y, float), zl, **kw)
    pred, _ = mdl.execute("points", np.asarray(xq, float), np.asarray(yq, float))
    pred = _clip_to_train(np.asarray(pred, float), zl)
    return _from_log(pred, log_space)


def ordinary_kriging(x, y, z, xq, yq, variogram_model: str = "spherical",
                     log_space: bool = True, **kw):
    return _krige(OrdinaryKriging, x, y, z, xq, yq, log_space,
                  variogram_model=variogram_model, **kw)


def universal_kriging(x, y, z, xq, yq, variogram_model: str = "spherical",
                      drift_terms=("regional_linear",), log_space: bool = True, **kw):
    return _krige(UniversalKriging, x, y, z, xq, yq, log_space,
                  variogram_model=variogram_model, drift_terms=list(drift_terms), **kw)


def anisotropic_kriging(x, y, z, xq, yq, anisotropy_scaling: float = 1.0,
                        anisotropy_angle: float = 0.0, variogram_model: str = "spherical",
                        log_space: bool = True, **kw):
    """Anisotropic ordinary kriging. `anisotropy_scaling` = ratio of major to
    minor correlation length; `anisotropy_angle` in degrees (principal axis).
    Both may be estimated from the data with :func:`directional_variogram`."""
    return _krige(OrdinaryKriging, x, y, z, xq, yq, log_space,
                  variogram_model=variogram_model,
                  anisotropy_scaling=anisotropy_scaling,
                  anisotropy_angle=anisotropy_angle, **kw)


def tps(x, y, z, xq, yq, smoothing: float = 0.0, log_space: bool = True):
    """Thin-plate spline via SciPy RBFInterpolator (kernel='thin_plate_spline')."""
    zl = _to_log(z, log_space)
    pts = np.column_stack([np.asarray(x, float), np.asarray(y, float)])
    q = np.column_stack([np.asarray(xq, float), np.asarray(yq, float)])
    rbf = RBFInterpolator(pts, zl, kernel="thin_plate_spline", smoothing=smoothing)
    return _from_log(rbf(q), log_space)
