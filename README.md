# Marcaje en Buk

Marca la entrada y la salida de Marcelo Venegas en el portal de Buk de Brinca, todos los días
hábiles, desde un servidor de GitHub. No depende del Mac.

> Estado: en construcción. La versión que marca hoy es la del Mac, en `mac/`. Este README se
> completa paso a paso; las secciones de uso se escriben cuando exista lo que describen.

## El problema

Marcelo tiene que marcar entrada y salida en el portal de Buk de Brinca todos los días hábiles, y
se le olvida. Son dos clics al día, unos 450 al año, y cada olvido se corrige a mano después.

Entre el 22 y el 25 de septiembre de 2026 funcionó una primera versión en el Mac. Marcó bien, pero
depende de que el Mac esté encendido y con Chrome abierto, y falló cinco veces por causas del Mac:
el Escritorio protegido por macOS, el Mac dormido, sin red al despertar, una ventana de Meet
adelante. Este repo lleva el marcaje a un servidor.

## La regla que gobierna todo

Ante la duda, no marca.

El registro de asistencia es un documento laboral. Una marca de más, en un día que no se trabajó,
afirma algo falso. Una marca que falta se corrige a mano en un minuto. Por eso cada verificación,
cuando no puede decidir, falla hacia no marcar, y avisa.

## Qué tiene que cumplir

### Cuándo marca

| Turno   | Lunes a jueves | Viernes |
| ------- | -------------- | ------- |
| Entrada | 08:30          | 08:30   |
| Salida  | 18:00          | 14:30   |

Siempre en hora de Chile, también cuando el país cambia de horario.

### Cuándo no marca

| Situación                                                         | Qué hace                                                            |
| ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| Fin de semana                                                     | No marca                                                            |
| Feriado en Chile                                                  | No marca                                                            |
| No pudo saber si hoy es feriado                                   | No marca y avisa                                                    |
| Día libre en el calendario de Brinca o en el personal: vacaciones, licencia, permiso o libre | No marca                                                            |
| No pudo leer alguno de los dos calendarios                        | No marca y avisa                                                    |
| Ese turno ya se marcó hoy                                         | No marca                                                            |
| Llegó más de 30 minutos tarde a la hora del turno                 | No marca y avisa. Marcar a destiempo sería registrar una hora falsa |
| Buk pide un código o una verificación extra al entrar             | No marca y avisa                                                    |

### De dónde salen los feriados

Una vez al año, en diciembre, se levanta la lista completa del año siguiente desde fuentes
oficiales de Chile y se guarda en el repo, en `feriados/AAAA.json`, con la fuente de cada fecha.
Es la lista que manda. Así el marcaje no depende de que una página responda justo a las 08:30.

La lista rara vez cambia durante el año, pero a veces sí: una ley puede agregar o mover un
feriado ya empezado el año. Por eso, una vez al mes, el servidor compara la lista guardada contra
una fuente en línea. Si difieren, no cambia nada solo: avisa, y la lista se corrige a mano con la
fuente a la vista. Si hoy aparece como feriado en cualquiera de las dos, no marca.

Si en diciembre no existe la lista del año siguiente, el servidor avisa. Si llega el 1 de enero
sin lista, no marca, porque no puede saber qué días son feriados.

### Cómo marca

1. Entra a Buk con el correo y la clave de Marcelo, que viven solo en GitHub Secrets.
2. Aprieta el botón del turno en el portal.
3. Lee la respuesta de Buk y la clasifica en una de tres: marcado, rechazado o sin confirmar.
4. Deja una línea en `registro.md` con la hora, el turno, el resultado y el texto de Buk.

Un «sin confirmar» cuenta como intento: no se reintenta ese día, porque pudo haber entrado.

### Cómo avisa

| Qué pasó                                   | Cómo se entera Marcelo                                                 |
| ------------------------------------------ | ---------------------------------------------------------------------- |
| Marcó                                      | Buk manda su comprobante al correo personal                            |
| Falló, fue rechazado o quedó sin confirmar | GitHub manda un correo                                                 |
| El servidor ni siquiera corrió             | Healthchecks.io manda un correo si a la hora esperada no recibió señal |

### Lo que no hace

- No corrige marcas pasadas ni marca días anteriores.
- No inventa una ubicación. Si Buk la exige para marcar, se decide aparte.
- No guarda la clave en ningún archivo, ni la imprime, ni siquiera en los errores.
- No decide si Marcelo trabajó: eso lo dicen sus calendarios. Si está enfermo y no lo anota, marca.

## Cómo sabremos que funciona

| Criterio | Umbral |
|---|---|
| Días hábiles con sus dos turnos resueltos | Todos, durante cuatro semanas seguidas. Resuelto es marcado y confirmado por Buk, u omitido con un motivo válido |
| Marcas en días no trabajados | Cero. Una sola lo detiene todo hasta entender por qué |
| Fallas avisadas | Todas, el mismo día |
| Corridas que no ocurrieron y nadie supo | Cero |

## Preguntas abiertas

- Si Buk deja entrar desde un servidor de GitHub sin pedir verificación. Se responde en el paso 8,
  con una prueba que no marca.
- Si Buk acepta una marca sin ubicación. Se responde con la primera marca real.
