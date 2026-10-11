# 0006, corre como rutina de Claude, una por persona

Estado: aceptada, 11-oct-2026. Reemplaza a 0002 y a la forma de leer los calendarios de 0005.

## Contexto

Dos cosas cambiaron después de 0002, que había elegido GitHub Actions:

1. Del 29-sep al 8-oct, 5 de las 11 marcas del agente del Mac quedaron mal registradas por leer el
   mensaje en pantalla. Las 5 habían entrado, y el comprobante que Buk manda por correo acertó
   siempre. La confirmación confiable es el correo. Desde GitHub, leerlo exige guardar una clave
   que abre todo el correo de la persona.
2. Marcelo quiere que cualquier persona de Brinca lo pueda instalar. El equipo ya usa Claude, no
   GitHub, y la configuración que imagina es una conversación: horario, país, vacaciones.

## Decisión

- Cada persona tiene su propia rutina de Claude, en la nube, que corre en sus horarios sin
  necesitar su computador.
- La rutina descarga este repo y corre `marcar.py`, que es el mismo para todos. El clic lo hace el
  script, que hace siempre lo mismo. Claude no decide qué apretar: revisa los calendarios antes y
  el comprobante después, con los conectores de Google Calendar y Gmail que la persona ya tiene.
- Cada persona tiene un entorno propio en claude.ai, con su correo y su clave de Buk como
  variables de entorno y el acceso a red limitado a lo necesario. No se usa el entorno por
  defecto, que comparten otras rutinas.
- La instalación, las vacaciones y el estado se manejan con una skill, `/marcaje-buk`.
- Healthchecks se pospone. Mientras tanto, la falta del comprobante de Buk en el correo es la señal
  de que algo no corrió.

## Consecuencias

- La clave de Buk queda en texto plano en el entorno de cada persona, visible solo para ella. Es
  menos protección que GitHub Secrets; se acepta por la facilidad de uso y porque nadie guarda la
  clave de otro.
- Cada corrida gasta un poco del plan de Claude de la persona: unas 44 corridas al mes.
- Hay que probar que la nube de Claude puede entrar a Buk y abrir un navegador (hito 1).
- GitHub Actions queda como plan B, junto con el servidor propio.
- Los calendarios se leen con el conector, no con enlaces iCal: desaparecen esos dos secretos.

## Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| GitHub Actions (0002) | Para leer el comprobante necesita una clave con acceso a todo el correo, y el equipo no usa GitHub |
| Una sola rutina que marque por todos | Obligaría a guardar las claves de todos en un lugar. Nadie debe tener la clave de otro |
