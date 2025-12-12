 #!/bin/bash
# Fine-tune PARSeq Decoder on fixed curved_mix dataset

set -e

echo "======================================================================================================"
echo "FINE-TUNING PARSeq DECODER ON FIXED CURVED_MIX DATASET"
echo "======================================================================================================"
echo ""
echo "Dataset: /data1/vivek/parseq/data_fixed/curved_mix/"
echo "  - Train: 30,157 text crops"
echo "  - Val:   6,785 text crops"
echo "  - NO DATA LEAKAGE ✅"
echo ""
echo "Configuration:"
echo "  - Model: PARSeq (Frozen Encoder, Trainable Decoder)"
echo "  - Learning rate: 1e-4"
echo "  - Max epochs: 50"
echo "  - Batch size: 384"
echo "  - CPUs: 1"
echo ""
echo "======================================================================================================"
echo ""

# Verify dataset exists
if [ ! -d "data_fixed/curved_mix/train" ]; then
    echo "❌ Fixed dataset not found at data_fixed/curved_mix/"
    echo "   Please run ./complete_fix_leakage.sh first"
    exit 1
fi

echo "✅ Dataset verified"
echo "✅ Starting fine-tuning..."
echo ""

# Run training
nohup python train.py +experiment=parseq_finetune_curved data.root_dir=/data1/vivek/parseq/data_fixed/curved_mix data.train_dir=. accelerator=cpu > training_finetune.log 2>&1 &
PID=$!

echo "Training started with PID: $PID"
echo "Logs: training_finetune.log"
echo ""
echo "Monitor with: tail -f training_finetune.log"
