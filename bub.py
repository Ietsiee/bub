from  pathlib import Path
import shutil
import sys
import argparse
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import hashlib
import os
import zipfile
import tarfile

cfg = Path.home() / ".config" / "bub" / "bub.config"

# Create config class
class Config:
    pass

config = Config()

# Create bub.config 
if not cfg.exists():
    cfg.parent.mkdir(parents=True, exist_ok=True)

    config.default = Path.home() / "Downloads" / "bub"

    with open(cfg, "w") as f:
        for key, value in vars(config).items():
             f.write(f"{key}={value}\n")

# Display bub banner
print(r"""
 _         _
| |__ _  _| |__
| '_ \ || | '_ \
|_.__/\_,_|_.__/
""")

# Load bubble.config
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

# Arguments
parser = argparse.ArgumentParser(
    prog="bub",
    add_help=False,
)

bub_group = parser.add_argument_group("Bub file")
bub_group.add_argument("bubfile", nargs="?", metavar="file", help=".bub file to use")

parser.add_argument("-h", "--help", action="help", help="show the help message")
parser.add_argument("-v", "--version", action="version", version="bub 1.0.1", help="show the current version")
parser.add_argument("-c", "--config", action="store_true", help="show the bub.config file path")

parser._action_groups.insert(0, parser._action_groups.pop(-1))

args = parser.parse_args()

if args.config:
    print(cfg)
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
    with urlopen(bub.source, timeout=10) as r:
        total = r.headers.get("Content-Length")
        total = int(total) if total else None

        with open(config.default / bub.filename, "wb") as f:
            downloaded = 0

            while True:
                chunk = r.read(8192)
                if not chunk:
                    break

                f.write(chunk)
                downloaded += len(chunk)

                if total:
                    percent = downloaded / total * 100
                    print(
                        f"\r[bub] 1/4 Downloading: {bub.filename} "
                        f"{percent:.0f}/100",
                        end=""
                    )
                else:
                    print(
                        f"\r[bub] 1/4 Downloading: {bub.filename}",
                        end=""
                    )

    print()

except (HTTPError, URLError, TimeoutError) as e:
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
