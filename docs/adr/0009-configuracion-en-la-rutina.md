# 0009, la configuración de cada persona va en sus rutinas, no en su entorno

Estado: aceptada, 12-oct-2026. Reemplaza de 0008 la configuración en el entorno.

## Contexto

0008 dejó el horario, el país y los calendarios de cada persona como variables de su entorno en
claude.ai, junto a su correo y su clave de Buk. Al escribir el código apareció el problema: el
formulario del entorno muestra todas sus variables en texto plano, también la clave. Para cambiar
un horario o agregar un calendario habría que abrir ese formulario, y quien lo abra, persona o
Claude, ve la clave.

## Decisión

- El entorno guarda solo `BUK_CORREO` y `BUK_CLAVE`. Una vez instalado, nadie vuelve a abrirlo
  salvo para cambiar la clave.
- El horario, el país, los calendarios y el modo van en las instrucciones de cada rutina, que las
  escriben en `configuracion.json` al empezar cada corrida (`rutina/plantilla.md`). Claude puede
  cambiarlas sin ver la clave.
- El modo por defecto es `ensayo`: hace todo menos apretar. Para marcar hay que escribir
  `"modo": "marcar"` a propósito.

## Consecuencias

- Cambiar el horario es actualizar las tres rutinas, no el entorno.
- Si la configuración no se entiende o falta, el script no marca y avisa (0001).

## Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| Variables del entorno (0008) | Cambiarlas obliga a abrir el formulario donde se ve la clave |
| Un archivo de configuración por persona en el repo | El repo es público |
