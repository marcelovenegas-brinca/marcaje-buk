# 0002, corre en GitHub Actions

Estado: reemplazada por 0006, 11-oct-2026. Aceptada el 25-sep-2026

## Contexto

La primera versión corrió en el Mac, con `launchd` y el Chrome de Marcelo. Funcionó, pero falló
cinco veces en tres días por causas del Mac: el Escritorio protegido por macOS, el Mac dormido o
recién despertado sin red, y una ventana de Meet adelante. Además, con el Mac apagado no marca.

Marcelo quiere que corra solo, sin depender de su equipo.

## Decisión

Corre en GitHub Actions, en un repo privado propio, con:

- Dos horarios por turno, uno para el horario de verano de Chile y otro para el de invierno. El
  script revisa la hora de Chile y solo actúa el que corresponde.
- Partida unos 15 minutos antes, porque GitHub puede atrasar los trabajos programados. El script
  espera la hora exacta.
- Credenciales en GitHub Secrets: `BUK_CORREO`, `BUK_CLAVE`, `CALENDARIO_ICAL_BRINCA`,
  `CALENDARIO_ICAL_PERSONAL` y la dirección de Healthchecks.
- Una alarma en Healthchecks.io: cada corrida le avisa al empezar, y si a la hora esperada no
  recibió nada, manda un correo. Cubre lo que GitHub no puede avisar: que no corrió.

## Consecuencias

- La clave de Buk queda guardada en un servidor externo. GitHub Secrets la cifra y nadie puede
  leerla de vuelta, pero existe fuera del Mac. La clave vieja quedó expuesta el 24-sep y se cambia
  antes de guardarla.
- El repo es aparte de `Brinca_00`, porque el servidor descarga el repo completo junto con la
  clave. Así solo tiene acceso a este script.
- El servidor está en Estados Unidos. Queda por probar que Buk lo deje entrar (paso 8).
- Costo: dentro de los 2.000 minutos gratuitos al mes para repos privados. Se estima entre 900 y
  1.100.
- La versión del Mac se conserva en `mac/`, apagada, como respaldo.

## Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| Seguir en el Mac | Depende de que el Mac esté encendido, despierto y con Chrome |
| Rutina de Claude Code | No tiene un lugar cifrado para la clave, gasta del plan en cada corrida y pone un modelo de lenguaje a decidir cada vez sobre un documento laboral |
| Vercel | Sus funciones no están hechas para cargar un navegador completo. Habría que imitar el formulario de Buk (ver 0003) |
| Servidor propio o Raspberry Pi | Funciona, pero hay que mantenerlo. Queda como plan B, por decisión de Marcelo del 3-oct, si GitHub falla o Buk bloquea sus servidores |
| API oficial de Buk | La mejor opción, pero depende de Recursos Humanos. Si se habilita, esta decisión se reemplaza |
