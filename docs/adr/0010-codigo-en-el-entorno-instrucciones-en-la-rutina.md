# 0010, el código llega con el entorno y las instrucciones van en la rutina

Estado: aceptada, 13-oct-2026. Reemplaza de 0008 la descarga durante la corrida.

## Contexto

0008 decidió que cada corrida descargara `marcar.py`, los feriados y las instrucciones desde la
versión `estable`. El 12-oct, en las dos primeras corridas de la rutina de salida, la nube de Claude
bloqueó esa descarga: «Code from External» la primera vez y «Untrusted Code Integration» la segunda.
En la primera, además, el propio Claude se negó a seguir instrucciones recién descargadas sin que
nadie las revisara. No se tocó Buk. El hito 1 había funcionado porque el código venía en el repo
clonado al empezar, no descargado en medio de la sesión.

## Decisión

- El script de configuración del entorno (`entorno/configuracion.sh`) descarga `marcar.py` y los
  feriados de este año y del siguiente a `/opt/marcaje-buk`, desde `estable`. Corre antes de que
  parta Claude, igual que la instalación de Playwright.
- Las instrucciones de cada corrida van completas en el texto de cada rutina: el nombre, la
  configuración y el cuerpo de `rutina/instrucciones.md`. La rutina no descarga nada.
- Si una descarga del script de configuración falla, el entorno igual se arma. La rutina ve que falta
  `marcar.py` y avisa, en vez de no partir sin que nadie se entere.

## Consecuencias

- Sigue sin hacer falta una cuenta de GitHub.
- Un cambio en `estable` le llega a cada persona cuando se rearma su entorno: claude.ai guarda el
  resultado del script de configuración unos siete días, o lo rehace cuando el script cambia. Un
  arreglo urgente se fuerza cambiando el script del entorno.
- Un cambio en las instrucciones obliga a actualizar las rutinas de cada persona. Lo hace Claude, con
  la herramienta de rutinas, sin abrir el entorno.

## Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| Descargar durante la corrida (0008) | La nube lo bloquea, y Claude desconfía de instrucciones recién descargadas |
| Clonar el repo en cada corrida, como en el hito 1 | Cada persona necesitaría una cuenta de GitHub conectada a Claude |
