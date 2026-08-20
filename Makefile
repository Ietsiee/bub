PREFIX  ?= /usr
BINDIR  := $(PREFIX)/bin

.PHONY: all install uninstall clean

all: install

install:
	@echo "Creating Python virtual environment..."
	python3 -m venv .venv

	@echo "Installing requests and PyInstaller..."
	.venv/bin/pip install requests pyinstaller

	@echo "Building bub..."
	.venv/bin/pyinstaller --onefile --add-data "bub.config:." bub.py

	@echo "Installing bub..."
	sudo install -m 755 dist/bub $(BINDIR)/bub

	@echo "bub installed successfully."

uninstall:
	@echo "Uninstalling bub..."
	sudo rm -f $(BINDIR)/bub
	@echo "bub uninstalled."

clean:
	rm -rf build dist bub.spec
