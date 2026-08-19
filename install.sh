#!/bin/sh
set -e

cd /tmp

rm -rf bub

cat << "EOF"
 _         _
| |__ _  _| |__
| '_ \ || | '_ \
|_.__/\_,_|_.__/
EOF

if command -v bub >/dev/null 2>&1; then
    echo "Updating bub..."
    sudo rm -rf /usr/bin/bub
fi

echo "downloading bub..."
wget -q -O wget -O bub https://github.com/Ietsiee/bub/releases/latest/download/bub-linux

chmod +x bub

echo "Installing bub..."
sudo cp bub /usr/bin/bub

echo "Cleaning up..."
rm -rf bub

echo "Successfully installed bub!"
