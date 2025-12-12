#!/usr/bin/env python3
"""
Verify ZERO Data Leakage in Fixed Datasets
Checks for image content overlap using MD5 hashes
"""

import lmdb
import hashlib
import os
from collections import defaultdict
from tqdm import tqdm

def get_dataset_hashes(lmdb_path, name):
    """Get MD5 hashes of all images in an LMDB dataset"""
    print(f"Scanning {name}...")
    print(f"  Path: {lmdb_path}")
    
    hashes = set()
    count = 0
    
    if not os.path.exists(lmdb_path):
        print(f"  ❌ Path does not exist: {lmdb_path}")
        return hashes, 0

    try:
        env = lmdb.open(lmdb_path, readonly=True, lock=False, readahead=False, meminit=False)
        with env.begin(write=False) as txn:
            num_samples = int(txn.get('num-samples'.encode()))
            
            for i in tqdm(range(1, num_samples + 1), desc=f"  Hashing {name}", leave=False):
                image_key = f'image-{i:09d}'.encode()
                image_data = txn.get(image_key)
                
                if image_data:
                    # Calculate MD5 hash of image content
                    img_hash = hashlib.md5(image_data).hexdigest()
                    hashes.add(img_hash)
                    count += 1
                    
        env.close()
        print(f"  ✅ Found {count} samples ({len(hashes)} unique images)")
        
    except Exception as e:
        print(f"  ❌ Error reading LMDB: {e}")
        
    return hashes, count

def check_overlap(set1, name1, set2, name2):
    """Check for overlap between two sets of hashes"""
    overlap = set1.intersection(set2)
    num_overlap = len(overlap)
    
    print(f"\nComparing {name1} vs {name2}:")
    if num_overlap == 0:
        print(f"  ✅ ZERO OVERLAP (Clean)")
    else:
        print(f"  🚨 FOUND {num_overlap} OVERLAPPING IMAGES! (Leakage Detected)")
        print(f"  Overlap Rate: {num_overlap/len(set1):.2%} of {name1}")
        
    return num_overlap

def main():
    print("=" * 100)
    print("VERIFYING FIXED DATASET INTEGRITY")
    print("Checking for Data Leakage via Image Content Hashing")
    print("=" * 100)
    print()
    
    base_dir = "/data1/vivek/parseq/data_fixed"
    
    # 1. Verify Total-Text
    print("█" * 50)
    print("1. Checking Total-Text Splits")
    print("█" * 50)
    
    tt_train_path = f"{base_dir}/totaltext_lmdb/train/totaltext"
    tt_val_path = f"{base_dir}/totaltext_lmdb/val/totaltext"
    tt_test_path = f"{base_dir}/totaltext_lmdb/test/totaltext"
    
    tt_train_hashes, _ = get_dataset_hashes(tt_train_path, "TT Train")
    tt_val_hashes, _ = get_dataset_hashes(tt_val_path, "TT Val")
    tt_test_hashes, _ = get_dataset_hashes(tt_test_path, "TT Test")
    
    leaks = 0
    leaks += check_overlap(tt_train_hashes, "TT Train", tt_val_hashes, "TT Val")
    leaks += check_overlap(tt_train_hashes, "TT Train", tt_test_hashes, "TT Test")
    leaks += check_overlap(tt_val_hashes, "TT Val", tt_test_hashes, "TT Test")
    
    if leaks == 0:
        print("\n✅ Total-Text is CLEAN (No Leakage)")
    else:
        print(f"\n❌ Total-Text has {leaks} leakage instances!")

    print("\n" + "█" * 50)
    print("2. Checking ArT Splits")
    print("█" * 50)
    
    art_train_path = f"{base_dir}/art_lmdb/train/art"
    art_val_path = f"{base_dir}/art_lmdb/val/art"
    art_test_path = f"{base_dir}/art_lmdb/test/art"
    
    art_train_hashes, _ = get_dataset_hashes(art_train_path, "ArT Train")
    art_val_hashes, _ = get_dataset_hashes(art_val_path, "ArT Val")
    art_test_hashes, _ = get_dataset_hashes(art_test_path, "ArT Test")
    
    leaks = 0
    leaks += check_overlap(art_train_hashes, "ArT Train", art_val_hashes, "ArT Val")
    leaks += check_overlap(art_train_hashes, "ArT Train", art_test_hashes, "ArT Test")
    leaks += check_overlap(art_val_hashes, "ArT Val", art_test_hashes, "ArT Test")
    
    if leaks == 0:
        print("\n✅ ArT is CLEAN (No Leakage)")
    else:
        print(f"\n❌ ArT has {leaks} leakage instances!")
        
    print("\n" + "█" * 50)
    print("3. Checking Curved Mix (Combined)")
    print("█" * 50)
    
    # Curved mix is just symlinks, but let's verify the aggregate
    # Train = TT Train + ArT Train
    # Val = TT Val + ArT Val
    
    mix_train_hashes = tt_train_hashes.union(art_train_hashes)
    mix_val_hashes = tt_val_hashes.union(art_val_hashes)
    # We don't strictly have a 'mix test' folder, but conceptually it's TT Test + ArT Test
    mix_test_hashes = tt_test_hashes.union(art_test_hashes)
    
    print(f"Combined Train Unique Images: {len(mix_train_hashes)}")
    print(f"Combined Val Unique Images:   {len(mix_val_hashes)}")
    print(f"Combined Test Unique Images:  {len(mix_test_hashes)}")
    
    leaks = 0
    leaks += check_overlap(mix_train_hashes, "Mix Train", mix_val_hashes, "Mix Val")
    leaks += check_overlap(mix_train_hashes, "Mix Train", mix_test_hashes, "Mix Test")
    leaks += check_overlap(mix_val_hashes, "Mix Val", mix_test_hashes, "Mix Test")
    
    print("\n" + "=" * 100)
    print("FINAL VERDICT")
    print("=" * 100)
    
    if leaks == 0:
        print("\n✅✅✅ PASSED: NO DATA LEAKAGE DETECTED ✅✅✅")
        print("The dataset is safe for training and evaluation.")
    else:
        print("\n❌❌❌ FAILED: DATA LEAKAGE DETECTED ❌❌❌")
        print("Do not use this dataset!")

if __name__ == "__main__":
    main()
