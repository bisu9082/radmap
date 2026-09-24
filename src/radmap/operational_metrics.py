"""Operational decision-quality metrics evaluated against a known reference field.

Zoning accuracy (hazard-zone intersection-over-union, false-negative/missed
hazardous area, boundary displacement) and minimum-dose route regret. Grids are
2-D arrays of dose rate on a common raster; `cell_area_km2` scales areas.
"""
from __future__ import annotations
import numpy as np


def _mask(field, threshold):
    return np.asarray(field, float) >= threshold


def iou(recon, truth, threshold):
    a, b = _mask(recon, threshold), _mask(truth, threshold)
    inter = np.logical_and(a, b).sum(); union = np.logical_or(a, b).sum()
    return float(inter / union) if union else float("nan")


def false_negative_area(recon, truth, threshold, cell_area_km2=1.0):
    """Safety-critical missed hazardous area: truly hazardous cells the
    reconstruction classifies as safe."""
    miss = np.logical_and(_mask(truth, threshold), ~_mask(recon, threshold))
    return float(miss.sum() * cell_area_km2)


def false_positive_area(recon, truth, threshold, cell_area_km2=1.0):
    fp = np.logical_and(~_mask(truth, threshold), _mask(recon, threshold))
    return float(fp.sum() * cell_area_km2)


def boundary_displacement(recon, truth, threshold, cell_size_km=1.0):
    """Mean distance from each reconstructed boundary cell to the nearest true
    boundary cell (km). Requires scipy.ndimage."""
    from scipy import ndimage
    def edge(m):
        m = m.astype(bool)
        return m ^ ndimage.binary_erosion(m)
    er, et = edge(_mask(recon, threshold)), edge(_mask(truth, threshold))
    if er.sum() == 0 or et.sum() == 0:
        return float("nan")
    dt = ndimage.distance_transform_edt(~et) * cell_size_km
    return float(dt[er].mean())


def route_regret(route_dose_on_truth, optimum_dose):
    """Relative excess integrated dose of a planned route vs the true optimum
    (0 = recovers optimum)."""
    return float((route_dose_on_truth - optimum_dose) / optimum_dose) if optimum_dose else float("nan")


def shortest_path_dose(cost_grid, start, goal):
    """Minimum cumulative-dose path cost via Dijkstra on a 4-connected grid.
    `cost_grid` is the per-cell dose (evaluated on the field the route is scored
    on). Returns the integrated dose of the least-dose path."""
    import heapq
    g = np.asarray(cost_grid, float); H, W = g.shape
    dist = np.full((H, W), np.inf); dist[start] = g[start]
    pq = [(g[start], start)]
    while pq:
        d, (i, j) = heapq.heappop(pq)
        if (i, j) == goal:
            return float(d)
        if d > dist[i, j]:
            continue
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            ni, nj = i+di, j+dj
            if 0 <= ni < H and 0 <= nj < W:
                nd = d + g[ni, nj]
                if nd < dist[ni, nj]:
                    dist[ni, nj] = nd; heapq.heappush(pq, (nd, (ni, nj)))
    return float(dist[goal])
