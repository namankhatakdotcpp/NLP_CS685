#!/bin/bash
# Train PARSeq on fixed curved_mix dataset (no data leakage)

set -e

echo "======================================================================================================"
echo "TRAINING PARSeq ON FIXED CURVED_MIX DATASET"
echo "======================================================================================================"
echo ""
echo "Dataset: /data1/vivek/parseq/data_fixed/curved_mix/"
echo "  - Train: 30,157 text crops (TT: 7,431 + ArT: 22,726)"
echo "  - Val:   6,785 text crops (TT: 1,858 + ArT: 4,927)"
echo "  - NO DATA LEAKAGE ✅"
echo ""
echo "Configuration:"
echo "  - Model: PARSeq (pretrained)"
echo "  - Learning rate: 5.7e-5 (fine-tuning)"
echo "  - Max epochs: 20"
echo "  - Batch size: 384"
echo "  - GPUs: 2"
echo ""
echo "======================================================================================================"
echo ""

# Check if pretrained model exists
if [ ! -f "pretrained=parseq.ckpt" ]; then
    echo "⚠️  Pretrained PARSeq checkpoint not found!"
    echo "   Downloading pretrained model..."
    python -c "import torch; torch.hub.load('baudm/parseq', 'parseq', pretrained=True, trust_repo=True).save('pretrained=parseq.ckpt')" || {
        echo "❌ Failed to download pretrained model"
        echo "   Please download manually or train from scratch"
        exit 1
    }
    echo "✅ Pretrained model downloaded"
    echo ""
fi

# Verify dataset exists
if [ ! -d "data_fixed/curved_mix/train" ]; then
    echo "❌ Fixed dataset not found at data_fixed/curved_mix/"
    echo "   Please run ./complete_fix_leakage.sh first"
    exit 1
fi

echo "✅ Dataset verified"
echo "✅ Starting training..."
echo ""

# Run training
python train.py experiment=parseq_curved_fixed

echo ""
echo "======================================================================================================"
echo "Training completed!"
echo "======================================================================================================"
echo ""
echo "Next steps:"
echo "  1. Check training logs in outputs/parseq/"
echo "  2. Evaluate on test sets:"
echo "     - Total-Text: data_fixed/totaltext_lmdb/test/"
echo "     - ArT: data_fixed/art_lmdb/test/"
echo ""
