# Spatial block-CV results (G3, R2-M4 / R4-3)  — 2026-08-29
Random 5-fold CV vs Spatial block 5-fold CV (mean over folds), N=1500 space-filling samples, log10 space.

## HotSpot (2000 kT, real field)
| Method | Random R2 | Spatial R2 | Random logRMSE | Spatial logRMSE |
|---|---|---|---|---|
| IDW | 0.617 | collapse(neg) | 0.322 | 1.188 |
| OK  | 0.201 | -4.67 | 0.397 | 0.903 |
| Aniso_OK | 0.792 | 0.744 | 0.107 | 0.383 |
| TPS | 0.769 | 0.780 | 0.213 | 0.449 |

## Fukushima 2011 (real, n=128684)
IDW 0.882->0.638 | OK 0.899->0.725 | Aniso_OK 0.896->0.746 | TPS unstable(RBF blowup; needs larger smoothing)

## Fukushima 2020 (real, n=29024)
IDW 0.903->0.533 | OK 0.955->0.747 | Aniso_OK 0.935->0.720 | TPS 0.972->0.697

Takeaways:
1. Random CV overestimates accuracy vs spatially-independent CV (confirms R2-M4/R4-3). Fukushima "all>0.95 convergence" is partly autocorrelation artifact -> report lower spatial-CV values.
2. HotSpot: under spatial CV, Aniso_OK/TPS remain robust (0.74-0.78) while isotropic OK & IDW collapse -> central claim REINFORCED.
3. Synthetic anisotropy sweep (R=2/5/10/20): isotropic OK degrades monotonically (0.86->0.85->0.57->-0.57), Aniso_OK robust (0.77->0.64->0.73->0.78) -> method ranking driven by anisotropy strength (answers R2-M6).
