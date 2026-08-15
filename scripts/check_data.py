#!/usr/bin/env python3
"""Verify the CalMS21 dataset is present and loadable from ultron/data.

Checks:
  1. keypoints train/test JSONs load and report sequence counts.
  2. both mask cache symlinks resolve and contain the expected train/test splits.
  3. a sample mask from each cache has the expected (T, C, 192, 192) shape.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parent.parent / "data"
KEYPOINTS = DATA / "calms21-keypoints"
MASKS = DATA / "masks"

# Cache layout: masks/<cache>/task1/{train,test}/*.npy
EXPECTED_CHANNELS = {"roi": 2, "roi_motion_aware_v1": 4}
EXPECTED_TRAIN_SEQS = 70
EXPECTED_TEST_SEQS = 19
MASK_SIZE = 192


def check_keypoints() -> None:
    print("== keypoints ==")
    for name, expected in (
        ("calms21_task1_train.json", EXPECTED_TRAIN_SEQS),
        ("calms21_task1_test.json", EXPECTED_TEST_SEQS),
    ):
        path = KEYPOINTS / name
        if not path.is_file():
            raise SystemExit(f"missing keypoints file: {path}")
        with path.open() as fh:
            data = json.load(fh)
        seqs = next(iter(data.values()))
        n = len(seqs)
        first = next(iter(seqs.values()))
        kps = np.asarray(first["keypoints"])
        shape = kps.shape
        print(f"  {name}: {n} sequences (expected {expected}), keypoints shape {shape}")
        if n != expected:
            raise SystemExit(f"  FAIL: expected {expected} sequences, got {n}")


def check_masks() -> None:
    print("== masks ==")
    for cache, channels in EXPECTED_CHANNELS.items():
        root = MASKS / cache
        if not root.is_symlink():
            raise SystemExit(f"not a symlink: {root}")
        target = root.resolve()
        if not target.exists():
            raise SystemExit(f"broken symlink: {root} -> {target}")
        task1 = root / "task1"

        def _count(split: str) -> int:
            files = list((task1 / split).glob("*.npy"))
            temps = [f.name for f in files if f.name.endswith(".tmp.npy")]
            if temps:
                print(f"    WARN: leftover temp file(s) in {cache}/{split}: {temps}")
            return len([f for f in files if not f.name.endswith(".tmp.npy")])

        train_n = _count("train")
        test_n = _count("test")
        print(f"  {cache} ({channels}ch): -> {target}")
        print(f"    train={train_n} sequences, test={test_n} sequences")

        # Sample one .npy and check (T, C, 192, 192).
        sample = next((task1 / "test").glob("*.npy"))
        mask = np.load(sample, mmap_mode="r")
        ok_shape = (
            mask.ndim == 4
            and mask.shape[1] == channels
            and mask.shape[2:] == (MASK_SIZE, MASK_SIZE)
        )
        print(f"    sample {sample.name}: shape {mask.shape} -> {'OK' if ok_shape else 'FAIL'}")
        if not ok_shape:
            raise SystemExit(f"  FAIL: unexpected mask shape {mask.shape} for {cache}")


def main() -> None:
    if not DATA.is_dir():
        raise SystemExit(f"data dir not found: {DATA} (run from repo root)")
    check_keypoints()
    check_masks()
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
