PREFIX  ?= /usr
BINDIR  := $(PREFIX)/bin

.PHONY: all install uninstall

all: install

install:
	@echo "Installing bub..."

	@if ! head -n 1 bub.py | grep -q '^#!/bin/python3$$'; then { echo '#!/bin/python3'; cat bub.py; } > bub.py.tmp; mv bub.py.tmp bub.py; fi

	@install -m 755 bub.py $(BINDIR)/bub

	@echo "bub installed successfully."

uninstall:
	@echo "Uninstalling bub..."

	@rm -f $(BINDIR)/bub

	@echo "bub uninstalled."
