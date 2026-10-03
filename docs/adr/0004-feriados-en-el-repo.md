# 0004, los feriados viven en el repo, con control mensual

Estado: aceptada, 25-sep-2026

## Contexto

La versión del Mac consultaba cada mañana una página de feriados. El 23-sep la fuente oficial,
`apis.digital.gob.cl`, dejó de existir, y la segunda, `api.boostr.cl`, falló esa mañana por falta
de red. Consultar en línea justo a la hora de marcar agrega un punto de falla.

Los feriados de Chile casi no cambian durante el año, pero una ley puede agregar o mover uno con
el año ya empezado.

## Decisión

- La lista del año vive en el repo, en `feriados/AAAA.json`, con la fuente de cada fecha. Se
  levanta una vez al año, en diciembre, desde fuentes oficiales. Esa lista manda.
- Una vez al mes, un trabajo aparte la compara con una fuente en línea. Si difieren, avisa y no
  cambia nada solo.
- Si hoy es feriado en cualquiera de las dos, no marca.
- Si en diciembre falta la lista del año siguiente, avisa. Si llega enero sin lista, no marca.

## Consecuencias

- El marcaje diario no depende de ninguna página externa para los feriados.
- Una vez al año hay que actualizar la lista. El aviso de diciembre lo recuerda.
- Un feriado agregado por ley se detecta en el control mensual, o el mismo día si la fuente en
  línea ya lo trae.

## Alternativas descartadas

- Consultar en línea cada vez: falló el 23-sep.
- Calcular los feriados: San Pedro y San Pablo y el Encuentro de Dos Mundos se mueven según la ley
  19.973, y Semana Santa depende de la Pascua. Una lista revisada es más confiable que un cálculo.
