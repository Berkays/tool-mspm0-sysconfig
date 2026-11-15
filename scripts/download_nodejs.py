import os
from os import path
import platform
import ssl
import sys
import urllib.request
import tarfile
import zipfile
import shutil
from pathlib import Path


OS = platform.system().lower()
NODE_VERSION = "22.17.0"


def fatal(message):
    """Abort the post-install so that package installation fails loudly."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def get_ssl_context():
    """Use the certifi CA bundle when available.

    PlatformIO runs this script with its own Python interpreter whose
    urllib may not find system CA certificates (e.g. on macOS), which makes
    every download fail with CERTIFICATE_VERIFY_FAILED. certifi is bundled
    with PlatformIO itself.
    """
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def get_nodejs_url():
    ARCH = platform.machine().lower()

    if OS == "windows":
        ext = "zip"
        if ARCH in ("x86_64", "amd64"):
            ARCH = "win-x64"
        elif ARCH == "x86":
            ARCH = "win-x86"
        elif ARCH in ("arm64", "aarch64"):
            ARCH = "win-arm64"
        else:
            raise ValueError(f"Unsupported architecture: {ARCH}")
    elif OS == "linux":
        ext = "tar.gz"
        if ARCH == "x86_64":
            ARCH = "linux-x64"
        elif ARCH in ("arm64", "aarch64"):
            ARCH = "linux-arm64"
        else:
            raise ValueError(f"Unsupported architecture: {ARCH}")
    elif OS == "darwin":
        ext = "tar.gz"
        if ARCH == "x86_64":
            ARCH = "darwin-x64"
        elif ARCH in ("arm64", "aarch64"):
            ARCH = "darwin-arm64"
        else:
            raise ValueError(f"Unsupported architecture: {ARCH}")
    else:
        raise ValueError(f"Unsupported platform: {OS}")

    return f"https://nodejs.org/dist/v{NODE_VERSION}/node-v{NODE_VERSION}-{ARCH}.{ext}"


def download_file(url, dest_path):
    print(f"Downloading from {url}...")
    try:
        with urllib.request.urlopen(url, context=get_ssl_context()) as response, \
                open(dest_path, "wb") as f:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
        print(f"Downloaded to {dest_path}")
    except urllib.error.URLError as e:
        fatal(f"Download failed: {e}")


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
        fatal(f"Extraction failed: {e}")


def main():
    output_dir = Path("bin", "nodejs")
    output_file = os.path.join("bin", "nodejs", "node")

    if OS == "windows":
        output_file = output_file + ".exe"

    if path.exists(output_file):
        print("Node binary already exists.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # Define the output directory
    tmp_dir = Path("tmp")
    shutil.rmtree(tmp_dir, ignore_errors=True)
    tmp_dir.mkdir(exist_ok=True)

    # Get the Node.js download URL
    try:
        download_url = get_nodejs_url()
    except ValueError as e:
        fatal(str(e))

    # Determine the file name from the URL
    file_name = download_url.split("/")[-1]
    temp_file = os.path.join(tmp_dir, file_name)

    # Download the Node.js binary
    download_file(download_url, temp_file)

    # Extract the downloaded file
    extract_file(str(temp_file), str(tmp_dir))

    # POSIX archives ship the binary as node-v*/bin/node*, Windows archives
    # as node-v*/node.exe
    node_binary = next(tmp_dir.glob("node-v*/bin/node*"), None)
    if node_binary is None:
        node_binary = next(tmp_dir.glob("node-v*/node.exe"), None)

    if node_binary is None:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        fatal("Node binary not found in the downloaded archive.")

    shutil.move(str(node_binary), str(output_dir / Path(node_binary).name))
    print(f"Node binary saved to {output_file}")

    # Clean up: remove extracted directory and downloaded archive
    shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
