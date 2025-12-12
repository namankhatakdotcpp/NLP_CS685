#!/usr/bin/env python3
"""
Create new LMDB databases with proper train/val/test splits (NO LEAKAGE)
"""

import lmdb
import os
import re
from pathlib import Path
from tqdm import tqdm

def load_split_files(split_dir):
    """Load the split files"""
    split_dir = Path(split_dir)
    
    splits = {}
    
    # Total-Text
    with open(split_dir / "totaltext_train.txt") as f:
        splits['tt_train'] = set(line.strip() for line in f)
    
    with open(split_dir / "totaltext_val.txt") as f:
        splits['tt_val'] = set(line.strip() for line in f)
    
    with open(split_dir / "totaltext_test.txt") as f:
        splits['tt_test'] = set(line.strip() for line in f)
    
    # ArT
    with open(split_dir / "art_train_scenes.txt") as f:
        splits['art_train'] = set(line.strip() for line in f)
    
    with open(split_dir / "art_val_scenes.txt") as f:
        splits['art_val'] = set(line.strip() for line in f)
    
    with open(split_dir / "art_test_scenes.txt") as f:
        splits['art_test'] = set(line.strip() for line in f)
    
    return splits

def create_totaltext_lmdb(old_lmdb_path, new_lmdb_path, image_files, split_name):
    """Create new Total-Text LMDB with only specified images"""
    print(f"\nCreating Total-Text {split_name} LMDB...")
    print(f"  Source: {old_lmdb_path}")
    print(f"  Target: {new_lmdb_path}")
    print(f"  Images: {len(image_files)}")
    
    # We need to map from original LMDB to new one
    # Since Total-Text doesn't have imagepath keys, we'll need to use the original train LMDB
    # and filter based on some heuristic or rebuild from scratch
    
    # For now, let's note that we need the original image files
    print(f"  ⚠️  Note: This requires access to original Total-Text images")
    print(f"  ⚠️  You'll need to use the STR-HUB dataset creation tools")
    
    return len(image_files)

def create_art_lmdb(old_lmdb_paths, new_lmdb_path, scene_ids, split_name):
    """Create new ArT LMDB with only specified scenes"""
    print(f"\nCreating ArT {split_name} LMDB...")
    print(f"  Target: {new_lmdb_path}")
    print(f"  Scenes: {len(scene_ids)}")
    
    # Create output directory
    os.makedirs(new_lmdb_path, exist_ok=True)
    
    # Open new LMDB for writing
    env_out = lmdb.open(new_lmdb_path, map_size=1099511627776)  # 1TB
    
    # Collect all samples from specified scenes
    samples = []
    
    for old_lmdb_path in old_lmdb_paths:
        if not os.path.exists(old_lmdb_path):
            continue
            
        print(f"  Reading from: {old_lmdb_path}")
        env_in = lmdb.open(old_lmdb_path, readonly=True, lock=False, readahead=False, meminit=False)
        
        with env_in.begin(write=False) as txn_in:
            num_samples = int(txn_in.get('num-samples'.encode()))
            
            for i in tqdm(range(1, num_samples + 1), desc=f"  Scanning"):
                path_key = f'imagepath-{i:09d}'.encode()
                path = txn_in.get(path_key)
                
                if path:
                    path_str = path.decode('utf-8')
                    match = re.search(r'gt_(\d+)_\d+\.jpg', path_str)
                    if match:
                        scene_id = match.group(1)
                        
                        if scene_id in scene_ids:
                            # Get all data for this sample
                            image_key = f'image-{i:09d}'.encode()
                            label_key = f'label-{i:09d}'.encode()
                            
                            image_data = txn_in.get(image_key)
                            label_data = txn_in.get(label_key)
                            
                            if image_data and label_data:
                                samples.append({
                                    'image': image_data,
                                    'label': label_data,
                                    'path': path
                                })
        
        env_in.close()
    
    print(f"  Collected {len(samples)} text crops from {len(scene_ids)} scenes")
    
    # Write to new LMDB
    with env_out.begin(write=True) as txn_out:
        for idx, sample in enumerate(tqdm(samples, desc="  Writing"), start=1):
            image_key = f'image-{idx:09d}'.encode()
            label_key = f'label-{idx:09d}'.encode()
            path_key = f'imagepath-{idx:09d}'.encode()
            
            txn_out.put(image_key, sample['image'])
            txn_out.put(label_key, sample['label'])
            txn_out.put(path_key, sample['path'])
        
        # Write num-samples
        txn_out.put('num-samples'.encode(), str(len(samples)).encode())
    
    env_out.close()
    
    print(f"  ✅ Created {new_lmdb_path} with {len(samples)} samples")
    return len(samples)

