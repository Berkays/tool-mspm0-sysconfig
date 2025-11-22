import os
from os import path
import platform
import urllib.request
import tarfile
import zipfile
import shutil
from pathlib import Path


OS = platform.system().lower()

def get_nodejs_url():
    node_version = "22.17.0"
    ARCH = platform.machine().lower()
    
    if OS == "windows":
        ext = "zip"
        if ARCH == "x86_64" or ARCH == "amd64":
            ARCH = "win-x64"
        elif ARCH == "x86":
            ARCH = "win-x86"
        else:
            raise ValueError(f"Unsupported architecture: {ARCH}")
    elif OS == "linux":
        ext = "tar.gz"
        if ARCH == "x86_64":
            ARCH = "linux-x64"
        elif ARCH == "arm64":
            ARCH = "linux-arm64"
        else:
            raise ValueError(f"Unsupported architecture: {ARCH}")
    elif OS == "darwin":
        ext = "tar.gz"
        if ARCH == "x86_64":
            ARCH = "darwin-x64"
        elif ARCH == "arm64":
            ARCH = "darwin-arm64"
        else:
            raise ValueError(f"Unsupported architecture: {ARCH}")
    else:
        raise ValueError(f"Unsupported platform: {OS}")
    
    return f"https://nodejs.org/dist/v{node_version}/node-v{node_version}-{ARCH}.{ext}"

def download_file(url, dest_path):
    print(f"Downloading from {url}...")
    try:
        with urllib.request.urlopen(url) as response, open(dest_path, "wb") as f:
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                f.write(chunk)
        print(f"Downloaded to {dest_path}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Download failed: {e}")

def extract_file(file_path, extract_to):
    print(f"Extracting {file_path} to {extract_to}...")
    try:
        if file_path.endswith(".tar.gz"):
            with tarfile.open(file_path, "r:gz") as tar:
                tar.extractall(extract_to)
        elif file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        print("Extraction complete")
    except (tarfile.TarError, zipfile.BadZipFile) as e:
        raise RuntimeError(f"Extraction failed: {e}")

def main():
    output_path = Path("bin", "nodejs")
    output_file = os.path.join("bin","nodejs", "node")
    
    if OS == "windows":
        output_file = output_file + ".exe"

    if(path.exists(output_file)):
        print("Node binary already exists.")
        return

    # Define the output directory
    tmp_dir = Path("tmp")
    shutil.rmtree(tmp_dir, ignore_errors=True)
    tmp_dir.mkdir(exist_ok=True)
    
    # Get the Node.js download URL
    try:
        download_url = get_nodejs_url()
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Determine the file name from the URL
    file_name = download_url.split("/")[-1]
    temp_file = os.path.join(tmp_dir, file_name)
    
    # Download the Node.js binary
    try:
        download_file(download_url, temp_file)
    except RuntimeError as e:
        print(f"Error: {e}")
        return
    
    # Extract the downloaded file
    try:
        extract_file(str(temp_file), str(tmp_dir))
    except RuntimeError as e:
        print(f"Error: {e}")
        return
    
    node_binary = next(tmp_dir.glob(f"node-v*/bin/node*"), None)

    if node_binary is None:
        print("Node binary not found in archive.")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return    
    
    shutil.move(str(node_binary), str(output_path))
    print(f"Node binary saved to {output_file}")
        
    # Clean up: remove extracted directory and downloaded archive
    shutil.rmtree(tmp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()