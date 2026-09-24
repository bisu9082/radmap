"""Scenario-dependent temporal normalization of dose-rate measurements.

Radiological accident (single dominant radionuclide): half-life exponential
decay. Nuclear detonation (mixed fission products): the empirical t^{-n}
power-law (classical Way-Wigner rule, n~1.2), consistent with HotSpot's
internal fallout-decay model.
"""
from __future__ import annotations
import numpy as np

LN2 = np.log(2.0)


def decay_normalize(rate, t_meas, t_ref, half_life):
    """Accident: normalize a dose rate measured at t_meas to reference time
    t_ref using the dominant-radionuclide half-life (same time units)."""
    lam = LN2 / half_life
    return np.asarray(rate, float) * np.exp(-lam * (t_ref - t_meas))


def kaufmann_normalize(rate, t_meas, t_ref, n=1.2):
    """Detonation: normalize using the Way-Wigner/Kaufmann power law
    R(t) = R1 * t^{-n}. Times are hours after burst (t>0)."""
    t_meas = np.asarray(t_meas, float); t_ref = float(t_ref)
    return np.asarray(rate, float) * (t_ref / t_meas) ** (-n)
