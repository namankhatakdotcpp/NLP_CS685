# 🚀 Training PARSeq on Fixed Dataset - Complete Guide

## ✅ Setup Complete

All configurations and scripts are ready for training on the **fixed dataset with NO data leakage**.

---

## 📁 Dataset Summary

### Location
```
/data1/vivek/parseq/data_fixed/curved_mix/
```

### Statistics
| Split | Total Crops | Total-Text | ArT | Scenes |
|-------|-------------|------------|-----|---------|
| **Train** | 30,157 | 7,431 | 22,726 | ~4,100 |
| **Val** | 6,785 | 1,858 | 4,927 | ~900 |
| **Test** | 6,905 | 2,209 | 4,696 | ~1,000 |

### Verification
- ✅ **0% overlap** between train/val/test
- ✅ All splits properly separated
- ✅ Test sets are truly held-out

---

## 🎯 Training Configuration

### Model
- **Base**: PARSeq (pretrained on synthetic data)
- **Architecture**: Permutation Language Model
- **Fine-tuning**: On curved text (Total-Text + ArT)

### Hyperparameters
```yaml
Learning rate: 5.7e-5  (fine-tuning rate)
Batch size: 384
Max epochs: 20
Weight decay: 0.0
Warmup: 7.5%
GPUs: 2
Val check interval: 500 steps
```

### Config Files Created
- `configs/dataset/curved_mix_fixed.yaml` - Dataset config
- `configs/experiment/parseq_curved_fixed.yaml` - Experiment config

---

## 🏃 How to Train

### Option 1: Using the Training Script (Recommended)
```bash
cd /data1/vivek/parseq
./train_fixed_dataset.sh
```

This script will:
1. Check for pretrained PARSeq checkpoint
2. Verify dataset exists
3. Start training
4. Save checkpoints to `outputs/parseq/YYYY-MM-DD_HH-MM-SS/`

### Option 2: Direct Python Command
```bash
python train.py experiment=parseq_curved_fixed
```

### Option 3: Custom Configuration
```bash
python train.py \
    experiment=parseq_curved_fixed \
    trainer.max_epochs=30 \
    model.lr=1e-4
```

---

## 📊 Monitoring Training

### During Training
```bash
# Monitor training log
tail -f outputs/parseq/YYYY-MM-DD_HH-MM-SS/train.log

# Or use the monitoring script
./monitor_training.sh
```

### TensorBoard (if available)
```bash
tensorboard --logdir outputs/parseq/
```

### Key Metrics to Watch
- **Val Accuracy**: Should improve over epochs
- **Val NED** (Normalized Edit Distance): Should increase
- **Train Loss**: Should decrease steadily

---

## 🧪 Evaluation After Training

### Evaluate on Test Sets
```bash
python evaluate_fixed_dataset.py
```

This will test on:
- **Total-Text Test**: 2,209 samples (never seen during training)
- **ArT Test**: 4,696 samples (never seen during training)

### Manual Evaluation
```bash
# Total-Text Test
python test.py \
    pretrained=outputs/parseq/YYYY-MM-DD_HH-MM-SS/checkpoints/last.ckpt \
    data.root_dir=data_fixed \
    data.test_root=totaltext_lmdb/test

# ArT Test
python test.py \
    pretrained=outputs/parseq/YYYY-MM-DD_HH-MM-SS/checkpoints/last.ckpt \
    data.root_dir=data_fixed \
    data.test_root=art_lmdb/test
```

---

## 📈 Expected Results

### Baseline (Pretrained PARSeq on Total-Text)
- Total-Text accuracy: ~83-85%

### After Fine-tuning (Your Goal)
- **Total-Text**: Should maintain or improve (85-90%)
- **ArT**: Should significantly improve for curved text
- **Generalization**: Better performance on curved/arbitrary text

### Important Notes
- ⚠️ **Previous results are INVALID** due to data leakage
- ✅ **New results will be reliable** and publishable
- 📊 **Expect lower numbers** initially (no more inflated metrics from leakage)

---

## 🔧 Troubleshooting

### Out of Memory
```bash
# Reduce batch size
python train.py experiment=parseq_curved_fixed model.batch_size=192
```

### Slow Training
```bash
# Reduce validation frequency
python train.py experiment=parseq_curved_fixed trainer.val_check_interval=1000
```

### Resume Training
```bash
python train.py \
    experiment=parseq_curved_fixed \
    ckpt_path=outputs/parseq/YYYY-MM-DD_HH-MM-SS/checkpoints/last.ckpt
```

---

## 📝 Training Checklist

Before starting:
- [ ] Fixed dataset created (`data_fixed/curved_mix/`)
- [ ] No data leakage verified
- [ ] Pretrained checkpoint available
- [ ] GPU memory sufficient
- [ ] Configs created

During training:
- [ ] Monitor validation accuracy
- [ ] Check for overfitting
- [ ] Save best checkpoints

After training:
- [ ] Evaluate on test sets
- [ ] Compare with baseline
- [ ] Document results

---

## 🎓 What's Different from Before

| Aspect | Before (Leaked) | Now (Fixed) |
|--------|----------------|-------------|
| **Val Set** | Same as test ❌ | Separate from test ✅ |
| **Train/Val Overlap** | 94.8% ❌ | 0% ✅ |
| **Val Metrics** | Inflated (test data) | Reliable ✅ |
| **Test Set** | Contaminated | Clean ✅ |
| **Results** | Invalid | Publishable ✅ |

---

## 🚀 Ready to Start!

Everything is set up. Run:

```bash
cd /data1/vivek/parseq
./train_fixed_dataset.sh
```

Training will start automatically and save results to `outputs/parseq/`.

Good luck! 🎯

---

*Dataset: Fixed Curved Mix (No Leakage)*  
*Created: 2025-11-24*  
*Verified: MD5 hash-based overlap detection*
