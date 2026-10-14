# 0012, la instalación deja las rutinas marcando desde el primer día

Estado: aceptada, 14-oct-2026. Cambia de 0007 el ensayo antes de marcar.

## Contexto

0007 pedía unos días de ensayo, haciendo todo menos apretar, antes de que las rutinas marcaran.
Servía para comparar con la versión del Mac, que seguía marcando. Para el equipo esa comparación no
existe: un ensayo solo muestra que la rutina entra a Buk y encuentra el botón, y eso ya lo comprueba
la prueba de la instalación. Lo que un ensayo no puede mostrar es si la marca llega a Buk, y eso
solo lo dice un comprobante real.

Además, mientras dura el ensayo la persona sigue marcando a mano, que es justo lo que la
herramienta viene a quitar.

## Decisión

- La instalación crea las rutinas en modo `marcar`. Marcan desde el primer turno.
- Antes de crearlas, la prueba de la instalación (`probar`) tiene que dar `PRUEBA_OK`: entra a Buk,
  ve los botones y la página tiene el código que envía la marca.
- La persona deja de marcar a mano desde la instalación, y durante la primera semana verifica que
  le llegue el comprobante de Buk de cada turno. Si uno falta, revisa su asistencia en Buk y marca
  a mano.
- El modo `ensayo` sigue existiendo, para dejar de marcar sin desinstalar.

## Consecuencias

- La primera marca real ocurre el mismo día de la instalación, o al día siguiente.
- Si algo falla, la falla aparece en un turno real. Lo cubren las reglas de 0001: ante la duda no
  marca y avisa, y un turno sin comprobante también avisa.
- La verificación pasa de la herramienta a la persona, solo la primera semana.

## Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| Ensayo de unos días antes de marcar (0007) | No muestra lo único que falta saber, si la marca llega, y mantiene a la persona marcando a mano |
| Marcar sin pedir verificación | Una falla silenciosa en los primeros días sería una marca que falta y que nadie ve |
