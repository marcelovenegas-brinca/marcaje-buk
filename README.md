# Marcaje en Buk

Marca la entrada y la salida en Buk de cada persona que lo instala, todos los días hábiles, desde
rutinas de Claude en la nube. No depende del computador de nadie.

> Estado: marca de verdad desde el 13-oct-2026, y en piloto con parte del equipo de Brinca. Para
> instalarlo, ver [`INSTALAR.md`](INSTALAR.md).

## El problema

Quien trabaja con Buk marca su entrada y su salida en el portal todos los días hábiles. Es un gesto
chico, pero se repite cientos de veces al año, y se olvida. Un olvido no desaparece: se vuelve una
regularización manual. La persona pide corregir la marca, y administración y finanzas la revisa, la
corrige y la cuadra con la nómina.

| Al año | 1 persona | 5 personas | 10 personas |
|---|---|---|---|
| Marcas | 472 | 2.360 | 4.720 |
| Clics | 1.416 a 2.832 | 7.080 a 14.160 | 14.160 a 28.320 |
| Horas marcando | 8 a 16 | 39 a 79 | 79 a 157 |
| Horas en regularizaciones | 3 a 8 | 15 a 40 | 30 a 80 |

Los supuestos detrás de la tabla:

- 236 días hábiles: 261 de lunes a viernes en 2026, menos 10 feriados que caen en día hábil y 15
  días de vacaciones. Dos marcas por día.
- 3 clics por marca con la sesión abierta, y 6 cuando hay que entrar con correo y clave.
- 1 a 2 minutos por marca, contando el cambio de contexto.
- 1 a 2 olvidos por persona al mes, y 15 a 20 minutos por regularización entre la persona y
  administración.

El número que más pesa es el de regularizaciones, y es el más fácil de medir: basta contar cuántas
procesa administración en un mes.

## Qué hace

Cada persona tiene tres rutinas de Claude en la nube: la entrada, la salida de lunes a jueves y la
salida del viernes. En cada turno:

1. Revisa que hoy toque marcar: no es fin de semana ni feriado, y la hora calza con el turno.
2. Revisa los calendarios de la persona y los comprobantes de Buk que ya tiene en el correo: si hoy
   es un día libre o el turno ya está marcado, no hace nada.
3. Entra a Buk con el correo y la clave de la persona, que viven solo en su entorno de Claude, y
   aprieta el botón del turno.
4. Espera el comprobante que Buk manda por correo y lo usa como confirmación.

Las decisiones las toma `marcar.py`, con reglas probadas. Claude solo trae los datos de los
calendarios y del correo, corre los comandos y avisa (ADR 0007).

## La regla que gobierna todo

Ante la duda, no marca.

El registro de asistencia es un documento laboral. Una marca de más, en un día que no se trabajó,
afirma algo falso. Una marca que falta se corrige a mano en un minuto. Por eso cada verificación,
cuando no puede decidir, falla hacia no marcar, y avisa.

## Cuándo marca

| Turno   | Lunes a jueves | Viernes |
| ------- | -------------- | ------- |
| Entrada | 08:30          | 08:30   |
| Salida  | 18:00          | 14:30   |

Es el horario de Brinca, y cada persona puede tener el suyo. Siempre en hora de Chile, también
cuando el país cambia de horario.

## Cuándo no marca

| Situación | Qué hace |
| --- | --- |
| Fin de semana | No marca |
| Feriado en Chile | No marca |
| Falta la lista de feriados del año | No marca y avisa |
| Día libre en alguno de sus calendarios: un evento de todo el día con vacaciones, licencia, permiso o libre | No marca |
| No pudo leer alguno de sus calendarios | No marca y avisa |
| Ese turno ya se marcó hoy, también a mano | No marca |
| La rutina llegó más de 30 minutos tarde a la hora del turno | No marca y avisa. Marcar a destiempo sería registrar una hora falsa |
| Buk pide un código o una verificación extra al entrar | No marca y avisa |
| La página de Buk cargó sin su código | No marca y avisa qué dominio falta |

