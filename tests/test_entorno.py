"""El script de configuración del entorno, el que cada persona tiene pegado en claude.ai.

Falla del 11-oct-2026 (docs/modos-de-falla.md): `pip` a secas instaló Playwright en un Python y
`python3`, el que corre después, era otro y no lo veía. La rutina no alcanzó a empezar.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = (RAIZ / "entorno" / "configuracion.sh").read_text()


def ordenes():
    """Cada orden del script, sin comentarios, partida en palabras."""
    for linea in SCRIPT.splitlines():
        for orden in re.split(r"\|\||&&|;", linea.split("#")[0]):
            if orden.strip():
                yield orden.split()


def test_pip_es_el_del_mismo_python_que_corre_marcar():
    for palabras in ordenes():
        assert palabras[0] not in ("pip", "pip3"), "usar python3 -m pip: " + " ".join(palabras)


def test_playwright_con_la_version_de_requirements():
    fija = re.search(r"playwright==([\d.]+)", (RAIZ / "requirements.txt").read_text()).group(1)
    assert set(re.findall(r"playwright==([\d.]+)", SCRIPT)) == {fija}
