# Plantilla de las instrucciones de cada rutina

Es el texto que va en el campo de instrucciones de cada una de las rutinas de una persona. La
instalación lo arma; nadie lo escribe a mano. No se descarga durante la corrida (ADR 0010).

## Cómo se arma

```text
Eres la rutina de marcaje en Buk de <nombre>. Tu configuración, que escribes tal cual en ~/marcaje/configuracion.json:

<configuración en una línea>

Sigue estas instrucciones al pie de la letra.

<rutina/instrucciones.md, desde el párrafo que empieza con «`marcar.py` y los feriados ya están» hasta el final>
```

La configuración, en una línea (ADR 0009):

```json
{"horario": "L-J 08:30-18:00; V 08:30-14:30", "pais": "CL", "calendarios": ["persona@brinca.com"], "modo": "ensayo"}
```

## Programación

Las rutinas de una persona usan el mismo texto. Lo que cambia es su programación, en UTC, con dos
disparos por turno para seguir el cambio de hora de Chile (ADR 0007):

| Rutina | Programación por defecto |
|---|---|
| Entrada | `30 11,12 * * 1-5` |
| Salida de lunes a jueves | `0 21,22 * * 1-4` |
| Salida del viernes | `30 17,18 * * 5` |

Cada rutina va sin repositorio, en el entorno `marcaje-buk` de la persona, y con solo los conectores
de Gmail y Google Calendar (ADR 0008).
