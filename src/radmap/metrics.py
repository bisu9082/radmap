"""Evaluation metrics used throughout the radmap study.

All metrics operate on 1-D arrays of observed (`y_true`) and predicted
(`y_pred`) dose-rate values. log10-RMSE is the *principal* criterion adopted in
the paper because dose-rate fields span several orders of magnitude; R^2 is
reported alongside as a variance-explained measure.
"""
from __future__ import annotations
import numpy as np


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, float); y_pred = np.asarray(y_pred, float)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")


def log10_rmse(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-9) -> float:
    """RMSE computed in log10 space (principal criterion).

    Values are floored at `eps` before the log to keep the metric finite where
    dose rates approach zero.
    """
    a = np.log10(np.clip(np.asarray(y_true, float), eps, None))
    b = np.log10(np.clip(np.asarray(y_pred, float), eps, None))
    return float(np.sqrt(np.mean((a - b) ** 2)))


def mape(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-9) -> float:
    y_true = np.asarray(y_true, float); y_pred = np.asarray(y_pred, float)
    return float(np.mean(np.abs((y_true - y_pred) / np.clip(np.abs(y_true), eps, None))) * 100.0)


def median_abs_log_error(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-9) -> float:
    """Median absolute log10 error (MedALE): a stable alternative to MAPE where
    dose rates approach zero (MAPE becomes unstable there)."""
    a = np.log10(np.clip(np.asarray(y_true, float), eps, None))
    b = np.log10(np.clip(np.asarray(y_pred, float), eps, None))
    return float(np.median(np.abs(a - b)))
