# Marcaje en Buk

Marca la entrada y la salida de Marcelo Venegas en el portal de Buk de Brinca, todos los días
hábiles, desde una rutina de Claude en la nube. No depende del computador.

> Estado: en construcción. La versión que marca hoy es la del Mac, en `mac/`. Este README se
> completa paso a paso; las secciones de uso se escriben cuando exista lo que describen.

## El problema

Marcelo tiene que marcar entrada y salida en el portal de Buk de Brinca todos los días hábiles, y
se le olvida. Son dos clics al día, unos 450 al año, y cada olvido se corrige a mano después.

Entre el 22 y el 25 de septiembre de 2026 funcionó una primera versión en el Mac. Marcó bien, pero
depende de que el Mac esté encendido y con Chrome abierto, y falló cinco veces por causas del Mac:
el Escritorio protegido por macOS, el Mac dormido, sin red al despertar, una ventana de Meet
adelante. Este repo lleva el marcaje a la nube.

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

1. Entra a Buk con el correo y la clave de la persona, que viven solo en su entorno de Claude.
2. Aprieta el botón del turno en el portal.
3. Lee la respuesta de Buk y la clasifica en una de tres: marcado, rechazado o sin confirmar.
4. Espera el comprobante que Buk manda por correo y lo usa como confirmación. La sesión de la
   rutina en claude.ai queda como registro de lo que hizo y por qué (ADR 0007).

Un «sin confirmar» cuenta como intento: no se reintenta ese día, porque pudo haber entrado.

### Cómo avisa

| Qué pasó                                   | Cómo se entera Marcelo                                                 |
| ------------------------------------------ | ---------------------------------------------------------------------- |
| Marcó                                      | Buk manda su comprobante al correo personal                            |
| Falló, fue rechazado o quedó sin confirmar | La rutina le avisa                                                     |
| La rutina ni siquiera corrió               | No llega el comprobante de Buk. Healthchecks queda para después (ADR 0006) |

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

- Buk sí deja entrar desde la nube de Claude sin pedir verificación, respondido el 11-oct en el
  hito 1: la prueba entró con correo y clave, vio los botones de entrada y salida, y salió sin
  marcar (`RESULTADO PRUEBA_OK`).
- Buk sí acepta una marca sin ubicación, respondido el 2-oct por la versión del Mac: avisó «No
  pudimos obtener tu ubicación exacta. Puedes marcar igualmente», y el comprobante muestra la
  entrada registrada a las 08:30:26. Queda por decidir en el paso 5 cómo se trata ese aviso.
- Cómo se confirma una marca desde el servidor. Entre el 29-sep y el 5-oct el mensaje en pantalla
  falló tres veces como confirmación y el comprobante que Buk manda por correo acertó las tres.
