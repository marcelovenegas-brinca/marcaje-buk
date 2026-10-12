#!/usr/bin/env python3
"""marcar.py: marca la asistencia en Buk desde una rutina de Claude en la nube.

    python3 marcar.py revisar                       sin red: ¿toca algún turno ahora?
    python3 marcar.py entrada hoy.json              marca la entrada, si los datos de hoy lo permiten
    python3 marcar.py salida hoy.json               marca la salida
    python3 marcar.py confirmar salida correo.json  ¿llegó el comprobante de Buk?
    python3 marcar.py probar                        entra a Buk, mira y sale SIN marcar

La decisión de marcar vive acá, con tests. Claude solo trae los datos de los calendarios y del
correo, y los deja en hoy.json tal como los leyó (ADR 0007).

Las credenciales vienen de las variables BUK_CORREO y BUK_CLAVE, del entorno de cada persona en
claude.ai. Este script no las imprime nunca, tampoco en los errores. BUK_DOMINIO es opcional y vale
brinca.buk.cl por defecto.

La configuración de cada persona la escribe su rutina en configuracion.json, en la carpeta donde
corre (ADR 0008):

    {"horario": "L-J 08:30-18:00; V 08:30-14:30",   el valor por defecto
     "pais": "CL",                                   el valor por defecto
     "calendarios": ["persona@brinca.com"],          obligatorio
     "modo": "ensayo"}                               «ensayo», el valor por defecto, hace todo menos
                                                     apretar el botón. Solo con «marcar» aprieta

La salida es una sola línea, RESULTADO <ESTADO>: <detalle>, para que la rutina la lea sin
interpretar. Ante la duda, no marca (ADR 0001).
"""
import json
import os
import re
import sys
import time as reloj
import unicodedata
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ZONA = ZoneInfo("America/Santiago")
TOLERANCIA_MIN = 30
HORARIO_POR_DEFECTO = "L-J 08:30-18:00; V 08:30-14:30"
FERIADOS = Path(__file__).resolve().parent / "feriados"

DOMINIO = os.environ.get("BUK_DOMINIO", "brinca.buk.cl")
BASE_URL = "https://" + DOMINIO
PORTAL = BASE_URL + "/static_pages/portal"
BOTON = {
    "entrada": ".btn-asistencia:not(.btn-marcaje-salida):visible",
    "salida": ".btn-asistencia.btn-marcaje-salida:visible",
}


def fin(estado, detalle=""):
    print("RESULTADO %s%s" % (estado, (": " + detalle) if detalle else ""))
    sys.exit(0)


def normalizar(texto):
    """Minúsculas y sin tildes, para comparar palabras como las escribe una persona."""
    sin_tildes = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in sin_tildes if not unicodedata.combining(c)).lower()


# El horario: «L-J 08:30-18:00; V 08:30-14:30». X es miércoles, para no confundirlo con martes.

DIAS = "LMXJVSD"
TRAMO = re.compile(r"^\s*([LMXJVSD][LMXJVSD,\-\s]*?)\s+(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})\s*$")


def leer_horario(texto):
    horario = {}
    for tramo in [t for t in texto.split(";") if t.strip()]:
        m = TRAMO.match(tramo)
        if not m:
            raise ValueError("no entiendo el tramo de horario «%s»" % tramo.strip())
        entrada, salida = time.fromisoformat(m.group(2)), time.fromisoformat(m.group(3))
        if entrada >= salida:
            raise ValueError("la entrada va antes de la salida en «%s»" % tramo.strip())
        for parte in m.group(1).replace(" ", "").split(","):
            extremos = parte.split("-")
            if len(extremos) not in (1, 2) or not all(len(e) == 1 for e in extremos):
                raise ValueError("no entiendo los días «%s»" % parte)
            desde, hasta = DIAS.index(extremos[0]), DIAS.index(extremos[-1])
            for dia in range(desde, hasta + 1):
                horario[dia] = {"entrada": entrada, "salida": salida}
    if not horario:
        raise ValueError("el horario está vacío")
    return horario


# La hora: la rutina dispara dos veces por turno, una por cada horario de Chile (ADR 0007)