## De dónde salen los feriados

La lista de cada año vive en el repo, en `feriados/AAAA.json`, armada desde dos fuentes con la
fuente de cada fecha. Así el marcaje no depende de que una página responda justo a la hora de
marcar (ADR 0004). El mantenedor la revisa cada diciembre para el año siguiente, y también si una
ley agrega o mueve un feriado durante el año. Si llega un año sin lista, no marca.

Por ahora funciona solo en Chile. El ADR 0011 describe cómo se suma otro país sin depender del
mantenedor.

## Cómo avisa

| Qué pasó | Cómo se entera la persona |
| --- | --- |
| Marcó | Buk le manda su comprobante al correo |
| Falló, fue rechazado o quedó sin confirmar | La rutina le manda una notificación |
| La rutina ni siquiera corrió | No le llega el comprobante de Buk |

Un «sin confirmar» cuenta como intento: no se reintenta ese día, porque pudo haber entrado.

## Lo que no hace

- No corrige marcas pasadas ni marca días anteriores.
- No inventa una ubicación. Buk acepta la marca sin ella.
- No guarda la clave en ningún archivo, ni la imprime, ni siquiera en los errores.
- No decide si la persona trabajó: eso lo dicen sus calendarios. Si está enferma y no lo anota,
  marca.

## Cómo sabremos que funciona

| Criterio | Umbral |
|---|---|
| Días hábiles con sus dos turnos resueltos | Todos, durante cuatro semanas seguidas. Resuelto es marcado y confirmado por Buk, u omitido con un motivo válido |
| Marcas en días no trabajados | Cero. Una sola lo detiene todo hasta entender por qué |
| Fallas avisadas | Todas, el mismo día |
| Corridas que no ocurrieron y nadie supo | Cero |

## Lo que se aprendió en el camino

- Buk deja entrar desde la nube de Claude con correo y clave, sin pedir verificación extra.
- Buk acepta una marca sin ubicación. Avisa «No pudimos obtener tu ubicación exacta. Puedes marcar
  igualmente», y la marca entra.
- El mensaje en pantalla no sirve como confirmación. En la primera versión falló 5 de 11 veces, y
  las 5 marcas sí habían entrado. El comprobante que Buk manda por correo acertó siempre.
- La red de la nube tiene que dejar pasar el dominio desde donde Buk sirve el código de su página.
  Sin él, el botón se ve pero no envía nada. Cada falla real está en
  [`docs/modos-de-falla.md`](docs/modos-de-falla.md).

## Instalarlo

Hace falta un plan Pro o Max de Claude, los conectores de Gmail y Google Calendar de Brinca, y la
clave de Buk. No hace falta cuenta de GitHub ni instalar nada en el computador. En la app de
escritorio de Claude, pestaña Code, se pega:

> Instala marcaje-buk desde github.com/marcelovenegas-brinca/marcaje-buk

Claude sigue [`INSTALAR.md`](INSTALAR.md) y pide solo lo que nadie puede hacer por la persona.

## Cómo está hecho

| Ruta | Qué es |
|---|---|
| `marcar.py` | El script que decide y aprieta, el mismo para todos |
| `rutina/` | Lo que hace cada rutina en cada corrida, y cómo se arma su texto |
| `entorno/configuracion.sh` | El script del entorno de cada persona: instala Playwright y descarga `marcar.py` y los feriados |
| `feriados/` | La lista de feriados de cada año, con sus fuentes |
| `tests/` | 101 pruebas sin red: horarios, cambio de hora, feriados, calendarios y lectura de Buk |
| `docs/adr/` | Las decisiones de diseño, con su porqué y lo que se descartó |
| `docs/modos-de-falla.md` | Cada falla real: síntoma, causa y qué se hizo |
