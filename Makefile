TEMP_FILE := .mypy_cache

MYPY_FLAG := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

UV := uv
PDB := pdb

SRC_DIR := src

CONFIG_PATH ?= config.json

run: install
	$(UV) run python3 -m $(SRC_DIR) "$(CONFIG_PATH)"

install:
		$(UV) sync

debug:
	$(UV) run python3 -m pdb -m $(SRC_DIR) "$(CONFIG_PATH)"

clean:
		rm -rf $(TEMP_FILE)
		find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
		@$(UV) run flake8 src/
		@$(UV) run mypy src/ $(MYPY_FLAG)

.PHONY: run install debug clean lint