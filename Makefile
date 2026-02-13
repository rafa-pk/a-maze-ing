# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rvaz-da- <rvaz-da-@student.s19.be>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/01 18:24:00 by rvaz-da-          #+#    #+#              #
#    Updated: 2026/02/11 11:51:02 by rvaz-da-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = a_maze_ing.py
PY = python3
PIP = pip3
VENV = .venv
BIN = $(ENV)/bin/python

install:
	$(PY) -m venv $(VENV)
	$(VENV)/bin/$(PIP) install --upgrade pip
	$(VENV)/bin/$(PIP) install -r requirements.txt
	$(VENV)/bin/$(PIP) install ./packages/mlx_CLXV-2.2.tar 

run:


debug:

clean:

lint:


