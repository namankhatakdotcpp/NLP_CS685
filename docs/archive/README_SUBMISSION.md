# PARSeq Fine-tuning Submission Package

## Overview
This submission contains code, checkpoints, and reproduction instructions for fine-tuning PARSeq on curved text datasets (Total-Text and ArT).

## Directory Structure

```
parseq/
├── README_SUBMISSION.md          # This file
├── RESULTS_SUMMARY.md            # Detailed results and analysis
├── configs/
│   ├── model/
│   │   ├── parseq_finetune.yaml      # Decoder-only fine-tuning config
│   │   ├── parseq_adapters.yaml      # Adapter-based fine-tuning config
│   │   └── parseq_tps.yaml           # TPS rectification config
├── strhub/
│   └── models/
│       └── parseq/
│           ├── system_finetune.py    # Decoder fine-tuning implementation
│           ├── system_adapters.py    # Adapter implementation
│           ├── adapters.py           # Adapter module definitions
│           └── system_tps.py         # TPS implementation
├── scripts/
│   ├── train_decoder_finetune.sh     # Training script for decoder fine-tuning
│   ├── train_adapters.sh             # Training script for adapters
│   ├── train_tps.sh                  # Training script for TPS
│   ├── evaluate_all.sh               # Evaluation script for all models
│   └── reproduce_results.sh          # One-click reproduction script
├── checkpoints/
│   ├── decoder_finetune_epoch24.ckpt # Best decoder fine-tuning checkpoint
│   ├── adapter_epoch0.ckpt           # Best adapter checkpoint
│   └── baseline_parseq.pt            # Official baseline weights
└── data/
    └── README_DATA.md                # Instructions for dataset preparation
```

## Key Files to Submit

### 1. Code Files (Essential)
- `configs/model/parseq_finetune.yaml`
- `configs/model/parseq_adapters.yaml`
- `configs/model/parseq_tps.yaml`
- `strhub/models/parseq/system_finetune.py`
- `strhub/models/parseq/system_adapters.py`
- `strhub/models/parseq/adapters.py`
- `strhub/models/parseq/system_tps.py`

### 2. Training Scripts
- `run_finetune_curved_mix.sh` → rename to `scripts/train_decoder_finetune.sh`
- `run_experiments_finetuned.sh` → split into separate scripts
- `evaluate_all.sh` → comprehensive evaluation script

### 3. Checkpoints (Critical)
**Best Models:**
- `outputs/parseq_finetune/2025-11-25_06-58-53/checkpoints/epoch=24-step=1950-val_accuracy=93.2065-val_NED=97.6834.ckpt`
  → Save as: `checkpoints/decoder_finetune_epoch24.ckpt`
  
- `outputs/parseq_adapters/2025-11-25_07-58-33/checkpoints/epoch=0-step=20-val_accuracy=93.8544-val_NED=97.6979.ckpt`
  → Save as: `checkpoints/adapter_epoch0.ckpt`

**Optional (if space allows):**
- `outputs/parseq_tps/2025-11-25_07-43-14/checkpoints/epoch=19-step=400-val_accuracy=92.0216-val_NED=97.1684.ckpt`
  → Save as: `checkpoints/tps_epoch19.ckpt`

### 4. Documentation
- `README_SUBMISSION.md` - Overview and quick start
- `RESULTS_SUMMARY.md` - Detailed experimental results
- `REPRODUCTION_GUIDE.md` - Step-by-step reproduction instructions

### 5. Results Files
- Evaluation logs for all models on all datasets
- Comparison tables (can be in RESULTS_SUMMARY.md)

## What NOT to Submit
- Raw training logs (too large)
- Intermediate checkpoints (only best ones)
- Dataset files (provide download instructions instead)
- Cached files (.pyc, __pycache__, etc.)
- TensorBoard logs (unless specifically required)

## Checkpoint Sizes
- Decoder fine-tuning checkpoint: ~201 MB
- Adapter checkpoint: ~192 MB
- TPS checkpoint: ~219 MB
- Total: ~612 MB (manageable for most submission systems)

## Next Steps
1. Create the directory structure above
2. Copy/organize the essential files
3. Create comprehensive documentation
4. Test reproduction scripts on a clean environment
5. Package everything (zip/tar.gz)

## Estimated Total Size
- Code: ~50 KB
- Checkpoints: ~612 MB
- Documentation: ~100 KB
- **Total: ~612 MB**

If size is a constraint, you can:
- Submit only the best checkpoint (decoder epoch 24): ~201 MB
- Provide download links for other checkpoints
- Use model compression techniques
