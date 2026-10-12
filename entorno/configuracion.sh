#!/bin/bash
# Script de configuración del entorno de la rutina. Se pega tal cual en claude.ai, en el campo
# «Script de configuración» del entorno de cada persona. Corre antes de cada sesión, y claude.ai
# guarda su resultado unos siete días para no repetirlo en cada corrida.
#
# Siempre `python3 -m pip`, nunca `pip` a secas: en la nube hay más de un Python, y `pip` puede
# instalar en uno mientras `python3` corre otro (falla del 11-oct, docs/modos-de-falla.md).
# La versión de Playwright es la de requirements.txt; tests/test_entorno.py revisa que coincidan.
python3 -m pip install playwright==1.63.0 || python3 -m pip install --break-system-packages playwright==1.63.0
python3 -m playwright install --with-deps chromium
