"""Las reglas que decide marcar.py, sin red y sin tocar Buk (ADR 0007).

Las horas de los disparos son las de las rutinas en UTC: entrada a las 11:30 y 12:30, salida de
lunes a jueves a las 21:00 y 22:00, salida del viernes a las 17:30 y 18:30.
"""
from datetime import date, datetime, time, timezone
from pathlib import Path

import pytest

import marcar

FERIADOS = Path(__file__).resolve().parent.parent / "feriados"
HORARIO = marcar.leer_horario(marcar.HORARIO_POR_DEFECTO)


def utc(texto):
    return datetime.fromisoformat(texto).replace(tzinfo=timezone.utc)


def revisar(texto_utc):
    return marcar.revisar(utc(texto_utc), HORARIO, FERIADOS)


# El horario

def test_horario_por_defecto():
    assert HORARIO[0] == {"entrada": time(8, 30), "salida": time(18, 0)}
    assert HORARIO[3] == {"entrada": time(8, 30), "salida": time(18, 0)}
    assert HORARIO[4] == {"entrada": time(8, 30), "salida": time(14, 30)}
    assert 5 not in HORARIO and 6 not in HORARIO


def test_horario_con_dias_sueltos():
    h = marcar.leer_horario("L,X 09:00-17:00; V 09:00-13:00")
    assert sorted(h) == [0, 2, 4]
    assert h[4] == {"entrada": time(9, 0), "salida": time(13, 0)}


@pytest.mark.parametrize("texto", ["", "L-J 8:30", "Q 08:30-18:00", "L-J 18:00-08:30", "L-J 25:00-26:00"])
def test_horario_invalido(texto):
    with pytest.raises(ValueError):
        marcar.leer_horario(texto)


# La hora: tolerancia de 30 minutos y los dos disparos por el cambio de hora

@pytest.mark.parametrize("ahora, esperado", [
    ("08:30", "EN_HORA"), ("08:31", "EN_HORA"), ("09:00", "EN_HORA"),
    ("09:01", "TARDE"), ("09:14", "TARDE"),
    ("09:30", "OTRO_HORARIO"), ("07:30", "OTRO_HORARIO"),
    ("08:00", "TEMPRANO"),
    ("12:00", None),
])
def test_clasificar_hora(ahora, esperado):
    dia = date(2026, 10, 13)
    turno = datetime.combine(dia, time(8, 30), marcar.ZONA)
    momento = datetime.combine(dia, time.fromisoformat(ahora), marcar.ZONA)
    assert marcar.clasificar_hora(momento, turno) == esperado


@pytest.mark.parametrize("disparo, esperado", [
    # Martes 13-oct-2026, horario de verano (UTC-3)
    ("2026-10-13 11:30:40", ("SEGUIR", "entrada")),
    ("2026-10-13 12:30:40", ("NO_TOCA", "OTRO_HORARIO")),
    ("2026-10-13 21:00:40", ("SEGUIR", "salida")),
    ("2026-10-13 22:00:40", ("NO_TOCA", "OTRO_HORARIO")),
    # Viernes 16-oct-2026, salida a las 14:30
    ("2026-10-16 17:30:40", ("SEGUIR", "salida")),
    ("2026-10-16 18:30:40", ("NO_TOCA", "OTRO_HORARIO")),
    # Martes 13-jul-2027, horario de invierno (UTC-4)
    ("2027-07-13 11:30:40", ("NO_TOCA", "OTRO_HORARIO")),
    ("2027-07-13 12:30:40", ("SEGUIR", "entrada")),
    ("2027-07-13 22:00:40", ("SEGUIR", "salida")),
    # Viernes 9-jul-2027, invierno
    ("2027-07-09 17:30:40", ("NO_TOCA", "OTRO_HORARIO")),
    ("2027-07-09 18:30:40", ("SEGUIR", "salida")),
    # Lunes 5-abr-2027, el día después del cambio a invierno
    ("2027-04-05 12:30:40", ("SEGUIR", "entrada")),
])
def test_disparos_en_verano_y_en_invierno(disparo, esperado):
    estado, detalle = revisar(disparo)
    assert (estado, detalle.split(":")[0]) == esperado


def test_llega_tarde_no_marca_y_avisa():
    estado, detalle = revisar("2026-10-13 12:05:00")  # 09:05 en Chile
    assert estado == "NO_MARCA" and detalle.startswith("TARDE")


def test_fin_de_semana():
    assert revisar("2026-10-17 11:30:40")[0] == "NO_TOCA"  # sábado


