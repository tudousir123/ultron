# Data

CalMS21 Task 1 dataset for the ultron experiment.

## Layout

```
data/
├── calms21-keypoints/           # COPIED locally (gitignored, ~1.8G)
│   ├── calms21_task1_train.json  # 70 train sequences, ~1.2G
│   └── calms21_task1_test.json   # 19 test sequences, ~603M
└── masks/                        # SYMLINKS to msgl-repo mask cache
    ├── roi                  -> /home/nbustu/LSC/msgl-repo/cache/calms21_task1_mask_derived/roi
    └── roi_motion_aware_v1  -> /home/nbustu/LSC/msgl-repo/cache/calms21_task1_mask_derived/roi_motion_aware_v1
```

## Sizes / provenance

| Item | Size | Origin |
|---|---|---|
| keypoints train JSON | 1.2G | copied from `msgl-repo/calms21-keypoints/` |
| keypoints test JSON | 603M | copied from `msgl-repo/calms21-keypoints/` |
| `roi` mask cache (2ch) | 54G | built by `msgl-repo/prepare_calms21_mask_cache.py` |
| `roi_motion_aware_v1` (4ch) | 108G | built by `msgl-repo/prepare_calms21_mask_derived_cache.py` |

The mask caches are NOT copied (161G total) — they are symlinked to the source
cache so no disk is duplicated. Recreate symlinks on a fresh machine with:

```bash
mkdir -p data/masks
ln -s /home/nbustu/LSC/msgl-repo/cache/calms21_task1_mask_derived/roi data/masks/roi
ln -s /home/nbustu/LSC/msgl-repo/cache/calms21_task1_mask_derived/roi_motion_aware_v1 data/masks/roi_motion_aware_v1
```

## Formats

### keypoints JSON

```
{ "annotator-id_0": { "<video_id>": {
      "annotations": [...],          # per-frame behavior labels
      "keypoints":   [...],          # (T, mouse, coord, body_part)
      "metadata":    {...},
      "scores":      [...]           # per-keypoint confidence
} } }
```

Official keypoints shape is `(T, 2 mice, 2 coords, 7 body_parts)`; coordinates are
2-D + confidence per point.

### Mask cache (`.npy` per sequence)

- `roi` (2 channels): `(T, 2, 192, 192)`, one binary ROI mask stream per mouse.
- `roi_motion_aware_v1` (4 channels): `(T, 4, 192, 192)`; channels `0:2` = base
  ROI masks, channels `2:4` = binary adjacent-frame difference per mouse.

## Verification

```bash
python scripts/check_data.py
```

Reports sequence counts for train/test keypoints and the channel/shape of each
mask cache.
