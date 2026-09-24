# Operational decision-quality validation vs HotSpot reference (G3: R2-M8, R4-5, R4-6) — 2026-08-29
Reconstruction from N=1500 samples; zones/routes computed on reconstruction, EVALUATED on true reference field.

## Zoning accuracy (Hot=1.0, Warm=0.1 Sv/hr)
| Method | IoU_Hot | FN_Hot(km2) | IoU_Warm | Bdisp_Warm(km) |
|---|---|---|---|---|
| IDW | 0.885 | 33.4 | 0.956 | 0.23 |
| OK  | 0.870 | 44.9 | 0.956 | 0.43 |
| Aniso_OK | 0.986 | 5.0 | 0.996 | 0.03 |
| TPS | 0.985 | 3.4 | 0.992 | 0.03 |
FN = missed hazardous area (safety-critical false negative). Aniso/TPS cut it ~9x.

## Route-regret (route on recon -> integrated dose on TRUE field; mean of 5 O-D pairs)
True optimum mean dose = 0.448 (Sv-km units)
| Method | route dose on truth | excess vs optimum |
|---|---|---|
| Aniso_OK | 0.45 | ~0 (0.1%) recovers optimum |
| OK  | 56.8 | large (route crosses plume) |
| IDW | 56.8 | large |
| TPS | 54.2 | large (smoothing-sensitive - verify) |

Takeaway: only anisotropy-aware reconstruction recovers near-optimal routes; reconstruction accuracy propagates into operational decision quality. Report absolute route dose + excess (not %, tiny denominator).
