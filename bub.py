#!/bin/python3
import argparse
import sys
import requests
import hashlib
import os
import zipfile
import tarfile

# Arguments
parser = argparse.ArgumentParser(
    prog="bub",
    description="bub file downloader"
)

parser.add_argument("file", nargs="?", help="bub file to use")
parser.add_argument("-v", "--version", action="version", version="bub 1.0.0")

args = parser.parse_args()

if not args.file:
    parser.error("a .bub file is required")

# Display bub banner
print(r"""
 _         _
| |__ _  _| |__
| '_ \ || | '_ \
|_.__/\_,_|_.__/
""")

# Read .bub file
class Bub:
    pass

bub = Bub()

try:
    with open(args.file) as f:
        for line in f:
            if not line.strip():
                continue

            key, value = line.strip().split("=", 1)
            setattr(bub, key, value)

except FileNotFoundError:
    print(f"[bub] Error: file not found: {args.file}")
    sys.exit(1)

# Display name
print(bub.name)

# Download file
try:
    with requests.get(bub.source, stream=True, timeout=10) as r:
        r.raise_for_status()

        if "content-length" in r.headers:
            with open(bub.filename, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
                    print(
                        f"\r[bub] 1/4 Downloading: {bub.filename} "
                        f"{f.tell() / int(r.headers['content-length']) * 100:.0f}/100",
                        end=""
                    )
        else:
            with open(bub.filename, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
                    print(
                        f"\r[bub] 1/4 Downloading: {bub.filename}",
                        end=""
                    )

    print()

except requests.RequestException as e:
    print(f"[bub] Error: download failed: {e}")
    exit(1)

# Get SHA-256 (optional)
if not hasattr(bub, "sha256") or not bub.sha256:
    print("[bub] 2/4 SHA-256: skipping")

elif hashlib.sha256(open(bub.filename, "rb").read()).hexdigest() == bub.sha256:
    print("[bub] 2/4 SHA-256: Correct")

else:
    print("[bub] 2/4 SHA-256: Incorrect")
    os.remove(bub.filename)
    exit(1)

# Extract archive (optional)
if bub.filename.endswith(".zip"):
    print("[bub] 3/4 Extracting: ZIP")

    os.makedirs(bub.filename.split(".zip")[0], exist_ok=True)

    with zipfile.ZipFile(bub.filename) as f:
        f.extractall(bub.filename.split(".zip")[0])

    os.remove(bub.filename)

elif tarfile.is_tarfile(bub.filename):
    print("[bub] 3/4 Extracting: TAR")

    os.makedirs(bub.filename.split(".tar")[0], exist_ok=True)

    with tarfile.open(bub.filename) as f:
        f.extractall(bub.filename.split(".tar")[0])

    os.remove(bub.filename)

else:
    print("[bub] 3/4 Extracting: Skipping")

# Done
print("[bub] 4/4 Done")
