# 🚀 Fine-Tuning Started: PARSeq Decoder on Curved Text

## ✅ Status: RUNNING

The fine-tuning process has successfully started with the following configuration:

### 🔧 Configuration
- **Task**: Fine-tune PARSeq Decoder ONLY (Encoder Frozen)
- **Dataset**: Fixed Curved Mix (Total-Text + ArT) - **NO LEAKAGE**
- **Batch Size**: 64 (Reduced to fit GPU memory)
- **Learning Rate**: 1e-4
- **Validation**: Every epoch

### 📊 Training Progress
- **Train Samples**: ~30,000 (Total-Text + ArT)
- **Val Samples**: ~6,700 (Total-Text + ArT)
- **Trainable Params**: 2.5M (Decoder + Head)
- **Frozen Params**: 21.4M (Encoder)

### 📝 Monitoring

To monitor the training progress, run:

```bash
tail -f training_finetune.log
```

### 🧪 Next Steps

1. **Wait for training to complete** (20 epochs)
2. **Evaluate on Test Sets**:
   ```bash
   python evaluate_fixed_dataset.py
   ```
   This will test on the held-out Total-Text and ArT test sets.

3. **Compare Results**:
   Check if the fine-tuned model performs better on Total-Text compared to the baseline.

---
*Started: 2025-11-24 17:57 UTC*
*PID: 963515*
