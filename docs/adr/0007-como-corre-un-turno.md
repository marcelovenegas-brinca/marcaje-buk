# 0007, cómo corre un turno en la rutina

Estado: aceptada, 12-oct-2026. Reemplaza de 0001 el `registro.md` como prueba y como estado. El ensayo antes de marcar lo cambia 0012.

## Contexto

El hito 1 mostró que la rutina entra a Buk desde la nube. Para que marque faltan cuatro cosas, y
cada una choca con algo ya decidido o con un dato nuevo:

1. La rutina no guarda nada entre corridas: cada sesión parte de cero. El `registro.md` de 0001,
   que era a la vez la prueba y el estado que evita marcar dos veces, obligaría a la rutina a
   escribir en el repo, que es público, la asistencia de cada persona. Y tiene que funcionar como
   una aplicación que cualquier persona de Brinca pueda usar, no solo quien la creó.
2. El perfil de Buk no le muestra al empleado sus marcas del día (revisado el 11-oct). El único
   lugar donde queda si un turno ya se marcó, también a mano, es el comprobante que Buk manda por
   correo.
3. Los comprobantes pueden llegar a un Gmail personal, y el conector de Gmail lee el de
   Brinca. El conector de Calendar sí ve los dos calendarios.
4. Las rutinas se programan en hora UTC, y Chile cambia de horario dos veces al año: el 5-abr y el
   6-sep en 2026, el 4-abr y el 5-sep en 2027.

## Decisión

### La decisión de marcar vive en el script, Claude solo trae datos

Cada turno corre en cuatro tiempos:

| Tiempo | Quién | Qué hace |
|---|---|---|
| 1. Revisar | `marcar.py revisar` | Sin red: fin de semana, feriado y hora de Chile. Responde qué turno toca, o que no toca ninguno |
| 2. Traer datos | Claude, con los conectores | Lee los eventos de todo el día de hoy en los dos calendarios y busca el comprobante de Buk de ese turno, de hoy. Lo escribe tal cual en `hoy.json` |
| 3. Marcar | `marcar.py entrada hoy.json`, o `salida` | Vuelve a revisar todo, aplica la regla de las cuatro palabras (0005) y la del comprobante, entra a Buk, aprieta y lee la respuesta |
| 4. Confirmar | Claude | Espera unos minutos y busca el comprobante. Si no llega, avisa |

Claude no interpreta los calendarios ni decide si hoy es libre: copia los títulos y el script
aplica la regla, que tiene tests. Si Claude no pudo leer un calendario o el correo, lo anota en
`hoy.json` y el script no marca.

### El estado es el comprobante

Un turno ya está marcado hoy si existe el comprobante de Buk de ese turno con la fecha de hoy.
Eso cubre también la marca hecha a mano.

### El registro es el historial de la rutina

No hay `registro.md`. Cada corrida queda guardada como una sesión en la cuenta de Claude de la
persona, que solo ella ve: qué turno revisó, qué decidió, por qué y qué respondió Buk. Ese es su
registro, y el comprobante de Buk es la prueba (0008). Nada de la asistencia de nadie se escribe
en el repo.

### Dos disparos por turno, uno por cada horario de Chile

| Turno | Disparos en UTC | En Chile con horario de verano | Con horario de invierno |
|---|---|---|---|
| Entrada, lunes a viernes | 11:30 y 12:30 | 08:30 y 09:30 | 07:30 y 08:30 |
| Salida, lunes a jueves | 21:00 y 22:00 | 18:00 y 19:00 | 17:00 y 18:00 |
| Salida, viernes | 17:30 y 18:30 | 14:30 y 15:30 | 13:30 y 14:30 |

El script mira la hora de Chile, no la de UTC. El disparo que cae una hora antes o una hora
después del turno es el del otro horario: termina sin hacer nada y sin avisar. Uno que llega más de
30 minutos tarde por otra causa no marca y avisa (0001).

Son tres rutinas por persona, porque una sola programación no puede mezclar las 18:00 con las
08:30 y las 14:30 sin disparar cada media hora, y el mínimo es una hora. Las tres usan las mismas
instrucciones: el script deduce el turno de la hora y del día.

### Avisos

La rutina avisa con una notificación de Claude solo cuando hay algo que hacer: no marcó por una
duda, quedó sin confirmar o no llegó el comprobante. Cuando marca y el comprobante llega, el aviso
es el mismo comprobante de Buk.

### Ensayo antes de marcar

Las rutinas parten en modo ensayo, que hace todo menos apretar el botón, mientras el Mac sigue
marcando. Durante unos días se compara lo que la rutina habría hecho con lo que hizo el Mac.
Recién entonces se apaga el Mac (regla 6 de `CLAUDE.md`) y la rutina pasa a marcar.

### El correo de los comprobantes

Si los comprobantes llegan a un correo que el conector no lee, un filtro en ese correo los reenvía
al de Brinca: todo lo que venga de `no_responder@buk.cl`, y nada más. Gmail exige verificar la
dirección de destino con un código que llega al correo de Brinca, y ese código se lee con el
conector. El filtro es una regla permanente en el correo de la persona: se crea solo con su
permiso explícito. La instalación (0008)
revisa a qué correo les llegan y, si hace falta, pide el permiso y arma el mismo filtro.

## Consecuencias

- Desaparece `registro.md`. La historia queda en las sesiones de la rutina y en los comprobantes.
- Si el reenvío se corta sin que nadie lo note, la rutina no ve una marca hecha a mano y puede
  marcar encima. Lo detecta el mismo día: después de marcar no llega el comprobante, y avisa.
- Son unos 88 disparos al mes por persona en vez de 44. La mitad termina en segundos.
- La regla de las cuatro palabras, la de la hora y la del comprobante quedan en el script, con
  tests. Lo que hace Claude es leer y copiar.

## Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| Un disparo por turno, y cambiar la hora a mano dos veces al año | El día del cambio no marcaría hasta que alguien lo arregle |
| Que Claude decida con los calendarios si hoy es libre | La regla quedaría sin test, y cada corrida podría leerla distinto |
| `registro.md` en el repo | La asistencia de cada persona quedaría en un repo público, y la rutina necesitaría permiso para escribir en él |
| Leer las marcas en Buk | El perfil del empleado no las muestra |

## Queda abierto

Buk guarda las vacaciones aprobadas de cada persona, y el script ya está dentro de Buk cuando
marca. Podría ser una tercera fuente de días libres, la oficial. Se evalúa en el hito 3.
