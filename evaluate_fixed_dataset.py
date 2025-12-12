#!/usr/bin/env python3
"""
Evaluate PARSeq on fixed test sets (no data leakage)
"""

import sys
import subprocess
from pathlib import Path

def run_evaluation(checkpoint_path, test_dataset, dataset_name):
    """Run evaluation on a test dataset"""
    print(f"\n{'='*100}")
    print(f"Evaluating on {dataset_name}")
    print(f"{'='*100}\n")
    
    cmd = [
        "python", "test.py",
        f"pretrained={checkpoint_path}",
        f"data.root_dir=data_fixed",
        f"data.test_root={test_dataset}"
    ]
    
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode == 0:
        print(f"\n✅ {dataset_name} evaluation completed")
    else:
        print(f"\n❌ {dataset_name} evaluation failed")
    
    return result.returncode

def main():
    print("=" * 100)
    print("EVALUATE PARSeq ON FIXED TEST SETS (NO DATA LEAKAGE)")
    print("=" * 100)
    print()
    
    # Find latest checkpoint
    outputs_dir = Path("outputs/parseq")
    if not outputs_dir.exists():
        print("❌ No training outputs found!")
        print("   Please train the model first using: ./train_fixed_dataset.sh")
        sys.exit(1)
    
    # Get latest run
    runs = sorted(outputs_dir.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not runs:
        print("❌ No training runs found!")
        sys.exit(1)
    
    latest_run = runs[0]
    print(f"Latest training run: {latest_run}")
    
    # Find best checkpoint
    ckpt_dir = latest_run / "checkpoints"
    if not ckpt_dir.exists():
        print(f"❌ No checkpoints found in {ckpt_dir}")
        sys.exit(1)
    
    checkpoints = list(ckpt_dir.glob("*.ckpt"))
    if not checkpoints:
        print(f"❌ No .ckpt files found in {ckpt_dir}")
        sys.exit(1)
    
    # Use last.ckpt or best checkpoint
    best_ckpt = ckpt_dir / "last.ckpt"
    if not best_ckpt.exists():
        best_ckpt = checkpoints[0]
    
    print(f"Using checkpoint: {best_ckpt}")
    print()
    
    # Test datasets
    test_datasets = {
        "Total-Text Test": "totaltext_lmdb/test",
        "ArT Test": "art_lmdb/test"
    }
    
    results = {}
    
    for name, path in test_datasets.items():
        full_path = Path("data_fixed") / path
        if not full_path.exists():
            print(f"⚠️  {name} not found at {full_path}, skipping...")
            continue
        
        ret_code = run_evaluation(str(best_ckpt), path, name)
        results[name] = "✅ Success" if ret_code == 0 else "❌ Failed"
    
    # Summary
    print("\n" + "=" * 100)
    print("EVALUATION SUMMARY")
    print("=" * 100)
    print()
    
    for name, status in results.items():
        print(f"  {name}: {status}")
    
    print()
    print("=" * 100)
    print("NOTE: These are TRUE test set results (no data leakage)")
    print("Previous results with leaked data are INVALID")
    print("=" * 100)

if __name__ == "__main__":
    main()
