import gdown
import zipfile
import os

# Google Drive shared link (make sure it's a direct link)
url = 'https://drive.google.com/uc?id=1d4bcnkFZWQBr8tbAEk5_pQEyoNOlHLRi'

# Output zip filename
output_zip = 'data.zip'

# Step 1: Download the zip file
print("Downloading data from Google Drive...")
gdown.download(url, output_zip, quiet=False)

# Step 2: Extract the zip into the current directory
print("Extracting files...")
with zipfile.ZipFile(output_zip, 'r') as zip_ref:
    zip_ref.extractall('.')  # Extracts exactly what's inside zip, in-place

# Step 3: Remove the zip file (optional cleanup)
os.remove(output_zip)

print("✅ Done! Data is ready.")