def clasificar_hora(ahora, turno):
    """EN_HORA, TARDE, TEMPRANO, OTRO_HORARIO o None si el turno no está cerca."""
    minutos = (ahora.astimezone(timezone.utc) - turno.astimezone(timezone.utc)).total_seconds() / 60
    if 0 <= minutos <= TOLERANCIA_MIN:
        return "EN_HORA"
    if TOLERANCIA_MIN < minutos < 45:
        return "TARDE"
    if 45 <= abs(minutos) <= 90:
        return "OTRO_HORARIO"
    if -45 < minutos < 0:
        return "TEMPRANO"
    return None


# Los feriados viven en el repo, uno por año (ADR 0004)

class FaltaLista(Exception):
    pass


def cargar_feriados(anio, carpeta=FERIADOS):
    archivo = Path(carpeta) / ("%d.json" % anio)
    if not archivo.exists():
        raise FaltaLista("falta la lista de feriados de %d en el repo" % anio)
    return json.loads(archivo.read_text())


def feriado(dia, carpeta=FERIADOS):
    for f in cargar_feriados(dia.year, carpeta)["feriados"]:
        if f["fecha"] == dia.isoformat():
            return f["nombre"]
    return None


def revisar(ahora_utc, horario, carpeta=FERIADOS, pais="CL"):
    """Sin red: ¿toca algún turno ahora? Devuelve (estado, detalle)."""
    ahora = ahora_utc.astimezone(ZONA)
    turnos = horario.get(ahora.weekday())
    if not turnos:
        return "NO_TOCA", "hoy no hay horario"
    clases = {t: clasificar_hora(ahora, datetime.combine(ahora.date(), h, ZONA))
              for t, h in turnos.items()}
    en_hora = [t for t, c in clases.items() if c == "EN_HORA"]
    if not en_hora:
        for clase, estado in (("TARDE", "NO_MARCA"), ("TEMPRANO", "NO_MARCA"),
                              ("OTRO_HORARIO", "NO_TOCA")):
            for t, c in clases.items():
                if c == clase:
                    return estado, "%s: la %s es a las %s y son las %s" % (
                        clase, t, turnos[t].strftime("%H:%M"), ahora.strftime("%H:%M"))
        return "NO_TOCA", "SIN_TURNO: no hay ningún turno cerca de las %s" % ahora.strftime("%H:%M")
    if pais != "CL":
        return "NO_MARCA", "no hay lista de feriados para %s" % pais
    try:
        nombre = feriado(ahora.date(), carpeta)
    except FaltaLista as e:
        return "NO_MARCA", str(e)
    if nombre:
        return "NO_TOCA", "feriado: %s" % nombre
    return "SEGUIR", en_hora[0]


# Los días libres: un evento de todo el día con una de las cuatro palabras (ADR 0005)

PALABRAS_LIBRE = re.compile(r"\b(vacaciones|licencias?|permisos?|libres?)\b")


def dia_libre(dia, calendarios):
    for cal in calendarios:
        for ev in cal.get("eventos", []):
            if not ev.get("todo_el_dia"):
                continue
            inicio = date.fromisoformat(ev["inicio"][:10])
            termino = date.fromisoformat(ev["fin"][:10]) if ev.get("fin") else inicio + timedelta(1)
            if inicio <= dia < termino and PALABRAS_LIBRE.search(normalizar(ev["titulo"])):
                return ev["titulo"]
    return None


# El comprobante de Buk: dice si el turno ya está marcado hoy (ADR 0007)

ASUNTO = {
    "entrada": re.compile(r"registro (manual )?de (ingreso|entrada)"),
    "salida": re.compile(r"registro (manual )?de salida"),
}


def fecha_en_chile(texto):
    momento = datetime.fromisoformat(texto.replace("Z", "+00:00"))
    if momento.tzinfo is None:
        momento = momento.replace(tzinfo=ZONA)
    return momento.astimezone(ZONA).date()


def ya_marcado(dia, turno, comprobantes):
    for c in comprobantes:
        if ASUNTO[turno].search(normalizar(c["asunto"])) and fecha_en_chile(c["fecha"]) == dia:
            return c["asunto"]
    return None


