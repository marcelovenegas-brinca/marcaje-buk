# 0008, cómo lo obtiene cualquier persona de Brinca

Estado: aceptada, 12-oct-2026. Reemplaza de 0006 la skill `/marcaje-buk` y la descarga del repo
con GitHub. La configuración en el entorno la reemplaza 0009, y la descarga durante la corrida, 0010.

## Contexto

Marcelo quiere compartirlo pronto con el equipo, y que cada persona lo use con su propia clave. Hay
cuatro datos que mandan:

1. El equipo no usa GitHub.
2. Brinca no tiene plan Team de Claude: cada persona tiene su plan personal. Algunos pasarán a
   Team, no todos.
3. Una rutina necesita una cuenta de GitHub para clonar un repo. El 12-oct se probó una rutina sin
   repo: corrió en una carpeta vacía y descargó desde `raw.githubusercontent.com` sin cuenta.
4. Una skill hay que instalarla en el computador de cada persona, y actualizarla en cada uno cuando
   cambia.

## Decisión

### El código es público

El código vive en el repo público `marcaje-buk`. El original, `buk-marcaje`, queda privado y
congelado desde el 12-oct con la historia completa. El público tiene la misma historia, sin dos
pasajes que no debían publicarse. Lo que no puede quedar público no se escribe acá (regla 8 de
`CLAUDE.md`).

### La rutina no clona el repo: descarga lo que necesita

Las rutinas no tienen repo. En cada corrida descargan `marcar.py`, la lista de feriados y las
instrucciones de la rutina desde la versión marcada `estable`. `estable` es una etiqueta de git que
mueve solo Marcelo, cuando una versión pasó sus tests y el ensayo. Lo que se sube a `main` no le
llega a nadie hasta entonces.

### La instalación es una frase

La persona abre la app de escritorio de Claude, en la pestaña Code, y pega:

> Instala marcaje-buk desde github.com/marcelovenegas-brinca/marcaje-buk

Claude lee `INSTALAR.md` del repo y la guía.

| Lo hace la persona | Lo hace Claude |
|---|---|
| Escribir su correo y su clave de Buk en el formulario del entorno | Revisar que tenga conectados Gmail y Calendar de Brinca |
| Aprobar el filtro de reenvío, si sus comprobantes llegan a otro correo | Dejar listo el entorno, salvo la clave |
| Contar su horario, su país y sus próximas vacaciones | Anotar esas vacaciones en su calendario de Brinca |
| | Correr la prueba que entra a Buk sin marcar, y crear las tres rutinas |

Las vacaciones de después se anotan en el calendario de Brinca con una de las cuatro palabras
(0005), a mano o pidiéndoselo a Claude en cualquier chat.

### La configuración de cada persona vive en su entorno

Su correo, su clave, su horario y su país son variables de su entorno: `BUK_CORREO`, `BUK_CLAVE`,
`MARCAJE_HORARIO` y `MARCAJE_PAIS`. Las instrucciones de la rutina son las mismas para todos.

### La trazabilidad no necesita un agente

| Pregunta | Dónde se responde |
|---|---|
| ¿Se marcó? | En el comprobante de Buk, que llega al correo como siempre. Es el registro oficial |
| ¿Por qué no se marcó? | En la notificación de Claude de ese día, y en la lista de rutinas de la cuenta, donde cada corrida dice qué decidió y por qué |
| ¿Qué marqué esta semana? | Cualquier chat de Claude con el conector de Gmail, leyendo los comprobantes |

### Lo que necesita cada persona

| Requisito | Por qué |
|---|---|
| Plan Pro o Max de Claude | Las rutinas en la nube no existen en el plan gratis |
| La app de escritorio de Claude | Para que Claude cree las rutinas durante la instalación |
| Gmail y Google Calendar de Brinca conectados en Claude | Para revisar el calendario y el comprobante |
| Su clave de Buk | La escribe ella, nadie más |

## Consecuencias

- Nadie necesita una cuenta de GitHub ni instalar nada en su computador.
- Un arreglo le llega a todos cuando Marcelo mueve `estable`, sin reinstalar. Un error también: por
  eso `estable` se mueve solo después de los tests y del ensayo, y ante la duda el script no marca
  (0001).
- Las rutinas siguen instrucciones que descargan del repo. Quien pueda escribir en el repo controla
  lo que hacen las rutinas de todos. Solo Marcelo tiene permiso de escritura, y así se mantiene.
- Cada persona gasta su propio plan: unas 88 corridas al mes, la mitad de segundos.
- Las rutinas de Claude están en vista previa. Si cambian, se ajusta `INSTALAR.md`.
- Por ahora solo Chile. Los feriados de otro país se agregan cuando alguien los necesite.

## Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| Un servidor que marque por todos | Alguien tendría las claves de todo el equipo (0006) |
| GitHub Actions | Cada persona necesitaría cuenta de GitHub y configurar secretos (0006) |
| Una skill o un plugin instalado | Un paso más en la instalación, y una copia que envejece en cada computador |
| Repo privado, con acceso por persona | Cada persona necesitaría cuenta de GitHub |
| Repo visible solo para Brinca | GitHub no lo permite sin una organización y cuentas para todos |
| Un agente para consultar la trazabilidad | No agrega nada a los tres lugares donde ya está |
