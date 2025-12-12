# Dataset Upload Summary

## ✅ Datasets Prepared Successfully!

Two compressed datasets are ready for upload:

1. **curved_mix_dataset.zip** (345 MB)
   - Contains: Total-Text + ArT combined training dataset
   - Location: `/data1/vivek/parseq/curved_mix_dataset.zip`
   - Structure:
     - `train/art/` - ArT training data
     - `train/totaltext/` - Total-Text training data
     - `val/totaltext/` - Total-Text validation data

2. **totaltext_lmdb_dataset.zip** (122 MB)
   - Contains: Total-Text only dataset
   - Location: `/data1/vivek/parseq/totaltext_lmdb_dataset.zip`
   - Structure:
     - `train/totaltext/` - Training data
     - `val/totaltext/` - Validation data
     - `test/totaltext/` - Test data

## Upload Options

### Option 1: Manual Upload via Web Browser (Easiest)

1. Open your browser and go to: https://drive.google.com/drive/folders/1QpSRvxYgOdpR8CJ2UcvC5q0Sp-DUzBcU
2. Click "New" → "File upload"
3. Select both files:
   - `/data1/vivek/parseq/curved_mix_dataset.zip`
   - `/data1/vivek/parseq/totaltext_lmdb_dataset.zip`
4. Wait for upload to complete

### Option 2: Using rclone (Command Line - Recommended)

**First-time setup:**
```bash
# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Configure Google Drive
rclone config
# Follow prompts:
# - Choose 'n' for new remote
# - Name it 'gdrive'
# - Choose 'drive' for Google Drive
# - Follow OAuth authentication
```

**Upload commands:**
```bash
cd /data1/vivek/parseq

# Upload both files
rclone copy curved_mix_dataset.zip gdrive:datasets/ -P
rclone copy totaltext_lmdb_dataset.zip gdrive:datasets/ -P
```

### Option 3: Using Python Script with PyDrive2

**Note:** Requires Google Cloud Console OAuth setup (complex)

See `UPLOAD_GUIDE.md` for detailed instructions.

## File Locations

- Compressed files: `/data1/vivek/parseq/`
- Original data:
  - ArT: `/data1/vivek/parseq/data/art_lmdb/`
  - Total-Text: `/data1/vivek/parseq/data/totaltext_lmdb/`
  - Mixed (symlinks): `/data1/vivek/parseq/data/curved_mix/`

## Next Steps

1. **Upload the files** using one of the options above
2. **Verify uploads** in Google Drive
3. **Share the folder** if needed with collaborators
4. **Clean up** local zip files after successful upload (optional):
   ```bash
   rm /data1/vivek/parseq/curved_mix_dataset.zip
   rm /data1/vivek/parseq/totaltext_lmdb_dataset.zip
   ```

## Target Google Drive Folder

https://drive.google.com/drive/folders/1QpSRvxYgOdpR8CJ2UcvC5q0Sp-DUzBcU
