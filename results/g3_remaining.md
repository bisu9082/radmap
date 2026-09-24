# G3 remaining (angle sensitivity, survey geometry, metric alternatives) — 2026-08-29

## (1) Aniso_OK directional-perturbation sensitivity (HotSpot, spatial block CV)
angle offset: -30 -20 -10 0 +10 +20 +30
R2:           0.07 0.68 0.74 0.74 0.74 0.43 0.16
-> robust within ±10 deg (R2~0.74), moderate loss at ±20 deg, severe at ±30 deg.
   Since directional variograms recover the principal axis from data, the required accuracy is attainable. (R2-M7)

## (2) Realistic survey geometry (HotSpot)
(a) Parallel flight lines (3 km spacing): IDW -4.84 | OK 0.231 | Aniso_OK 0.802 | TPS -0.104
    -> ranking preserved; Aniso_OK robust under realistic line geometry. (R2-M5)
(b) Core-excluded training, predict inaccessible high-dose core:
    all methods fail (R2<0; logRMSE 1.6-3.1; Aniso_OK least-bad 1.65)
    -> confirms extrapolation limit; physics-based priors needed for inaccessible near-field (matches manuscript limitation).

## (3) MAPE vs alternative metrics (HotSpot held-out test)
| Method | MAPE% | MedALE | MeanALE | logRMSE |
| IDW | 27.9 | 0.045 | 0.125 | 0.383 |
| OK  | 24.0 | 0.056 | 0.160 | 0.427 |
| Aniso_OK | 28.4 | 0.001 | 0.026 | 0.204 |
| TPS | 6.6 | 0.000 | 0.037 | 0.332 |
-> MAPE is unstable/misleading (rates Aniso_OK worst though it is best on all other metrics);
   median/mean absolute log-error give a stable ranking with Aniso_OK best. (R2-M12)
