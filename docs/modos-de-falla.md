# Modos de falla

Cada falla real del marcaje en la nube: qué se vio, cuál fue la causa y qué se hizo. Una fila por
falla nueva, con el test que la reproduce. Las fallas de la versión del Mac, del 22-sep al 8-oct,
están en la tabla «Modos de falla conocidos» de su `agente.md`.

| Fecha | Síntoma | Causa real | Qué se hizo | Test |
|---|---|---|---|---|
| 11-oct-2026 | La primera prueba del hito 1 no alcanzó a empezar: «Setup script failed with exit code 1». El log muestra «Successfully installed playwright-1.63.0» y justo después «/usr/local/bin/python3: No module named playwright». No tocó Buk | La nube tiene más de un Python. `pip` a secas instaló Playwright en el 3.13, y `/usr/local/bin/python3`, el que corre después, es otro y no lo ve | El script de configuración usa `python3 -m pip` y quedó versionado en `entorno/configuracion.sh`. La segunda prueba, ocho minutos después, dio `RESULTADO PRUEBA_OK` | `tests/test_entorno.py` |
| 12-oct-2026 | Las dos primeras corridas de la rutina de salida no hicieron nada: «Code from External» y «Untrusted Code Integration». No tocó Buk | La nube bloquea que Claude descargue y corra código en medio de una corrida, y Claude desconfía de instrucciones recién descargadas | `marcar.py` y los feriados los descarga el script de configuración del entorno, y las instrucciones van completas en cada rutina (ADR 0010) | `tests/test_entorno.py` |
