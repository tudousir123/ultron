# ultron

Redesign of the HSTWFormer dual-branch experiment (pose + ROI-mask fusion) for CalMS21 Task 1 rodent behavior recognition.

## Status

Fresh start — experiment design in progress.

## Background

- **Baseline (pose-only, 5-seed, epoch-8):** macro accuracy ~81.5% ± 3.5
  - Reference: `/home/nbustu/LSC/B/BASELINE.md`
- **Previous dual-branch results** (ROI-mask fusion + motion gate): no variant beat the baseline under controlled comparison; the 4-channel motion-gate run was invalid (NaN attack, ~64 samples).
  - Reference: `/home/nbustu/LSC/B/DUAL_BRANCH_SCHEME.md`, `/home/nbustu/LSC/B/experiments/runs/`
- **Historical (uncontrolled) evidence:** epoch-28 motion-gate fusion reported 85.69% macro.

## Plan

Design doc pending.
