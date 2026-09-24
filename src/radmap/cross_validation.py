"""Random and spatially-independent (spatial block) k-fold cross-validation.

Random k-fold can overestimate accuracy when the field is spatially
autocorrelated because nearby training/test points leak information. Spatial
block CV holds out contiguous spatial regions (here, a k x 1 or sqrt(k) grid of
blocks), so test points are spatially separated from training points. All
interpolation parameters must be re-estimated on the training partition only
within each fold (the reconstructor closures below receive only training data).
"""
from __future__ import annotations
import numpy as np


def random_folds(n: int, k: int = 5, seed: int = 0):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    return [idx[i::k] for i in range(k)]


def spatial_block_folds(x, y, k: int = 5, seed: int = 0):
    """Contiguous-region hold-out. Partition the domain into `k` vertical
    blocks along x (a simple, reproducible contiguous split); each block is one
    test fold. For a 2-D checkerboard use `blocks_2d`."""
    x = np.asarray(x, float)
    order = np.argsort(x)
    return [order[i * len(order) // k:(i + 1) * len(order) // k] for i in range(k)]


def blocks_2d(x, y, nx: int, ny: int):
    """Assign points to an nx-by-ny grid of contiguous spatial blocks (block id
    per point); useful for spatial block CV with 2-D blocks."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    bx = np.clip(((x - x.min()) / (np.ptp(x) + 1e-12) * nx).astype(int), 0, nx - 1)
    by = np.clip(((y - y.min()) / (np.ptp(y) + 1e-12) * ny).astype(int), 0, ny - 1)
    return bx * ny + by


def cross_validate(x, y, z, reconstruct, folds):
    """Run CV. `reconstruct(xtr,ytr,ztr,xte,yte)->zpred` re-fits on training
    data only. Returns concatenated (y_true, y_pred) over all folds."""
    x, y, z = map(lambda a: np.asarray(a, float), (x, y, z))
    yt, yp = [], []
    for test in folds:
        test = np.asarray(test, int)
        train = np.setdiff1d(np.arange(len(x)), test)
        pred = reconstruct(x[train], y[train], z[train], x[test], y[test])
        yt.append(z[test]); yp.append(np.asarray(pred, float))
    return np.concatenate(yt), np.concatenate(yp)