def main():
    print("=" * 100)
    print("CREATE NEW LMDB DATABASES (NO LEAKAGE)")
    print("=" * 100)
    print()
    
    # Load splits
    split_dir = "/data1/vivek/parseq/dataset_splits"
    splits = load_split_files(split_dir)
    
    print("Loaded splits:")
    print(f"  Total-Text Train: {len(splits['tt_train'])} images")
    print(f"  Total-Text Val:   {len(splits['tt_val'])} images")
    print(f"  Total-Text Test:  {len(splits['tt_test'])} images")
    print(f"  ArT Train:        {len(splits['art_train'])} scenes")
    print(f"  ArT Val:          {len(splits['art_val'])} scenes")
    print(f"  ArT Test:         {len(splits['art_test'])} scenes")
    print()
    
    # Create output directory
    output_base = "/data1/vivek/parseq/data_fixed"
    os.makedirs(output_base, exist_ok=True)
    
    # ===== ArT LMDB Creation =====
    print("=" * 100)
    print("Creating ArT LMDBs")
    print("=" * 100)
    
    art_sources = [
        "/data1/vivek/parseq/data/art_lmdb/train/art",
        "/data1/vivek/parseq/data/art_lmdb/val"
    ]
    
    art_train_count = create_art_lmdb(
        art_sources,
        f"{output_base}/art_lmdb/train/art",
        splits['art_train'],
        "Train"
    )
    
    art_val_count = create_art_lmdb(
        art_sources,
        f"{output_base}/art_lmdb/val/art",
        splits['art_val'],
        "Val"
    )
    
    art_test_count = create_art_lmdb(
        art_sources,
        f"{output_base}/art_lmdb/test/art",
        splits['art_test'],
        "Test"
    )
    
    # ===== Total-Text Note =====
    print("\n" + "=" * 100)
    print("Total-Text LMDB Creation")
    print("=" * 100)
    print()
    print("⚠️  Total-Text LMDB creation requires original image files.")
    print("   The existing LMDB doesn't have imagepath keys, so we can't filter it.")
    print()
    print("   You have two options:")
    print("   1. Use STR-HUB's create_lmdb_dataset.py with the split files")
    print("   2. Manually create LMDB from Total-Text images using the split lists")
    print()
    print("   Split files are in: /data1/vivek/parseq/dataset_splits/")
    print()
    
    # ===== Create Curved Mix =====
    print("=" * 100)
    print("Creating Curved Mix Dataset")
    print("=" * 100)
    print()
    print("Creating symlinks for curved_mix (Total-Text + ArT)...")
    
    curved_mix_dir = f"{output_base}/curved_mix"
    os.makedirs(f"{curved_mix_dir}/train", exist_ok=True)
    os.makedirs(f"{curved_mix_dir}/val", exist_ok=True)
    os.makedirs(f"{curved_mix_dir}/test", exist_ok=True)
    
    # Create symlinks (will need Total-Text LMDBs first)
    print("  ⚠️  Curved mix will be created after Total-Text LMDBs are ready")
    
    # ===== Summary =====
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print()
    print("✅ ArT LMDBs created:")
    print(f"   - Train: {art_train_count:,} text crops from {len(splits['art_train'])} scenes")
    print(f"   - Val:   {art_val_count:,} text crops from {len(splits['art_val'])} scenes")
    print(f"   - Test:  {art_test_count:,} text crops from {len(splits['art_test'])} scenes")
    print()
    print("⚠️  Total-Text LMDBs need to be created separately")
    print("   Use the split files in: /data1/vivek/parseq/dataset_splits/")
    print()
    print("Output directory: /data1/vivek/parseq/data_fixed/")
    print()
    print("=" * 100)

if __name__ == "__main__":
    main()
