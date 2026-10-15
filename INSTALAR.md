# Instalar marcaje-buk

Esta guía la sigue Claude cuando una persona de Brinca le pide, en la app de escritorio de Claude
(pestaña Code):

> Instala marcaje-buk desde github.com/marcelovenegas-brinca/marcaje-buk

Si eres esa persona y estás leyendo esto: no tienes que hacer nada más que pegar esa frase. Claude
te va a pedir solo lo que nadie puede hacer por ti.

Si eres Claude: sigue los pasos en orden. Habla con la persona en español, en frases cortas, sin
tecnicismos. Antes de cada acción que cambie algo en su cuenta, dile qué vas a hacer.

## Qué es, para contárselo a la persona en tres líneas

Tres rutinas de Claude marcan su entrada y su salida en Buk, en la nube, sin depender de su
computador. No marcan los fines de semana, los feriados de Chile ni los días que tenga anotados como
vacaciones, licencia, permiso o libre en su calendario. Si algo falla, no marcan y le avisan.

## Reglas que no se rompen durante la instalación

1. Nunca pidas, leas, escribas ni repitas la clave de Buk de la persona. La escribe ella, en el
   formulario del entorno. Si la pega en el chat, no la repitas y pídele que la cambie en Buk.
2. Nunca marques en Buk para probar. La prueba usa `python3 marcar.py probar`, que entra y sale sin
   apretar nada.
3. Las rutinas se crean en modo `marcar`: marcan desde el primer turno (ADR 0012). Antes de
   crearlas, la prueba del paso 5 tiene que haber dado `PRUEBA_OK`. La parte de la persona es
   verificar sus comprobantes los primeros días (ver «Verificar los primeros días»).
4. Cada rutina lleva solo los conectores de Gmail y Google Calendar, sin repositorio.
5. Si un paso no se puede cumplir, detente, explica qué falta y no sigas al siguiente.

## Paso 1. Revisar que tenga lo necesario

| Requisito | Cómo se revisa | Si falta |
|---|---|---|
| Plan Pro, Max o Team de Claude | Que puedas usar la herramienta de rutinas (`RemoteTrigger`) | Las rutinas no existen en el plan gratis. Detente. En el plan Team, si Claude responde que la organización desactivó las rutinas o las sesiones en la nube, detente: las activa el dueño de la organización |
| La cuenta de Claude donde la quiere | Sirve la personal o la de la empresa. Pregúntale con qué cuenta tiene abierta la app: ahí quedan las rutinas y el entorno | Si la quiere en otra, que cierre sesión, entre con esa y vuelva a pedir la instalación. Si sabe que se va a cambiar de cuenta pronto, explícale «Cambiar de cuenta de Claude» y que elija: instalar ahora y de nuevo el día del cambio, o esperar a ese día |
| Gmail y Google Calendar de Brinca conectados, aunque use su cuenta personal de Claude | Carga la skill `schedule`: trae la lista de conectores con su `connector_uuid`, y la de entornos con su `id` | Que los conecte en https://claude.ai/customize/connectors con su cuenta de Brinca, y vuelva a pedir la instalación. En el plan Team, si no aparecen para conectar, el dueño de la organización tiene que agregarlos primero |
| Su clave de Buk | Pregúntale si la sabe | Que la recupere en Buk antes de seguir |

## Paso 2. Tres preguntas

1. Horario. El de Brinca es lunes a jueves de 08:30 a 18:00 y viernes de 08:30 a 14:30. Pregunta
   si es el suyo. Si no, anótalo con el formato `L-J 08:30-18:00; V 08:30-14:30` (L lunes, M
   martes, X miércoles, J jueves, V viernes).
2. País. Por ahora funciona solo en Chile. Si trabaja en otro país, detente y explícale que todavía
   no está disponible: el ADR 0011 del repo describe cómo se va a sumar.
3. Calendarios y vacaciones. Con el conector de Calendar, lista sus calendarios. El de Brinca es
   el que tiene su correo de Brinca como `id`. Pregunta si anota días libres en otro calendario que
   aparezca en la lista, como uno personal, y súmalo. Pregunta por sus próximas vacaciones, licencias
   o permisos. Por cada uno, ofrece crear en su calendario de Brinca un evento de todo el día
   llamado «Vacaciones», «Licencia», «Permiso» o «Libre», y créalo solo si dice que sí.

## Paso 3. Que los comprobantes de Buk lleguen al correo de Brinca

Cada vez que alguien marca, Buk manda un comprobante desde `no_responder@buk.cl`. Las rutinas lo
usan para saber si un turno ya está marcado y para confirmar cada marca, y solo pueden leer su
correo de Brinca.

