#!/bin/bash
# Script de configuración del entorno de la rutina. Se pega tal cual en claude.ai, en el campo
# «Script de configuración» del entorno de cada persona. Corre antes de que parta Claude, y claude.ai
# guarda su resultado unos siete días para no repetirlo en cada corrida.
#
# Versión de estable: 14-oct-2026. Cambiar esta línea en el entorno obliga a claude.ai a correr el
# script de nuevo, y así a descargar el marcar.py de estable sin esperar los siete días.
#
# Siempre `python3 -m pip`, nunca `pip` a secas: en la nube hay más de un Python, y `pip` puede
# instalar en uno mientras `python3` corre otro (falla del 11-oct, docs/modos-de-falla.md).
# La versión de Playwright es la de requirements.txt; tests/test_entorno.py revisa que coincidan.
python3 -m pip install playwright==1.63.0 || python3 -m pip install --break-system-packages playwright==1.63.0
python3 -m playwright install --with-deps chromium
#
# marcar.py y los feriados se descargan acá, de la versión estable, y no durante la sesión: la nube
# bloquea que Claude descargue y corra código en medio de una corrida (falla del 12-oct, ADR 0010).
# Si una descarga falla, el entorno igual se arma: la rutina ve que falta marcar.py y avisa.
mkdir -p /opt/marcaje-buk/feriados
R=https://raw.githubusercontent.com/marcelovenegas-brinca/marcaje-buk/estable
curl -fsSL $R/marcar.py -o /opt/marcaje-buk/marcar.py || true
Y=$(TZ=America/Santiago date +%Y); for A in $Y $((Y+1)); do curl -fsSL $R/feriados/$A.json -o /opt/marcaje-buk/feriados/$A.json || true; done