def test_feriado_en_dia_habil():
    estado, detalle = revisar("2026-10-12 11:30:40")  # lunes, Encuentro de Dos Mundos
    assert estado == "NO_TOCA" and "feriado" in detalle


def test_feriado_que_solo_trae_una_fuente():
    estado, detalle = revisar("2027-09-17 11:30:40")  # viernes, Ley 20.983
    assert estado == "NO_TOCA" and "feriado" in detalle


def test_sin_lista_de_feriados_no_marca():
    estado, detalle = revisar("2028-03-01 11:30:40")
    assert estado == "NO_MARCA" and "2028" in detalle


def test_otro_pais_sin_lista_no_marca():
    estado, _ = marcar.revisar(utc("2026-10-13 11:30:40"), HORARIO, FERIADOS, pais="AR")
    assert estado == "NO_MARCA"


# Los días libres de los calendarios (ADR 0005)

HOY = date(2026, 10, 13)


def evento(titulo, inicio="2026-10-13", fin="2026-10-14", todo_el_dia=True):
    return {"titulo": titulo, "todo_el_dia": todo_el_dia, "inicio": inicio, "fin": fin}


@pytest.mark.parametrize("titulo", [
    "Vacaciones", "VACACIONES Marcelo", "Día libre", "Licencia médica", "Permiso administrativo",
    "Licencias", "Día Líbre",
])
def test_dia_libre_con_las_cuatro_palabras(titulo):
    assert marcar.dia_libre(HOY, [{"eventos": [evento(titulo)]}]) == titulo


@pytest.mark.parametrize("ev", [
    evento("Libreta de notas"),
    evento("Planificar vacaciones", todo_el_dia=False),
    evento("Vacaciones", inicio="2026-10-12", fin="2026-10-13"),
    evento("Cumpleaños"),
])
def test_no_es_dia_libre(ev):
    assert marcar.dia_libre(HOY, [{"eventos": [ev]}]) is None


def test_vacaciones_de_varios_dias():
    largo = evento("Vacaciones", inicio="2026-10-12", fin="2026-10-19")
    assert marcar.dia_libre(HOY, [{"eventos": []}, {"eventos": [largo]}]) == "Vacaciones"


# El comprobante de Buk (ADR 0007): dice si el turno ya está marcado hoy

def comprobante(asunto, fecha="2026-10-13T08:30:26-03:00"):
    return {"asunto": asunto, "fecha": fecha}


@pytest.mark.parametrize("turno, asunto", [
    ("entrada", "Registro de ingreso, recinto: Brinca"),
    ("entrada", "Se ha generado un registro manual de ingreso"),
    ("salida", "Registro de salida, recinto: Brinca"),
    ("salida", "Se ha generado un registro manual de salida"),
])
def test_ya_marcado(turno, asunto):
    assert marcar.ya_marcado(HOY, turno, [comprobante(asunto)]) == asunto


@pytest.mark.parametrize("turno, c", [
    ("salida", comprobante("Registro de ingreso, recinto: Brinca")),
    ("entrada", comprobante("Registro de ingreso, recinto: Brinca", "2026-10-12T08:30:26-03:00")),
    # 02:00 UTC del 13 son las 23:00 del 12 en Chile
    ("entrada", comprobante("Registro de ingreso, recinto: Brinca", "2026-10-13T02:00:00Z")),
    ("entrada", comprobante("Creación de Marcas")),
])
def test_no_esta_marcado(turno, c):
    assert marcar.ya_marcado(HOY, turno, [c]) is None


# hoy.json: lo que Claude trajo de los conectores, y lo que el script decide con eso

CALENDARIOS = ["marcelo.venegas@brinca.com", "venegast.marcelo@gmail.com"]


def hoy_json(**cambios):
    datos = {
        "fecha": "2026-10-13",
        "turno": "entrada",
        "calendarios": [{"id": c, "leido": True, "eventos": []} for c in CALENDARIOS],
        "correo": {"leido": True, "comprobantes": []},
    }
    datos.update(cambios)
    return datos


def decidir(datos, turno="entrada"):
    return marcar.decidir_con_hoy(datos, HOY, turno, CALENDARIOS)


def test_dia_normal_sigue():
    assert decidir(hoy_json()) == ("SEGUIR", "entrada")


