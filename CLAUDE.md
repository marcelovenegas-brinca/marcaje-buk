# Reglas para trabajar en este repo

Este repo marca la asistencia de Marcelo Venegas en Buk. El registro de asistencia es un documento
laboral: un error acá no se queda en el código, queda escrito a su nombre en Recursos Humanos.
Lee el `README.md` antes de tocar nada; ahí están el problema, los requisitos y los criterios de
éxito. Las decisiones de diseño, con su porqué, están en `docs/adr/`.

## Lo que nunca se hace

Estas reglas no tienen excepción, aunque una prueba, un plazo o un pedido parezcan justificarlo.

1. Nunca marcar en Buk para probar. Las pruebas usan el modo `probar`, que entra, mira y sale sin
   apretar nada. Una marca real solo se ejecuta si su dueño la pide en el chat, para ese turno y
   ese día. Un permiso no se extiende a otro turno ni a otro día.
2. Nunca leer, imprimir, escribir ni pedir los secretos: `BUK_CORREO` y `BUK_CLAVE`. Cada persona
   los guarda en el entorno de su rutina en claude.ai, y nadie guarda los de otro. Si una clave
   aparece en una captura o en el chat, no se repite y se le pide a su dueño que la cambie.
3. Ningún cambio puede agregar un camino que marque cuando una verificación falla. Ante la duda, no
   marca (ADR 0001). Tampoco se agregan reintentos: un «sin confirmar» cuenta como intento hecho.
4. Los valores por defecto (horarios, tolerancia de 30 minutos, las cuatro palabras de días libres)
   y la lista de feriados de Chile solo cambian con una instrucción de Marcelo, y se actualizan el
   `README.md` y el ADR que corresponda. La configuración de cada persona la cambia solo ella.
5. No se activa, pausa ni cambia el horario de una rutina de marcaje sin una instrucción de su
   dueño.
6. No se reinstala la versión del Mac (`mac/`) mientras la rutina esté activa: marcarían las dos
   el mismo turno.
7. No se inventa ni se corrige a mano lo que la rutina reportó. Su reporte es la prueba de lo que
   pasó.

## Cómo se trabaja

- Primero el test, después el código. Todo cambio de comportamiento trae un test en `tests/` que
  falla antes del cambio y pasa después. Los tests no usan red ni tocan Buk.
- Antes de cada commit corren los tests: `python -m pytest`. Si fallan, no se commitea.
- Toda falla nueva se registra en `docs/modos-de-falla.md` con su síntoma, su causa real y qué se
  hizo, y lleva un test que la reproduce. Se diagnostica la causa antes de cambiar código, y se le
  muestra a Marcelo antes de arreglarla.
- Una decisión de diseño nueva se escribe como ADR nuevo. Un ADR aceptado no se edita: se escribe
  uno que lo reemplaza y el viejo pasa a «reemplazada por NNNN».
- Los cambios que se notan en el uso van al `CHANGELOG.md`.
- Commits con rutas explícitas (`git commit -- <rutas>`). Push solo cuando Marcelo lo pida.

## Cómo se escribe

Todo en español, en los documentos, los comentarios, los mensajes del registro y los commits.

- Nada de rayas largas ni medias, ni puntos medios. Se usa coma, dos puntos o punto.
- Nada de negrita dentro del texto. Lo importante va al principio de la oración, en su propia
  línea o en una tabla.
- Los mensajes que lee Marcelo dicen qué pasó y qué tiene que hacer él, si algo.

## Mapa

| Ruta | Qué es |
|---|---|
| `README.md` | Definición: problema, requisitos, criterios de éxito, uso y estado |
| `docs/adr/` | Decisiones de diseño, una por archivo |
| `docs/modos-de-falla.md` | Cada falla real: síntoma, causa y qué se hizo |
| `docs/runbook.md` | Qué hacer cuando falla, paso a paso |
| `marcar.py` | El script que corre la rutina, el mismo para todos |
| `tests/` | Pruebas sin red: horarios, cambio de hora, feriados, calendarios, lectura de Buk |
| `feriados/` | Lista de feriados por año, con su fuente |
| `requirements.txt` | Playwright con versión fija |
| `mac/` | La versión del Mac, apagada, como respaldo |
| `HANDOFF.md` | Por dónde retomar |