Busca con el conector de Gmail `from:no_responder@buk.cl newer_than:30d`.

- Si aparecen comprobantes, sigue al paso 4.
- Si no aparece ninguno, pregúntale a qué correo le llegan. Si llegan a un correo personal de
  Gmail, guíala para crear un filtro de reenvío en ese correo. Lo hace ella, en su navegador:
  1. Configuración, «Ver todos los ajustes», «Filtros y direcciones bloqueadas», «Crear un filtro».
  2. En «De» escribe `no_responder@buk.cl` y aprieta «Crear filtro».
  3. Marca «Reenviarlo a» y elige su correo de Brinca. Si no aparece, aprieta «Añadir dirección de
     reenvío», escribe su correo de Brinca y confirma. Gmail manda un código a ese correo: búscalo
     con el conector, `from:forwarding-noreply@google.com newer_than:1d`, y díselo. Con el código
     verificado, vuelve a crear el filtro.
  4. Google puede pedirle que verifique su identidad. Eso lo hace ella.

  El filtro reenvía solo los correos de Buk, nada más. Si no quiere crearlo, detente: sin
  comprobantes, la rutina no puede saber si ya marcó a mano y podría marcar dos veces.

## Paso 4. El entorno, donde vive su clave

Pídele que cree un entorno en la nube. En la app de escritorio: pestaña Code, el selector de entorno
debajo del cuadro de texto, «Nube», «Agregar entorno en la nube». Dale estos valores para copiar:

| Campo | Valor |
|---|---|
| Nombre | `marcaje-buk` |
| Acceso a la red | Personalizado |
| Dominios permitidos, uno por línea | `brinca.buk.cl`, `dxcgedrrxtox6.cloudfront.net`, `api.boostr.cl`, `cdn.playwright.dev`, `playwright.download.prss.microsoft.com`, `playwright.azureedge.net` |
| Lista predeterminada de gestores de paquetes | Marcada |
| Variables de entorno | `BUK_CORREO=` seguido del correo con que entra a Buk, y en otra línea `BUK_CLAVE=` seguido de su clave. Esta línea la escribe ella |
| Script de configuración | El contenido de `entorno/configuracion.sh` de este repo, tal cual |

`dxcgedrrxtox6.cloudfront.net` es de donde Buk sirve el código de su página. Sin él la página carga
y el botón se ve, pero apretarlo no envía la marca.

Explícale que esas variables solo las ve ella, y que una vez creado no hay que volver a abrir el
entorno salvo para cambiar la clave. Cuando lo guarde, carga de nuevo la skill `schedule` y toma el
`id` del entorno `marcaje-buk`.

## Paso 5. La prueba que no marca

Revisa la hora con `date -u +%Y-%m-%dT%H:%M:%SZ` y crea una rutina de una sola corrida, para dentro
de dos minutos:

- Nombre: `Marcaje Buk: prueba (no marca)`.
- Entorno: el `id` del paso 4. Sin repositorio. Sin conectores: una rutina creada sin indicarlos se
  lleva todos los de la persona, así que justo después de crearla actualízala con
  `"clear_mcp_connections": true`. Modelo `claude-sonnet-5`. Herramientas: `Bash` y `Read`.
- Instrucciones:

```text
Prueba de marcaje-buk: comprueba que este entorno entra a Buk, SIN marcar. El script de configuración del entorno ya instaló marcar.py en /opt/marcaje-buk. Corre:

python3 /opt/marcaje-buk/marcar.py probar

Si /opt/marcaje-buk/marcar.py no existe, dilo y termina. Termina con la línea que empieza con RESULTADO, textual. No muestres BUK_CORREO ni BUK_CLAVE, no descargues nada, no corras otros modos y no reintentes.
```

Espera a que corra y lee el resultado con `list_runs` y `get_run_log`.

| RESULTADO | Qué significa | Qué haces |
|---|---|---|
| `PRUEBA_OK` | Entró a Buk, ve los botones y la página tiene el código que envía la marca | Sigue al paso 6 |
| `ERROR: Buk no aceptó el inicio de sesión` | El correo o la clave del entorno están mal | Que los corrija en el entorno, y repite la prueba |
| `ERROR: la página de Buk cargó sin su código` | La red del entorno no deja descargar el código de Buk | Que revise los dominios permitidos del paso 4. El mensaje dice cuál falta. Repite la prueba |
| `BLOQUEADO` | Buk pidió un código o entrar con Google | Detente. Explícale que la rutina no puede responder esa verificación, y que se lo cuente a quien le compartió marcaje-buk |
| Otro `ERROR` o ninguna línea | Algo del entorno | Muéstrale el error y detente |

## Paso 6. Las tres rutinas

