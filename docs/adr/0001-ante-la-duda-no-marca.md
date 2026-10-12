# 0001, ante la duda, no marca

Estado: aceptada, 25-sep-2026. El `registro.md` como prueba y como estado lo reemplaza 0007

## Contexto

El registro de asistencia es un documento laboral. Los dos errores posibles no pesan lo mismo:

| Error | Qué afirma | Cómo se corrige |
|---|---|---|
| Marca de más | Que Marcelo trabajó un día que no trabajó, o a una hora que no es | Hay que explicarlo a Recursos Humanos. Es una afirmación falsa en un documento laboral |
| Marca que falta | Nada | Se marca a mano en un minuto |

La versión del Mac lo aprendió con casos: el 22-sep el registro dijo «marcado» por una salida que
Buk había rechazado, y el 23 y el 24 el script culpó a Buk de un cambio que no existía.

## Decisión

Toda verificación que no puede decidir falla hacia no marcar, y avisa. En concreto:

- Sin lista de feriados, sin calendario o sin red, no marca.
- Si el disparo llega más de 30 minutos tarde, no marca: sería registrar una hora falsa.
- Nunca reintenta. Un intento cuyo resultado no se conoce («sin confirmar») cuenta como hecho,
  porque pudo haber entrado, y una marca doble es peor que una faltante.
- «Marcado» se escribe solo cuando Buk lo confirma con su mensaje, nunca al apretar el botón.
- Cada corrida deja una línea en `registro.md`, en el repo: qué hizo y por qué. Ese registro es a
  la vez la prueba y el estado que evita marcar dos veces el mismo turno.

## Consecuencias

- Habrá días en que no marque aunque debía, y Marcelo tendrá que hacerlo a mano. Es el costo
  aceptado.
- Cada «no marco» tiene que avisar, o se vuelve una falla silenciosa. Por eso existe la alarma de
  Healthchecks (ver 0002).
- Ningún cambio de código puede agregar un camino que marque ante la duda. Es la primera regla de
  `CLAUDE.md`.

## Alternativas descartadas

- Reintentar si falla: arriesga una marca doble cuando el primer intento sí entró.
- Marcar tarde con la hora real: Buk registra la hora del clic, y una entrada a las 11:00 de un
  día que empezó a las 08:30 también es falsa.