def decidir_con_hoy(datos, dia, turno, calendarios_esperados):
    """Aplica las reglas a lo que Claude trajo en hoy.json. Devuelve (estado, detalle)."""
    if not isinstance(datos, dict):
        return "NO_MARCA", "hoy.json no tiene la forma esperada"
    if datos.get("fecha") != dia.isoformat():
        return "NO_MARCA", "hoy.json es del %s y hoy es %s" % (datos.get("fecha"), dia.isoformat())
    if datos.get("turno") != turno:
        return "NO_MARCA", "hoy.json es para la %s, no para la %s" % (datos.get("turno"), turno)
    calendarios = [c for c in datos.get("calendarios") or [] if isinstance(c, dict)]
    leidos = {c.get("id"): c for c in calendarios}
    for cid in calendarios_esperados:
        c = leidos.get(cid)
        if not c or c.get("leido") is not True or not isinstance(c.get("eventos"), list):
            return "NO_MARCA", "no se pudo leer el calendario %s" % cid
    correo = datos.get("correo")
    if (not isinstance(correo, dict) or correo.get("leido") is not True
            or not isinstance(correo.get("comprobantes"), list)):
        return "NO_MARCA", "no se pudo leer el correo para buscar el comprobante de Buk"
    try:
        libre = dia_libre(dia, calendarios)
        marcado = ya_marcado(dia, turno, correo["comprobantes"])
    except (KeyError, ValueError, TypeError, AttributeError):
        return "NO_MARCA", "hoy.json trae un evento o un comprobante que no se entiende"
    if libre:
        return "NO_TOCA", "día libre en el calendario: %s" % libre
    if marcado:
        return "NO_TOCA", "la %s ya está marcada hoy: %s" % (turno, marcado)
    return "SEGUIR", turno


def confirmar(correo, dia, turno):
    """Después de marcar: ¿llegó el comprobante de ese turno, de hoy?"""
    if not isinstance(correo, dict) or correo.get("leido") is not True:
        return "SIN_COMPROBANTE", "no se pudo leer el correo"
    try:
        asunto = ya_marcado(dia, turno, correo.get("comprobantes") or [])
    except (KeyError, ValueError, TypeError, AttributeError):
        return "SIN_COMPROBANTE", "el correo trae un comprobante que no se entiende"
    if asunto:
        return "CONFIRMADO", asunto
    return "SIN_COMPROBANTE", "no llegó el comprobante de la %s de hoy" % turno


# La respuesta de Buk después del clic. El aviso de ubicación no es un rechazo: Buk avisa que no
# pudo obtenerla y registra igual (2-oct). Se sacan esas frases antes de leer el resto.

UBICACION = re.compile(r"[^.!?]*ubicaci[oó]n[^.!?]*[.!?]?", re.I)
EXITO = re.compile(r"exitos|correctamente", re.I)
RECHAZO = re.compile(r"no (se )?pud|no (se )?puede|no es posible|error|debe|requiere|falt|"
                     r"inv[aá]lid|no fue|sin (una )?entrada", re.I)


def clasificar_respuesta(fragmentos):
    utiles = [UBICACION.sub(" ", f) for f in fragmentos]
    exito = any(EXITO.search(f) for f in utiles)
    rechazo = any(RECHAZO.search(f) for f in utiles)
    if exito and not rechazo:
        return "MARCADO"
    if rechazo and not exito:
        return "RECHAZADO"
    return "SIN_CONFIRMAR"


# El navegador

LEER_MENSAJES = """
() => {
  const sel = '.alert, [role=alert], [class*=toast], [class*=notif], [class*=flash], ' +
              '.swal2-popup, .modal.show, [class*=snackbar]';
  const fijos = /No hay ítems pendientes|Preparando marcaje/;
  const vistos = [...document.querySelectorAll(sel)]
    .filter(e => e.offsetParent !== null || getComputedStyle(e).position === 'fixed')
    .map(e => e.innerText.replace(/\\s+/g, ' ').trim())
    .filter(t => t && !fijos.test(t));
  return [...new Set(vistos)];
}
"""


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


def en_el_portal(accion):
    """Entra a Buk, abre el portal y le pasa la página a `accion`, que termina con fin()."""
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
        accion(pagina, cual)


