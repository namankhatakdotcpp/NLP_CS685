# Reproduction Guide

This guide provides step-by-step instructions to reproduce all experimental results.

## Prerequisites

### Environment Setup
```bash
# Python 3.8+
conda create -n parseq python=3.10
conda activate parseq

# Install dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install pytorch-lightning==2.0.0
pip install hydra-core omegaconf
pip install lmdb pillow tqdm timm
```

### Dataset Preparation

1. **Download Datasets:**
   - Total-Text LMDB: [Provide link or instructions]
   - ArT LMDB: [Provide link or instructions]
   - LSVT LMDB: [Provide link or instructions]

2. **Verify Dataset Structure:**
```bash
data_fixed/
├── curved_mix/
│   ├── train/
│   │   ├── totaltext/  # 7,426 samples
│   │   └── art/        # 22,499 samples
│   └── val/
│       ├── totaltext/  # 1,855 samples
│       └── art/        # 4,872 samples
├── totaltext_lmdb/
│   └── test/
│       └── totaltext/  # 2,207 samples
├── art_lmdb/
│   └── test/
│       └── art/        # 4,635 samples
└── lsvt/ (or appropriate path)
    └── test/           # 4,046 samples
```

3. **Verify Data Integrity:**
```bash
python verify_label_hash.py
# Expected output: 831b7d4692f13a3c2417456551018d26
```

---

## Reproducing Results

### 1. Baseline Evaluation

```bash
# Total-Text
python test.py pretrained=parseq \
    --data_root data_fixed/totaltext_lmdb \
    --test_set totaltext \
    --device cuda

# Expected: 93.02% accuracy

# ArT
python test.py pretrained=parseq \
    --data_root data_fixed/art_lmdb \
    --test_set art \
    --device cuda

# Expected: 92.69% accuracy

# LSVT
python test.py pretrained=parseq \
    --data_root data/train/real/LSVT \
    --test_set lsvt \
    --device cuda

# Expected: 84.87% accuracy
```

### 2. Decoder Fine-tuning

#### Training (20 epochs)
```bash
python train.py model=parseq_finetune \
    data.root_dir=data_fixed/curved_mix \
    data.train_dir=. \
    pretrained=parseq \
    trainer.max_epochs=20 \
    trainer.accelerator=gpu \
    trainer.devices=1 \
    trainer.val_check_interval=1.0
```

#### Resume Training (to epoch 50)
```bash
python train.py model=parseq_finetune \
    data.root_dir=data_fixed/curved_mix \
    data.train_dir=. \
    pretrained=parseq \
    trainer.max_epochs=50 \
    trainer.accelerator=gpu \
    trainer.devices=1 \
    trainer.val_check_interval=1.0 \
    ckpt_path=outputs/parseq_finetune/[RUN_ID]/checkpoints/last.ckpt
```

#### Evaluation (Using Provided Checkpoint)
```bash
# Total-Text
python test.py checkpoints/decoder_finetune_epoch24.ckpt \
    --data_root data_fixed/totaltext_lmdb \
    --test_set totaltext \
    --device cuda

# Expected: 94.43% accuracy

# ArT
python test.py checkpoints/decoder_finetune_epoch24.ckpt \
    --data_root data_fixed/art_lmdb \
    --test_set art \
    --device cuda

# Expected: 92.34% accuracy

# LSVT
python test.py checkpoints/decoder_finetune_epoch24.ckpt \
    --data_root data/train/real/LSVT \
    --test_set lsvt \
    --device cuda

# Expected: 82.82% accuracy
```

### 3. Adapter Fine-tuning

#### Convert Fine-tuned Checkpoint
```bash
# First, convert the decoder fine-tuned checkpoint to .pt format
python convert_checkpoint.py \
    outputs/parseq_finetune/[RUN_ID]/checkpoints/epoch=16-step=1326-val_accuracy=93.2659-val_NED=97.7343.ckpt \
    finetuned_parseq.pt
```

