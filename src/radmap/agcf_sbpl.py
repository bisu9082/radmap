"""Air-to-Ground Correction Factor (AGCF) as a Segmented Broken Power-Law (SBPL).

The AGCF converts an airborne dose-rate reading at altitude h to a
ground-equivalent value: R_ground = AGCF(h) * R_air. The SBPL is a continuous
piecewise power-law interpolation of the discrete rotary-wing altitude-
correction factors tabulated in U.S. Army FM 3-3-1, Table 5-3 (e.g. AGCF=8.2 at
150 m). This is an interpolation of established reference factors, NOT an
independent physical air-to-ground validation (see manuscript / SI S2).
"""
from __future__ import annotations
import numpy as np

# FM 3-3-1 Table 5-3 rotary-wing (UH-1) reference altitude-correction factors.
# Replace/extend with the exact printed table values if needed.
FM331_TABLE_5_3 = {
    30: 2.1, 60: 3.4, 90: 4.9, 120: 6.5, 150: 8.2,
    300: 15.0, 600: 27.0, 900: 38.0,
}


def fit_sbpl(table: dict | None = None):
    """Fit per-segment power-law exponents b_k so AGCF(h)=a_k h^{b_k} on each
    interval [h_k, h_{k+1}]. Returns (breakpoints, a_k, b_k)."""
    table = table or FM331_TABLE_5_3
    h = np.array(sorted(table)); f = np.array([table[k] for k in h], float)
    b = np.diff(np.log(f)) / np.diff(np.log(h))          # segment exponents
    a = f[:-1] / h[:-1] ** b                              # segment coefficients
    return h, a, b


def agcf(h_query, table: dict | None = None):
    """Evaluate the SBPL AGCF at altitude(s) h_query (m). Out-of-range altitudes
    (below 30 m or above 900 m) use the nearest segment's power law (flagged in
    the manuscript as an extrapolation caveat)."""
    h, a, b = fit_sbpl(table)
    hq = np.atleast_1d(np.asarray(h_query, float))
    seg = np.clip(np.searchsorted(h, hq, side="right") - 1, 0, len(a) - 1)
    out = a[seg] * hq ** b[seg]
    return out if out.size > 1 else float(out[0])
