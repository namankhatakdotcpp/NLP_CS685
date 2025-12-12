# PARSeq Fine-tuning for Curved Text Recognition

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)

This repository contains fine-tuned PARSeq models for curved text recognition on Total-Text and ArT datasets. We achieve **94.43% accuracy** on Total-Text through decoder fine-tuning, a **+1.41% improvement** over the baseline.

---

## 📚 Course Information

This work is part of coursework for **Natural Language Processing (CS685)** at **IIT Mandi**, under the guidance of **Dr. Rohit Saluja**.

### Team Members
- **Vivek** (vivek005001)
- **Nischay**
- **Badal**
- **Jatin**

Our Presentation - NLP.pdf can be found in the root directory
---

## 🎯 Key Results

### Total-Text Test Set Performance

| Model | Accuracy | 1-NED | Improvement | Parameters |
|:------|:---------|:------|:------------|:-----------|
| **Decoder Fine-tune (Epoch 24)** | **94.43%** | **97.50%** | **+1.41%** | 2.5M (10.5%) |
| Adapter Fine-tune (Epoch 0) | 94.20% | 97.50% | +1.18% | 99K (0.42%) |
| Baseline (Official PARSeq) | 93.02% | 97.01% | - | - |

### Dataset Information

We created a mixed dataset (by combining Total-Text and ArT selectively) for curved images to finetune parseq and get better results for Curved Text (primary goal - Total-Text dataset) 

Our Dataset can be found [here
](https://drive.google.com/file/d/1H3c2U_CC4KX4lya7nL5Iilzk2SK53ecq/view?usp=drive_link)

- **Training:** 29,925 samples (7,426 Total-Text + 22,499 ArT)
- **Validation:** 6,727 samples (1,855 Total-Text + 4,872 ArT)
- **Test:** 2,207 Total-Text + 4,635 ArT samples
- **Data Integrity:** ✅ Zero leakage between splits (verified via MD5 hashing)

## 🚀 Quick Start

### Installation

1. Create a Python virtual environment and install dependencies:

```bash
git clone https://github.com/vivek005001/NLP_CS685.git
pip install -r requirements/core.cpu.txt -e .[train,test]
```

### Training

**Full decoder fine-tuning (recommended for best accuracy):**
```bash
./train_fixed_dataset.sh
```

**Decoder-only fine-tuning (faster, CPU-compatible):**
```bash
./finetune_decoder.sh
```

### Evaluation

```bash
# Evaluate on fixed dataset
python evaluate_fixed_dataset.py

# Evaluate on specific checkpoint
python test.py pretrained=outputs/parseq/YYYY-MM-DD_HH-MM-SS/checkpoints/last.ckpt \
    data.root_dir=data_fixed data.test_root=totaltext_lmdb/test
```

### Inference

```bash
# Read text from images
python read.py pretrained=path/to/checkpoint.ckpt --images demo_images/*
```

## 📊 Experimental Results

### Model Comparison on ArT Test Set

| Model | Accuracy | 1-NED | Change |
|:------|:---------|:------|:-------|
| Baseline | **92.69%** | **97.69%** | - |
| Decoder Fine-tune (Epoch 24) | 92.34% | 97.60% | -0.35% |
| Adapter Fine-tune | 92.13% | 97.53% | -0.56% |

### Zero-shot Transfer to LSVT

| Model | Accuracy | 1-NED |
|:------|:---------|:------|
| Baseline | **84.87%** | **93.96%** |
| Decoder Fine-tune | 82.82% | 93.00% |

**Key Finding:** Fine-tuning significantly improves Total-Text performance (+1.41%) with minimal impact on ArT (-0.35%), demonstrating effective domain adaptation. However, zero-shot transfer to LSVT shows 2% degradation, indicating a specialization vs generalization trade-off.

## 🔧 Training Approaches

We evaluated three fine-tuning strategies:

1. **Decoder Fine-tuning** (Best accuracy)
   - Freeze encoder, train decoder
   - 2.5M parameters (10.5% of model)
   - ~2 hours training on RTX 5000 Ada

2. **Adapter Fine-tuning** (Most efficient)
   - Add small adapter layers
   - 99K parameters (0.42% of model)
   - ~20 minutes training

3. **TPS Rectification** (Spatial transformation)
   - Add Thin-Plate Spline module
   - ~100K parameters
   - Limited benefit for PARSeq

## 📁 Repository Structure

```
parseq/
├── train.py                          # Main training script
├── test.py                           # Evaluation script
├── demo.py                           # Interactive demo
├── read.py                           # Inference on images
├── bench.py                          # Benchmark performance
├── train_fixed_dataset.sh            # Training script for fixed dataset
├── finetune_decoder.sh               # Decoder-only fine-tuning
├── evaluate_fixed_dataset.py         # Evaluate on test sets
├── create_fixed_lmdbs.py            # Create LMDB datasets
├── verify_fixed_dataset_leakage.py  # Verify no data leakage
├── configs/                          # Hydra configuration files
│   ├── experiment/                   # Experiment configs
│   │   ├── parseq_curved_fixed.yaml # Full fine-tuning config
│   │   └── parseq_finetune_curved.yaml # Decoder fine-tuning config
│   └── dataset/                      # Dataset configs
│       └── curved_mix_fixed.yaml    # Fixed curved mix dataset
├── strhub/                           # Core model implementation
└── tools/                            # Dataset conversion tools
```

## 🔬 Reproducibility

All results are reproducible using:
- **Base Model:** Official PARSeq weights (`parseq-bb5792a6.pt`)
- **Framework:** PyTorch 2.5.1, CUDA 12.4, Lightning 2.0
- **Datasets:** Fixed Total-Text + ArT with verified hashes
- **Training Configs:** Provided in `configs/experiment/`

See [`TRAINING_GUIDE.md`](TRAINING_GUIDE.md) for detailed setup instructions and [`docs/archive/RESULTS_SUMMARY.md`](docs/archive/RESULTS_SUMMARY.md) for complete experimental results.

## 📝 Citation

If you use this work, please cite the original PARSeq paper:

```bibtex
@InProceedings{bautista2022parseq,
  title={Scene Text Recognition with Permuted Autoregressive Sequence Models},
  author={Bautista, Darwin and Atienza, Rowel},
  booktitle={European Conference on Computer Vision},
  pages={178--196},
  year={2022},
  publisher={Springer}
}
```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original PARSeq implementation by [baudm](https://github.com/baudm/parseq)
- Total-Text and ArT dataset creators
- PyTorch and Lightning teams
