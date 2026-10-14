# 0011, cada persona configura su país y su zona horaria

Estado: propuesta, 14-oct-2026. Se implementa cuando entre la primera persona que trabaje fuera de
Chile.

## Contexto

- `marcar.py` fija la zona horaria en `America/Santiago` y solo tiene feriados de Chile, en
  `feriados/AAAA.json`. Con otro país, `revisar` termina en `NO_MARCA`.
- La programación de las rutinas está calculada para Chile: la hora del turno más 3 y más 4 en UTC,
  para seguir su cambio de hora (0007).
- La guía de instalación mandaba a quien trabaja en otro país a escribirle al autor. Una
  herramienta para el equipo no puede depender de una persona para configurarse.
- Hoy nadie del piloto trabaja fuera de Chile.

## Decisión

1. La configuración de cada persona suma `zona`, con un nombre de zona horaria como
   `America/Lima`, además de `pais`. Si faltan, valen `America/Santiago` y `CL`.
2. La instalación calcula la programación de cada rutina desde la zona: un disparo por cada
   desfase con UTC que esa zona tenga durante el año. Si la zona no cambia de hora, es uno solo.
3. Chile sigue con su lista revisada a mano, con dos fuentes (0004).
4. Para otro país, el script de configuración del entorno descarga sus feriados del año en curso y
   del siguiente desde `date.nager.at`, y guarda solo los de tipo público. Corre antes de que parta
   la rutina, igual que la descarga de `marcar.py` (0010), así que no depende de una página a la
   hora de marcar.
5. Si esa lista no está, no marca y avisa (0001).
6. Mientras esto no se implemente, la instalación dice que por ahora solo funciona en Chile, sin
   derivar a nadie.

## Consecuencias

- Nadie le tiene que pedir nada al mantenedor para usarlo en otro país.
- Fuera de Chile, la lista viene de una sola fuente y sin revisión humana. Es menos que la de
  Chile, y se acepta porque la alternativa es que alguien mantenga una lista por país.
- La red del entorno de esas personas suma `date.nager.at`.
- La forma exacta de la respuesta de `date.nager.at` se verifica con un test sin red al
  implementar, como el resto de las lecturas.

## Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| Que la persona le escriba al mantenedor | Depende de una persona, que es justo lo que se quiere evitar |
| El calendario de feriados de Google del país, leído con el conector | Trae también fechas que no son feriado legal, y separarlas exige interpretar texto |
| Una lista revisada a mano por país, en el repo | Alguien tiene que mantenerla cada año, por cada país |