def esperar_respuesta(pagina, maximo_s=30):
    """Lee los mensajes de Buk hasta que uno decide, o hasta `maximo_s` segundos."""
    fragmentos = []
    for _ in range(maximo_s):
        reloj.sleep(1)
        try:
            fragmentos = pagina.evaluate(LEER_MENSAJES)
        except Exception:
            continue
        if clasificar_respuesta(fragmentos) != "SIN_CONFIRMAR":
            break
    return fragmentos


# Los modos

def leer_configuracion(datos):
    """(horario, país, calendarios, modo) desde configuracion.json. ValueError si no se entiende."""
    if not isinstance(datos, dict):
        raise ValueError("configuracion.json no tiene la forma esperada")
    calendarios = datos.get("calendarios")
    if not isinstance(calendarios, list) or not calendarios or not all(
            isinstance(c, str) and c.strip() for c in calendarios):
        raise ValueError("faltan los calendarios que hay que revisar")
    modo = datos.get("modo", "ensayo")
    if modo not in ("ensayo", "marcar"):
        raise ValueError("el modo es «ensayo» o «marcar», no «%s»" % modo)
    horario = leer_horario(datos.get("horario") or HORARIO_POR_DEFECTO)
    return horario, (datos.get("pais") or "CL").upper(), [c.strip() for c in calendarios], modo


def configuracion():
    """La configuración de la persona, en configuracion.json. Si algo no se entiende, no marca."""
    try:
        return leer_configuracion(leer_json("configuracion.json"))
    except ValueError as e:
        fin("NO_MARCA", "configuracion.json: %s" % e)


def leer_json(ruta):
    try:
        return json.loads(Path(ruta).read_text())
    except (OSError, ValueError):
        return None


def modo_revisar():
    horario, pais, _, _ = configuracion()
    fin(*revisar(datetime.now(timezone.utc), horario, FERIADOS, pais))


def modo_marcar(turno, ruta_hoy):
    horario, pais, calendarios, modo = configuracion()
    # Todo se vuelve a revisar justo antes de entrar a Buk: la hora, el feriado y los datos de hoy.
    estado, detalle = revisar(datetime.now(timezone.utc), horario, FERIADOS, pais)
    if estado != "SEGUIR":
        fin(estado, detalle)
    if detalle != turno:
        fin("NO_MARCA", "ahora toca la %s, no la %s" % (detalle, turno))
    hoy = datetime.now(ZONA).date()
    estado, detalle = decidir_con_hoy(leer_json(ruta_hoy), hoy, turno, calendarios)
    if estado != "SEGUIR":
        fin(estado, detalle)

    def apretar(pagina, cual):
        boton = pagina.locator(BOTON[turno])
        if not boton.count():
            fin("ERROR", "entró a Buk pero no encontró el botón de %s" % turno)
        if modo != "marcar":
            fin("ENSAYO", "entró a Buk con %s y encontró el botón de %s; no lo apretó porque el "
                          "modo es «%s»" % (cual, turno, modo))
        boton.first.click()
        fragmentos = esperar_respuesta(pagina)
        fin(clasificar_respuesta(fragmentos),
            "Buk respondió «%s»" % (" / ".join(fragmentos)[:300] or "nada"))

    en_el_portal(apretar)


def modo_confirmar(turno, ruta_correo):
    fin(*confirmar(leer_json(ruta_correo), datetime.now(ZONA).date(), turno))


def modo_probar():
    def mirar(pagina, cual):
        if not all(pagina.locator(BOTON[t]).count() for t in BOTON):
            fin("ERROR", "sesión iniciada pero sin los botones de marcaje")
        fin("PRUEBA_OK", "entró a Buk desde la nube con %s y ve los botones de entrada y salida; "
                         "no se marcó nada" % cual)

    en_el_portal(mirar)


def main():
    args = sys.argv[1:]
    if args == ["revisar"]:
        modo_revisar()
    elif len(args) == 2 and args[0] in BOTON:
        modo_marcar(args[0], args[1])
    elif len(args) == 3 and args[0] == "confirmar" and args[1] in BOTON:
        modo_confirmar(args[1], args[2])
    elif args == ["probar"]:
        modo_probar()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
