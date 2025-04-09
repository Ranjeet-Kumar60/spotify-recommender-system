import gdown
import zipfile
import os

# Your shared link from Google Drive
url = 'https://drive.google.com/uc?id=1d4bcnkFZWQBr8tbAEk5_pQEyoNOlHLRi'

# Output file
output_zip = 'data.zip'

# Download the zip file
print("Downloading data from Google Drive...")
gdown.download(url, output_zip, quiet=False)

# Extract the zip
print("Extracting files...")
with zipfile.ZipFile(output_zip, 'r') as zip_ref:
    zip_ref.extractall('data')  # Extract to data/ folder

# Optional: Remove the zip file after extraction
os.remove(output_zip)

print("Done! Data is ready in the 'data' folder.")
