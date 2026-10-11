#!/usr/bin/env python3
"""marcar.py: marca la asistencia en Buk desde una rutina de Claude en la nube.

    python3 marcar.py probar     entra a Buk, confirma que ve los botones y sale SIN marcar

Por ahora solo existe el modo `probar`, el del hito 1: responde si la nube de Claude puede abrir un
navegador y entrar a Buk. Los modos `entrada` y `salida` llegan en el hito 2, con sus tests.

Las credenciales vienen de las variables de entorno BUK_CORREO y BUK_CLAVE, que cada persona guarda
en el entorno de su rutina en claude.ai. Este script no las imprime nunca, tampoco en los errores.
BUK_DOMINIO es opcional y vale brinca.buk.cl por defecto.

La salida es una sola línea que empieza con RESULTADO, para que la rutina la lea sin interpretar.
"""
import os
import re
import sys

DOMINIO = os.environ.get("BUK_DOMINIO", "brinca.buk.cl")
BASE_URL = "https://" + DOMINIO
PORTAL = BASE_URL + "/static_pages/portal"


def fin(estado, detalle=""):
    print("RESULTADO %s%s" % (estado, (": " + detalle) if detalle else ""))
    sys.exit(0)


def abrir_navegador(p):
    """Usa el Chrome del sistema si existe; si no, el Chromium que trae Playwright."""
    for nombre, opciones in (("chrome del sistema", {"channel": "chrome"}), ("chromium de playwright", {})):
        try:
            return p.chromium.launch(headless=True, **opciones), nombre
        except Exception:
            continue
    fin("ERROR", "no se pudo abrir ningún navegador. Corre `python3 -m playwright install chromium` "
                 "y revisa que el entorno permita esas descargas")


def entrar(pagina, correo, clave):
    """Login de Buk en dos pasos: primero el correo, después la clave."""
    pagina.goto(BASE_URL + "/users/sign_in", wait_until="domcontentloaded", timeout=45000)
    pagina.fill('input[name="user[email]"]', correo)
    pagina.locator('input[name="commit"], button[type=submit]').first.click()
    try:
        pagina.wait_for_selector("input[type=password]", timeout=20000)
    except Exception:
        texto = pagina.locator("body").inner_text()[:300]
        if re.search(r"google|microsoft|sso", texto, re.I):
            fin("BLOQUEADO", "Buk pidió entrar con Google o Microsoft, no con clave")
        fin("ERROR", "después del correo no apareció el campo de clave (%s)" % pagina.url[:80])
    pagina.fill("input[type=password]", clave)
    pagina.locator('input[name="commit"], button[type=submit]').first.click()
    pagina.wait_for_load_state("networkidle", timeout=45000)
    if pagina.locator("input[type=password]").count():
        texto = pagina.locator("body").inner_text()[:400]
        if re.search(r"c[oó]digo|verific|captcha|robot", texto, re.I):
            fin("BLOQUEADO", "Buk pidió una verificación adicional al entrar desde la nube")
        fin("ERROR", "Buk no aceptó el inicio de sesión. Revisa BUK_CORREO y BUK_CLAVE")


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "probar":
        sys.exit("uso: python3 marcar.py probar")
    correo, clave = os.environ.get("BUK_CORREO"), os.environ.get("BUK_CLAVE")
    if not correo or not clave:
        fin("ERROR", "faltan las variables BUK_CORREO y BUK_CLAVE en el entorno de la rutina")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        fin("ERROR", "falta Playwright. Corre `pip install -r requirements.txt`")

    with sync_playwright() as p:
        nav, cual = abrir_navegador(p)
        # Sin permiso de ubicación a propósito: no se inventa una posición. Buk marca igual
        # (comprobado el 2 y el 7-oct: sus comprobantes dicen «Sin coordenadas»).
        pagina = nav.new_context(locale="es-CL", timezone_id="America/Santiago").new_page()
        try:
            entrar(pagina, correo, clave)
            pagina.goto(PORTAL, wait_until="networkidle", timeout=45000)
        except Exception as e:
            fin("ERROR", "no se pudo cargar Buk (%s)" % type(e).__name__)
        if not pagina.locator(".box-marcaje").count():
            fin("ERROR", "el portal cargó sin la caja de marcaje (%s)" % pagina.url[:80])
        entrada = pagina.locator(".btn-asistencia:not(.btn-marcaje-salida)").count()
        salida = pagina.locator(".btn-asistencia.btn-marcaje-salida").count()
        if not entrada or not salida:
            fin("ERROR", "sesión iniciada pero sin los botones de marcaje")
        fin("PRUEBA_OK", "entró a Buk desde la nube con %s y ve los botones de entrada y salida; "
                         "no se marcó nada" % cual)


if __name__ == "__main__":
    main()
