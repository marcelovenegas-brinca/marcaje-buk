# Plantilla de las instrucciones de cada rutina

Es el texto que va en el campo de instrucciones de cada una de las tres rutinas de una persona. Lo
único que cambia entre personas es lo que está entre `<>`. La instalación lo completa; nadie lo
escribe a mano.

Las tres rutinas usan el mismo texto. Lo que cambia es su programación, en UTC, con dos disparos
por turno para seguir el cambio de hora de Chile (ADR 0007):

| Rutina | Programación por defecto |
|---|---|
| Entrada | `30 11,12 * * 1-5` |
| Salida de lunes a jueves | `0 21,22 * * 1-4` |
| Salida del viernes | `30 17,18 * * 5` |

La rutina no tiene repositorio y lleva solo los conectores de Gmail y Google Calendar (ADR 0008).

## El texto

```text
Eres la rutina de marcaje en Buk de <nombre>.

1. Prepara la carpeta. Corre, en un solo comando:

mkdir -p ~/marcaje/feriados ~/marcaje/rutina && cd ~/marcaje && R=https://raw.githubusercontent.com/marcelovenegas-brinca/marcaje-buk/estable && curl -fsSL $R/marcar.py -o marcar.py && curl -fsSL $R/rutina/instrucciones.md -o rutina/instrucciones.md && Y=$(TZ=America/Santiago date +%Y) && for A in $Y $((Y+1)); do curl -fsSL $R/feriados/$A.json -o feriados/$A.json || true; done

Si falla, no sigas: envía una notificación que diga «No pude descargar marcaje-buk» y termina.

2. Escribe ~/marcaje/configuracion.json con exactamente esto:

<configuración en una línea, por ejemplo {"horario": "L-J 08:30-18:00; V 08:30-14:30", "pais": "CL", "calendarios": ["persona@brinca.com"], "modo": "ensayo"}>

3. Lee ~/marcaje/rutina/instrucciones.md y síguelo al pie de la letra, trabajando desde ~/marcaje.
```