@pytest.mark.parametrize("datos", [
    hoy_json(fecha="2026-10-12"),
    hoy_json(turno="salida"),
    hoy_json(calendarios=[{"id": CALENDARIOS[0], "leido": True, "eventos": []}]),
    hoy_json(calendarios=[{"id": c, "leido": c != CALENDARIOS[1], "eventos": []} for c in CALENDARIOS]),
    hoy_json(correo={"leido": False, "comprobantes": []}),
    {"fecha": "2026-10-13"},
    "no es un objeto",
])
def test_datos_incompletos_no_marca(datos):
    assert decidir(datos)[0] == "NO_MARCA"


def test_dia_libre_no_toca():
    cal = [{"id": c, "leido": True, "eventos": [evento("Vacaciones")]} for c in CALENDARIOS]
    estado, detalle = decidir(hoy_json(calendarios=cal))
    assert estado == "NO_TOCA" and "Vacaciones" in detalle


def test_ya_marcado_no_toca():
    correo = {"leido": True, "comprobantes": [comprobante("Registro de ingreso, recinto: Brinca")]}
    assert decidir(hoy_json(correo=correo))[0] == "NO_TOCA"


# La respuesta de Buk después del clic. Los textos son los reales que vio la versión del Mac.

EXITO = ("check_circle ¡Registrar Asistencia! close Tu marcaje de asistencia ha sido exitoso. Si has "
         "registrado en el sentido correcto, el comprobante de asistencia llegará a tu correo.")
UBICACION = "No pudimos obtener tu ubicación exacta. Puedes marcar igualmente."
PERMISOS = ("info Permisos de Ubicación close No pudimos obtener tu ubicación. Por favor revisa los "
            "permisos de tu navegador.")


@pytest.mark.parametrize("fragmentos, esperado", [
    ([EXITO], "MARCADO"),
    ([UBICACION, EXITO], "MARCADO"),           # 2-oct: el aviso de ubicación no es rechazo
    ([UBICACION, PERMISOS], "SIN_CONFIRMAR"),
    ([], "SIN_CONFIRMAR"),                     # 29-sep y 5-oct: Buk tardó y no se vio nada
    (["No se pudo registrar la marca"], "RECHAZADO"),
    ([EXITO, "Ocurrió un error"], "SIN_CONFIRMAR"),
])
def test_clasificar_respuesta(fragmentos, esperado):
    assert marcar.clasificar_respuesta(fragmentos) == esperado


# La confirmación: el comprobante que llegó después de marcar

def test_confirmado_por_comprobante():
    correo = {"leido": True, "comprobantes": [comprobante("Registro de salida, recinto: Brinca",
                                                          "2026-10-13T18:00:31-03:00")]}
    assert marcar.confirmar(correo, HOY, "salida")[0] == "CONFIRMADO"


@pytest.mark.parametrize("correo", [
    {"leido": True, "comprobantes": []},
    {"leido": False, "comprobantes": []},
])
def test_sin_comprobante(correo):
    assert marcar.confirmar(correo, HOY, "salida")[0] == "SIN_COMPROBANTE"


# Las listas de feriados

@pytest.mark.parametrize("anio", [2026, 2027])
def test_lista_de_feriados_bien_formada(anio):
    datos = marcar.cargar_feriados(anio, FERIADOS)
    fechas = [f["fecha"] for f in datos["feriados"]]
    assert datos["pais"] == "CL" and datos["anio"] == anio
    assert fechas == sorted(set(fechas))
    assert all(f.startswith(str(anio)) for f in fechas)
    assert all(f["fuentes"] for f in datos["feriados"])


# La configuración de cada persona, que la rutina escribe en configuracion.json (ADR 0008)

def test_configuracion_minima_usa_los_valores_por_defecto():
    horario, pais, calendarios, modo = marcar.leer_configuracion({"calendarios": ["a@brinca.com"]})
    assert horario == HORARIO and pais == "CL" and calendarios == ["a@brinca.com"]
    assert modo == "ensayo"


def test_configuracion_completa():
    datos = {"horario": "L-V 09:00-18:00", "pais": "cl", "calendarios": ["a@brinca.com", "b@gmail.com"],
             "modo": "marcar"}
    horario, pais, calendarios, modo = marcar.leer_configuracion(datos)
    assert sorted(horario) == [0, 1, 2, 3, 4] and pais == "CL" and modo == "marcar"


@pytest.mark.parametrize("datos", [
    None, {}, {"calendarios": []}, {"calendarios": "a@brinca.com"},
    {"calendarios": ["a@brinca.com"], "modo": "Marcar ya"},
    {"calendarios": ["a@brinca.com"], "horario": "todos los días"},
])
def test_configuracion_invalida(datos):
    with pytest.raises(ValueError):
        marcar.leer_configuracion(datos)
