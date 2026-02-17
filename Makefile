# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rvaz-da- <rvaz-da-@student.s19.be>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/01 18:24:00 by rvaz-da-          #+#    #+#              #
#    Updated: 2026/02/17 18:27:30 by rvaz-da-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = src/a_maze_ing.py
PY = python3
PIP = pip3
VENV = .venv
PYTHON = $(VENV)/bin/python3
VENV_PIP = $(VENV)/bin/pip3
CONFIG_FILE = config.txt
SRC_DIR = src

.PHONY: install run debug clean lint lint-strict

install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	$(PY) -m venv $(VENV)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt
	tar -xf ./packages/mlx_CLXV-2.2.tar
	$(VENV_PIP) install ./mlx_CLXV/python
	@echo "Virtual environment setup complete!"


run: $(VENV)/bin/activate
	$(PYTHON) $(NAME) $(CONFIG_FILE)

debug: $(VENV)/bin/activate
	$(PYTHON) -m pdb $(NAME) $(CONFIG_FILE)

clean:
	rm -rf __pycache__/
	rm -rf $(SRC_DIR)/__pycache__/
	rm -rf $(SRC_DIR)/mazegen/__pycache__/
	rm -rf .mypy_cache/
	rm -rf $(VENV)
	rm -rf mlx_CLXV
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete!"

lint: $(VENV)/bin/activate
	$(PYTHON) -m flake8 $(SRC_DIR)/
	$(PYTHON) -m mypy $(SRC_DIR)/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: $(VENV)/bin/activate
	$(PYTHON) -m flake8 $(SRC_DIR)/
	$(PYTHON) -m mypy $(SRC_DIR)/ --strict
