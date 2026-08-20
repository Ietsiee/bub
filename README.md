<p align="center">
  <img src="screenshot.png" alt="bub Screenshot" width="100%">
</p>

# bub
bub is a simple downloader that reads .bub files and downloads them.

## Features
- Written entirely in Python
- Easy to make your own .bub file

## Usage
```bub -h / --help``` Shows the help message
```bub -v / --version``` Shows the current version
```bub -d / --directory``` Resets the save location to default
```bub -d / -- directory [directory]``` Sets a custom save location 
```bub [bubfile]``` Runs the specified .bub file  

## .bub file
A .bub file is simple syntax style for downloading files.
See the [example `.bub` file](examples/example.bub) for a complete example.

## Installation
You can install bub using one of the following methods.

### Linux
Requirments: sudo and wget
```
curl -fsSL https://raw.githubusercontent.com/Ietsiee/bub/main/install.sh | sh
```

### Make
Requirments: sudo, make, python3 and python3-venv
```
git clone https://github.com/Ietsiee/bub.git
cd bub
sudo make install
```
