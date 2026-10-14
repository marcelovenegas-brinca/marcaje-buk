# 0005, los días libres salen de los dos calendarios

Estado: aceptada, 3-oct-2026. La forma de leer los calendarios, con enlaces iCal, la reemplaza 0006: ahora se leen con el conector de Google Calendar. Lo demás sigue vigente

## Contexto

En el Mac, que el equipo estuviera dormido o apagado era una señal indirecta de que la persona no
estaba trabajando. En un servidor esa señal desaparece: corre siempre. Algo tiene que decirle qué
días no son laborales, además de fines de semana y feriados.

La versión del Mac usaba `libres.txt`, un archivo que se editaba a mano. En dos semanas se usó una
sola vez, y llegó tarde: la entrada de ese día ya estaba marcada.

Quien lo usaba anota sus ausencias en dos calendarios: el de Brinca y el personal. Cualquiera de los dos
puede tener el día libre.

## Decisión

El servidor lee los dos calendarios, cada uno con su enlace privado en formato iCal, guardados como
secretos `CALENDARIO_ICAL_BRINCA` y `CALENDARIO_ICAL_PERSONAL`. Si hoy hay, en cualquiera de los
dos, un evento de todo el día cuyo título contiene una de estas cuatro palabras, sin importar
mayúsculas ni tildes, no marca:

- vacaciones
- licencia
- permiso
- libre

Si no puede leer uno de los dos, no marca y avisa, aunque el otro diga que es un día normal: no
sabe qué dice el que faltó (0001).

## Consecuencias

- Nadie mantiene un archivo aparte: basta con anotar el día en cualquiera de los dos
  calendarios.
- Si está enfermo y no lo anota, marca. Es el límite declarado en el README.
- Cada enlace iCal da lectura de todo ese calendario a quien lo tenga. Por eso son secretos, y el
  script solo lee los eventos de todo el día de la fecha de hoy, sin imprimir ni guardar ningún
  otro.
- Dos fuentes son dos puntos de falla: si cualquiera no responde, ese turno no se marca. Es el
  costo de no perder un día libre anotado en el calendario que falló.
- Google Workspace permite que el administrador desactive los enlaces iCal privados. Si en el
  calendario de Brinca no aparece la opción, se resuelve antes del paso 8 y se escribe una decisión
  nueva que reemplace esta.

## Alternativas descartadas

- `libres.txt` en el repo: obliga a hacer un commit por cada día libre, y se olvida.
- Leer solo un calendario: pierde las ausencias anotadas en el otro.
- El conector de Google Calendar: solo existe dentro de Claude, no en un servidor de GitHub.