Arma el texto de cada rutina como dice `rutina/plantilla.md`: el nombre de la persona, su
configuración en una línea y el cuerpo de `rutina/instrucciones.md`. La configuración:

```json
{"horario": "<su horario>", "pais": "CL", "calendarios": ["<su calendario de Brinca>", "<otros, si los hay>"], "modo": "marcar"}
```

Crea una rutina por cada combinación distinta de turno y hora. Los días con la misma hora van
juntos. Cada turno dispara dos veces, a la hora de Chile más 3 y más 4 en UTC, para seguir el cambio
de hora. Con el horario de Brinca quedan estas tres:

| Nombre | Programación (UTC) |
|---|---|
| `Marcaje Buk: entrada` | `30 11,12 * * 1-5` |
| `Marcaje Buk: salida de lunes a jueves` | `0 21,22 * * 1-4` |
| `Marcaje Buk: salida del viernes` | `30 17,18 * * 5` |

Para otro horario: una entrada a las 09:00 de lunes a viernes es `0 12,13 * * 1-5`. En cron, lunes
es 1 y viernes es 5.

Todas: entorno `marcaje-buk`, sin repositorio, modelo `claude-sonnet-5`, herramientas `Bash`,
`Read` y `Write`, y como conectores solo Gmail y Google Calendar. Una rutina creada sin indicar
conectores se lleva todos los de la persona: indica esos dos de forma explícita, con su
`connector_uuid`, su nombre y su dirección.

## Paso 7. Cerrar

Dile a la persona, en una tabla corta:

- Qué quedó instalado, con el enlace a cada rutina.
- Que marca sola desde el próximo turno, y cuál es.
- Que desde ahora deja de marcar a mano. Si un día quiere marcar a mano, que lo haga antes de la
  hora del turno: la rutina ve el comprobante y no marca encima. Después de la rutina quedarían dos
  marcas.
- Que su parte es verificar durante la primera semana: por cada turno le tiene que llegar el
  comprobante de Buk. Si un turno no lo trae, que revise su asistencia en Buk, marque a mano si
  falta y se lo cuente a quien le compartió marcaje-buk.
- Que le puede pedir a Claude «revisa mi marcaje de hoy».
- Que para vacaciones basta con anotarlas en su calendario de Brinca con una de las cuatro
  palabras, o pedírselo a Claude.
- Que las rutinas viven en la cuenta de Claude con que la instaló. Si se cambia de cuenta, por
  ejemplo de la personal a la de la empresa, tiene que instalarla de nuevo en la nueva (ver
  «Cambiar de cuenta de Claude»).
- Que si algo falla le llega una notificación de Claude, y que el comprobante de Buk sigue siendo
  la prueba de cada marca.

## Después de instalar

### Verificar los primeros días y revisar el marcaje

Con `list_runs` y `get_run_log` de cada rutina, muéstrale la línea de resumen y las líneas
`RESULTADO` de las corridas del día, y busca con el conector de Gmail
`from:no_responder@buk.cl newer_than:1d`. Un turno bueno termina en `CONFIRMADO` en su hora, con su
comprobante, o en `NO_TOCA` cuando no tocaba. Si un turno quedó sin comprobante, que revise su
asistencia en Buk y marque a mano si falta.

### Dejar de marcar sin desinstalar

Si la persona quiere que las rutinas sigan corriendo pero sin apretar, por ejemplo mientras se
revisa una falla, actualiza las instrucciones de sus rutinas cambiando `"modo": "marcar"` por
`"modo": "ensayo"`: hacen todo menos apretar el botón. Para volver, al revés.

### Cambiar el horario o los calendarios

Actualiza las instrucciones de las tres rutinas con la configuración nueva y, si cambió una hora,
su programación. No hace falta abrir el entorno.

### Cambiar de cuenta de Claude

Las rutinas y el entorno no se mueven de una cuenta a otra: se instala de nuevo, desde el paso 1,
en la cuenta nueva. Antes, la persona pausa las tres rutinas de la cuenta anterior en
https://claude.ai/code/routines. Si quedan activas las de las dos cuentas, las dos corren el mismo
turno a la misma hora y pueden marcarlo dos veces.

Cuando la cuenta anterior se cancela, sus rutinas dejan de correr sin avisar. Por eso el cambio se
hace el mismo día en que la persona empieza a usar la cuenta nueva, para que no quede un turno sin
marcar.

### Cambiar la clave de Buk

Lo hace la persona, en el entorno `marcaje-buk`, editando la línea `BUK_CLAVE=`.

### Pausar o desinstalar

Las rutinas se pausan o se borran en https://claude.ai/code/routines. Borrarlas es decisión de la
persona: pregúntale antes.