#### Training
```bash
python train.py model=parseq_adapters \
    data.root_dir=data_fixed/totaltext_lmdb \
    data.train_dir=. \
    pretrained=finetuned_parseq.pt \
    trainer.max_epochs=20 \
    trainer.accelerator=gpu \
    trainer.devices=1 \
    trainer.val_check_interval=1.0
```

#### Evaluation (Using Provided Checkpoint)
```bash
# Total-Text
python test.py checkpoints/adapter_epoch0.ckpt \
    --data_root data_fixed/totaltext_lmdb \
    --test_set totaltext \
    --device cuda

# Expected: 94.20% accuracy

# ArT
python test.py checkpoints/adapter_epoch0.ckpt \
    --data_root data_fixed/art_lmdb \
    --test_set art \
    --device cuda

# Expected: 92.13% accuracy

# LSVT
python test.py checkpoints/adapter_epoch0.ckpt \
    --data_root data/train/real/LSVT \
    --test_set lsvt \
    --device cuda

# Expected: 82.75% accuracy
```

### 4. TPS Rectification

#### Training
```bash
python train.py model=parseq_tps \
    data.root_dir=data_fixed/totaltext_lmdb \
    data.train_dir=. \
    pretrained=finetuned_parseq.pt \
    trainer.max_epochs=20 \
    trainer.accelerator=gpu \
    trainer.devices=1 \
    trainer.val_check_interval=1.0
```

#### Evaluation
```bash
python test.py checkpoints/tps_epoch19.ckpt \
    --data_root data_fixed/totaltext_lmdb \
    --test_set totaltext \
    --device cuda

# Expected: 93.29% accuracy
```

---

## Quick Reproduction (All Results)

Use the provided script to reproduce all results at once:

```bash
chmod +x scripts/reproduce_all_results.sh
./scripts/reproduce_all_results.sh
```

This will:
1. Evaluate baseline on all datasets
2. Evaluate all fine-tuned models on all datasets
3. Generate a results comparison table
4. Save outputs to `results/` directory

---

## Expected Training Times

On NVIDIA RTX 5000 Ada Generation (32GB):

| Model | Epochs | Time |
|:------|:-------|:-----|
| Decoder Fine-tune | 20 | ~1.5 hours |
| Decoder Fine-tune | 50 | ~3.5 hours |
| Adapter | 20 | ~20 minutes |
| TPS | 20 | ~30 minutes |

---

## Troubleshooting

### Issue: CUDA Out of Memory
**Solution:** Reduce batch size in config files
```yaml
# In configs/model/*.yaml
batch_size: 256  # Reduce from 384
```

### Issue: Dataset Not Found
**Solution:** Check paths in commands match your directory structure
```bash
# Use absolute paths if needed
python test.py ... --data_root /absolute/path/to/data_fixed/totaltext_lmdb
```

### Issue: Checkpoint Loading Error
**Solution:** Ensure you're using the correct model config
```bash
# For decoder fine-tuned checkpoints, no special config needed
python test.py checkpoints/decoder_finetune_epoch24.ckpt ...

# For adapter checkpoints, the model auto-detects adapter layers
python test.py checkpoints/adapter_epoch0.ckpt ...
```

### Issue: Different Results
**Possible causes:**
1. Different PyTorch/CUDA versions
2. Different random seeds
3. Dataset mismatch (verify hash)
4. Evaluation mode (ensure case-insensitive: no `--cased` flag)

---

## Verification Checklist

- [ ] Environment matches requirements
- [ ] Datasets downloaded and verified (hash matches)
- [ ] Baseline evaluation matches expected results (±0.5%)
- [ ] Training completes without errors
- [ ] Checkpoints saved correctly
- [ ] Evaluation on all three datasets matches expected results (±0.5%)

---

## Contact

For issues or questions about reproduction:
- Check dataset integrity first (hash verification)
- Ensure exact PyTorch/CUDA versions
- Verify no `--cased` flag is used (case-insensitive evaluation)
