# 0003, marca con un navegador, no imitando el formulario

Estado: aceptada, 25-sep-2026

## Contexto

Hay dos maneras de marcar desde un servidor:

1. Abrir un navegador invisible, entrar y apretar el botón, como lo haría Marcelo.
2. Imitar lo que el navegador le manda a Buk: una petición web directa, sin navegador.

La segunda es más liviana, pero el botón de Buk no es un formulario simple. Tiene
`type="button"`, lo maneja JavaScript, muestra «Preparando marcaje…» y manda campos de latitud y
longitud. La petición real no está documentada: habría que copiarla de la red del navegador, y
Buk puede cambiarla sin aviso.

## Decisión

Marca con un navegador invisible (Chromium, manejado con Playwright). Entra con usuario y clave,
va al portal, aprieta el botón del turno y lee el mensaje que Buk muestra.

## Consecuencias

- Si Buk cambia su código interno pero el botón sigue ahí, sigue funcionando.
- Si Buk cambia el botón, falla con un aviso claro en vez de marcar mal.
- Cada corrida instala un navegador, lo que toma un par de minutos. Está dentro del presupuesto de
  0002.
- No se inventa una ubicación. Si Buk la exige, el navegador no la entrega y la marca falla con
  aviso. Se sabrá con la primera marca real.

## Alternativas descartadas

- Petición web directa: frágil ante cambios internos de Buk y obliga a mantener una copia de un
  protocolo ajeno.
