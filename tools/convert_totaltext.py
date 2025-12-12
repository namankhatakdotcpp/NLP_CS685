import os
import cv2
import numpy as np
import ast
from pathlib import Path
import tqdm

def parse_line(line):
    # Format: x: [[...]], y: [[...]], ornt: [...], transcriptions: [...]
    # We want x, y, and transcriptions
    
    # Extract x
    x_str = line.split('x: ')[1].split(']],')[0] + ']]'
    # The string is like "[[1 2 3]]". 
    # It might be space separated. ast.literal_eval might fail if it's "[[1 2 3]]" (no commas)
    # So we manually parse it.
    x_vals = x_str.replace('[', '').replace(']', '').strip().split()
    x = [int(v) for v in x_vals]
    
    # Extract y
    y_str = line.split('y: ')[1].split(']],')[0] + ']]'
    y_vals = y_str.replace('[', '').replace(']', '').strip().split()
    y = [int(v) for v in y_vals]
    
    # Extract transcription
    # Find "transcriptions: "
    trans_part = line.split('transcriptions: ')[1].strip()
    # It is a list like [u'TEXT']
    try:
        trans = ast.literal_eval(trans_part)
        text = trans[0]
    except:
        # Fallback if ast fails (e.g. complex string)
        # Remove [u' and ']
        text = trans_part[3:-2]
        
    return x, y, text

def crop_and_save(image_path, annotation_path, output_dir, gt_file):
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return

    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to read image: {image_path}")
            return
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return

    if not os.path.exists(annotation_path):
        print(f"Annotation not found: {annotation_path}")
        return

    with open(annotation_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    img_name = os.path.basename(image_path)
    base_name = os.path.splitext(img_name)[0]

    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        try:
            xs, ys, text = parse_line(line)
        except Exception as e:
            print(f"Error parsing line in {annotation_path}: {e}")
            continue

        if text == '#' or not text:
            continue

        # Create polygon
        pts = np.array(list(zip(xs, ys)), np.int32)
        
        # Bounding box
        rect = cv2.boundingRect(pts)
        x, y, w, h = rect
        
        # Crop
        # Ensure within bounds
        x = max(0, x)
        y = max(0, y)
        w = min(w, img.shape[1] - x)
        h = min(h, img.shape[0] - y)
        
        if w <= 0 or h <= 0:
            continue
            
        crop = img[y:y+h, x:x+w]
        
        # Save crop
        crop_name = f"{base_name}_{idx}.jpg"
        crop_path = os.path.join(output_dir, crop_name)
        cv2.imwrite(crop_path, crop)
        
        # Write to GT
        # GT format: relative_path label
        # We will run create_lmdb_dataset.py with inputPath = output_dir
        # So relative path is just crop_name
        gt_file.write(f"{crop_name} {text}\n")

def process_subset(subset_name, data_root, output_root):
    # subset_name: 'Train' or 'Test'
    # data_root: /data1/vivek/parseq/data/Total-Text
    
    img_dir = os.path.join(data_root, subset_name)
    # Note: Annotation dir structure is .../groundtruth_polygonal_annotation/{subset_name}
    # But wait, looking at file list, it is .../groundtruth_polygonal_annotation/Test/poly_gt_img1.txt
    # And image is .../Test/img1.jpg
    
    anno_dir = os.path.join(data_root, 'Annotation', 'groundtruth_polygonal_annotation', subset_name)
    
    out_dir = os.path.join(output_root, subset_name)
    os.makedirs(out_dir, exist_ok=True)
    
    gt_path = os.path.join(output_root, f"{subset_name}_gt.txt")
    
    # List images
    images = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))])
    
    print(f"Processing {subset_name}: {len(images)} images")
    
    with open(gt_path, 'w', encoding='utf-8') as gt_f:
        for img_file in tqdm.tqdm(images):
            img_path = os.path.join(img_dir, img_file)
            
            # Construct annotation filename
            # img1.jpg -> poly_gt_img1.txt
            # img10.jpg -> poly_gt_img10.txt
            # img61.JPG -> poly_gt_img61.txt (case insensitive check needed?)
            # The annotation files seem to be lowercase 'poly_gt_imgX.txt' or matching the number.
            
            name_part = os.path.splitext(img_file)[0]
            # name_part is 'img1'
            anno_file = f"poly_gt_{name_part}.txt"
            anno_path = os.path.join(anno_dir, anno_file)
            
            # Check if anno file exists, if not try lowercase extension or something?
            # The file list showed 'poly_gt_img1.txt'.
            
            crop_and_save(img_path, anno_path, out_dir, gt_f)

def main():
    data_root = '/data1/vivek/parseq/data/Total-Text'
    output_root = '/data1/vivek/parseq/data/totaltext_crops'
    
    process_subset('Train', data_root, output_root)
    process_subset('Test', data_root, output_root)

if __name__ == '__main__':
    main()
