#!/usr/bin/env python3
"""Reproduce results/synth_anisotropy_CV.csv (paper Figure 7 data)."""
import sys, os, csv, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from radmap.synthetic_benchmark import run

def main():
    cfg_path = os.path.join(os.path.dirname(__file__), "..", "config", "seeds.json")
    seed = 42
    if os.path.exists(cfg_path):
        seed = json.load(open(cfg_path)).get("anisotropy_benchmark_seed", 42)
    rows = run(seed=seed)
    out = os.path.join(os.path.dirname(__file__), "..", "results", "synth_anisotropy_CV_reproduced.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["anisotropy_R", "mode", "method", "R2", "log10_RMSE"])
        w.writeheader(); w.writerows(rows)
    print(f"wrote {out} ({len(rows)} rows)")

if __name__ == "__main__":
    main()
