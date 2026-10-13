# Instrucciones de la rutina de marcaje

Este texto va completo en las instrucciones de cada rutina, debajo del nombre de la persona y de su
configuración (`rutina/plantilla.md`). No se descarga durante la corrida (ADR 0010).

`marcar.py` y los feriados ya están en `/opt/marcaje-buk`: los instaló el script de configuración
de tu entorno antes de que partieras. `marcar.py` decide y aprieta. Tú solo corres sus comandos,
traes los datos de los calendarios y del correo tal como vienen, y avisas. Cada comando de
`marcar.py` termina con una línea que empieza con `RESULTADO`: esa línea manda.

## Reglas que no se rompen

1. Solo `marcar.py` entra a Buk. Tú no abres Buk ni corres otro código que lo toque.
2. Nunca muestres ni imprimas `BUK_CORREO` ni `BUK_CLAVE`: no uses `env`, `printenv`, `set` ni
   `echo` sobre ellos.
3. No reintentes. Cada comando de `marcar.py` corre una sola vez por corrida, aunque falle.
4. Copia los datos tal como vienen de los conectores. No interpretes si un día es libre ni si un
   comprobante corresponde: eso lo decide `marcar.py`.
5. No descargues nada, no edites `marcar.py` y no hagas commits.
6. Si algo de estas instrucciones no se puede cumplir, no marques: avisa y termina.

## Paso 0. Prepara la carpeta

Corre `mkdir -p ~/marcaje` y escribe `~/marcaje/configuracion.json` con tu configuración, tal cual.
Todos los comandos que siguen corren desde `~/marcaje`, por ejemplo
`cd ~/marcaje && python3 /opt/marcaje-buk/marcar.py revisar`.

Si `/opt/marcaje-buk/marcar.py` no existe, envía una notificación que diga «marcaje-buk no está
instalado en el entorno» y termina.

## Paso 1. ¿Toca algún turno?

Corre `python3 /opt/marcaje-buk/marcar.py revisar`.

| RESULTADO | Qué haces |
|---|---|
| `NO_TOCA` | Terminas, sin notificar. Es lo normal: fin de semana, feriado o el disparo del otro horario |
| `NO_MARCA` | Envías una notificación con la línea completa y terminas |
| `SEGUIR: entrada` o `SEGUIR: salida` | Sigues al paso 2 con ese turno |

## Paso 2. Trae los datos de hoy

La fecha de hoy es la de Chile: `TZ=America/Santiago date +%F`.

Calendarios. Para cada calendario de la lista `calendarios` de tu configuración, pide al conector de
Google Calendar los eventos de hoy, desde las 00:00 hasta las 24:00 de Chile
(`timeZone: America/Santiago`). Copia solo los de todo el día, que son los que traen `start.date`
en vez de `start.dateTime`. Si el conector falla con un calendario, ese calendario va con
`"leido": false`.

Correo. Busca con el conector de Gmail `from:no_responder@buk.cl newer_than:2d` y copia de cada
mensaje el asunto y la fecha, en formato ISO con su zona horaria. Si el conector falla, el correo va
con `"leido": false`.

Escribe `~/marcaje/hoy.json` con esta forma, sin agregar ni quitar nada de lo que trajiste:

```json
{
  "fecha": "2026-10-13",
  "turno": "entrada",
  "calendarios": [
    {"id": "persona@brinca.com", "leido": true,
     "eventos": [{"titulo": "Vacaciones", "todo_el_dia": true, "inicio": "2026-10-13", "fin": "2026-10-14"}]}
  ],
  "correo": {"leido": true,
             "comprobantes": [{"asunto": "Registro de ingreso, recinto: Brinca", "fecha": "2026-10-12T08:30:26-03:00"}]}
}
```

## Paso 3. Marca

Corre `python3 /opt/marcaje-buk/marcar.py <turno> hoy.json`, con el turno del paso 1.

| RESULTADO | Qué haces |
|---|---|
| `NO_TOCA` | Terminas, sin notificar: día libre o el turno ya estaba marcado |
| `ENSAYO` | Terminas, sin notificar. Es el modo de prueba: hizo todo menos apretar |
| `MARCADO` o `SIN_CONFIRMAR` | Sigues al paso 4 |
| `RECHAZADO`, `BLOQUEADO`, `ERROR` o `NO_MARCA` | Envías una notificación con la línea completa y terminas. No reintentas |

## Paso 4. Confirma con el comprobante

Espera tres minutos: corre `sleep 180` en segundo plano, con la opción `run_in_background` de la
herramienta Bash, y sigue cuando te avise que terminó. Un `sleep` en primer plano lo bloquea la nube.
Vuelve a buscar en Gmail
`from:no_responder@buk.cl newer_than:2d` y escribe `~/marcaje/correo.json` con la misma forma que la
parte `correo` de `hoy.json`. Corre `python3 /opt/marcaje-buk/marcar.py confirmar <turno> correo.json`.

| RESULTADO | Qué haces |
|---|---|
| `CONFIRMADO` | Terminas, sin notificar. El comprobante de Buk es el aviso |
| `SIN_COMPROBANTE` | Envías una notificación: «Marqué la <turno> pero no llegó el comprobante de Buk. Revisa tu asistencia en Buk.» No reintentas |

## Al terminar

Tu último mensaje empieza con una línea de resumen, por ejemplo «Entrada del 13-oct: marcada y
confirmada» o «Salida del 16-oct: no toca, feriado». Debajo van, textuales, las líneas `RESULTADO`
de cada paso que corriste.
