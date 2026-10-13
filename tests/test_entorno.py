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


# Falla del 12-oct (docs/modos-de-falla.md): la nube bloquea descargar código durante la sesión.
# Por eso marcar.py y los feriados los descarga el script de configuración, antes de que parta Claude.

def test_descarga_marcar_y_feriados_desde_estable():
    assert "/estable" in SCRIPT
    assert "marcar.py -o /opt/marcaje-buk/marcar.py" in SCRIPT
    assert "/opt/marcaje-buk/feriados/" in SCRIPT


def test_no_ejecuta_codigo_descargado_al_vuelo():
    for palabras in ordenes():
        assert not ({"bash", "sh", "python3"} & set(palabras) and "curl" in palabras), " ".join(palabras)
    assert "| bash" not in SCRIPT and "| sh" not in SCRIPT


def test_una_descarga_fallida_no_tumba_el_entorno():
    # Si el entorno no se arma, la rutina ni siquiera parte y nadie se entera. Mejor que parta y
    # avise que falta marcar.py (rutina/instrucciones.md).
    for linea in SCRIPT.splitlines():
        if linea.strip().startswith("curl") or " curl " in linea:
            assert "|| true" in linea, linea
