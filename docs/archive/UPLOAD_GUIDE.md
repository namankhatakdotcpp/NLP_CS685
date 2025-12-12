# Google Drive Upload Guide

## Datasets to Upload

1. **curved_mix** (Mixed Total-Text + ArT dataset) - Located at: `/data1/vivek/parseq/data/curved_mix`
2. **totaltext_lmdb** (Total-Text only dataset) - Located at: `/data1/vivek/parseq/data/totaltext_lmdb`

Target Google Drive folder: https://drive.google.com/drive/folders/1QpSRvxYgOdpR8CJ2UcvC5q0Sp-DUzBcU

## Method 1: Using the Python Script (Automated)

### Prerequisites
The required package `pydrive2` has been installed.

### Steps

1. **Set up Google Drive API credentials:**
   - Go to https://console.cloud.google.com/
   - Create a new project or select an existing one
   - Enable the Google Drive API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download the credentials JSON file
   - Update `settings.yaml` with your client_id and client_secret

2. **Run the upload script:**
   ```bash
   cd /data1/vivek/parseq
   python upload_to_gdrive.py
   ```

   This will:
   - Authenticate with Google Drive (opens browser for first-time auth)
   - Compress the datasets into zip files
   - Upload them to your specified Google Drive folder

## Method 2: Manual Compression and Upload

If you prefer to manually upload via the web interface:

### Step 1: Compress the datasets

```bash
cd /data1/vivek/parseq/data

# Compress curved_mix dataset
zip -r curved_mix_dataset.zip curved_mix/

# Compress totaltext_lmdb dataset
zip -r totaltext_lmdb_dataset.zip totaltext_lmdb/
```

### Step 2: Upload via web interface
1. Go to https://drive.google.com/drive/folders/1QpSRvxYgOdpR8CJ2UcvC5q0Sp-DUzBcU
2. Click "New" → "File upload"
3. Select the zip files created above
4. Wait for upload to complete

## Method 3: Using rclone (Recommended for large files)

### Install rclone
```bash
curl https://rclone.org/install.sh | sudo bash
```

### Configure rclone
```bash
rclone config
```
Follow the prompts to set up Google Drive.

### Upload the datasets
```bash
# Upload curved_mix
rclone copy /data1/vivek/parseq/data/curved_mix gdrive:curved_mix_dataset -P

# Upload totaltext_lmdb
rclone copy /data1/vivek/parseq/data/totaltext_lmdb gdrive:totaltext_lmdb_dataset -P
```

## Dataset Information

- **curved_mix**: ~12KB (symbolic links to train/val data)
- **totaltext_lmdb**: ~148MB (LMDB format dataset)

## Notes

- The curved_mix directory appears to contain only symbolic links (12KB). You may want to verify the actual data location.
- Consider uploading the actual training data if the curved_mix folder only contains links.
