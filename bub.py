from pathlib import Path
import shutil
import sys
import argparse
import requests
import hashlib
import os
import zipfile
import tarfile

cfg = Path.home() / ".config" / "bub" / "bub.config"

# Copy bub.config 
if not cfg.exists():
    cfg.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy("bub.config", cfg)

# Display bub banner
print(r"""
 _         _
| |__ _  _| |__
| '_ \ || | '_ \
|_.__/\_,_|_.__/

""")

# Load bubble.config
class Config:
    pass

config = Config()

with open(cfg) as f:
    for line in f:
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        key, value = line.split("=", 1)
        setattr(config, key, value)

config.default = Path(config.default).expanduser()
config.default.mkdir(parents=True, exist_ok=True)

# Save config to bub.config
def save_config():
    with open(cfg, "w") as f:
        for key, value in vars(config).items():
            f.write(f"{key}={value}\n")

# Arguments
parser = argparse.ArgumentParser(
    prog="bub",
)

parser.add_argument("bubfile", nargs="?", help=".bub file to use")
parser.add_argument("-v", "--version", action="version", version="bub 1.0.1")
parser.add_argument(
    "-d",
    "--directory",
    nargs="?",
    const="DEFAULT",
    default=None,
    metavar="directory",
    help="set a save location",
)

args = parser.parse_args()

if args.directory == "DEFAULT":
    config.default = Path.home() / "Downloads" / "bub"
    save_config()
    print(f"[bub] Default: {config.default}")
    sys.exit(0)

elif args.directory is not None:
    config.default = Path(args.directory).expanduser()
    save_config()
    print(f"[bub] Default: {config.default}")
    sys.exit(0)

if args.bubfile is None:
    parser.error("a .bub file is required")

# Read .bub file
class Bub:
    pass

bub = Bub()

try:
    with open(args.bubfile) as f:
        for line in f:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            setattr(bub, key, value)

except FileNotFoundError:
    print(f"[bub] Error: file not found: {args.bubfile}")
    sys.exit(1)

# Name
print(bub.name)

# Note
if bub.note:
    print(f"[bub] Note: {bub.note}")

# Download
try:
    with requests.get(bub.source, stream=True, timeout=10) as r:
        r.raise_for_status()

        if "content-length" in r.headers:
            with open(config.default / bub.filename, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
                    print(
                        f"\r[bub] 1/4 Downloading: {bub.filename} "
                        f"{f.tell() / int(r.headers['content-length']) * 100:.0f}/100",
                        end=""
                    )
        else:
            with open(config.default / bub.filename, "wb") as f:
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

#SHA-256 (optional)
if not hasattr(bub, "sha256") or not bub.sha256:
    print("[bub] 2/4 SHA-256: skipping")

elif hashlib.sha256(open(config.default / bub.filename, "rb").read()).hexdigest() == bub.sha256:
    print("[bub] 2/4 SHA-256: Correct")

else:
    print("[bub] 2/4 SHA-256: Incorrect")
    os.remove(config.default / bub.filename)
    exit(1)

# Extract (optional)
if bub.filename.endswith(".zip"):
    print("[bub] 3/4 Extracting: ZIP")

    os.makedirs(config.default / bub.filename.split(".zip")[0], exist_ok=True)

    with zipfile.ZipFile(config.default / bub.filename) as f:
        f.extractall(config.default / bub.filename.split(".zip")[0])

    os.remove(config.default / bub.filename)

elif tarfile.is_tarfile(config.default / bub.filename):
    print("[bub] 3/4 Extracting: TAR")

    os.makedirs(bub.filename.split(".tar")[0], exist_ok=True)

    with tarfile.open(config.default / bub.filename) as f:
        f.extractall(bub.filename.split(".tar")[0])

    os.remove(config.default / bub.filename)

else:
    print("[bub] 3/4 Extracting: Skipping")

# Done
print("[bub] 4/4 Done")
