# Decisiones de diseño

Cada archivo registra una decisión: el contexto que la forzó, qué se decidió, qué consecuencias
trae y qué alternativas se descartaron. Una decisión no se edita cuando cambia: se escribe una
nueva que la reemplaza, y la vieja pasa a estado «reemplazada por NNNN». Así queda el porqué de
cada momento.

| # | Decisión | Estado |
|---|---|---|
| [0001](0001-ante-la-duda-no-marca.md) | Ante la duda, no marca | aceptada, el registro lo cambia 0007 |
| [0002](0002-github-actions.md) | Corre en GitHub Actions | reemplazada por 0006 |
| [0003](0003-navegador-y-no-http.md) | Marca con un navegador, no imitando el formulario | aceptada |
| [0004](0004-feriados-en-el-repo.md) | Los feriados viven en el repo, con control mensual | aceptada |
| [0005](0005-dias-libres-desde-el-calendario.md) | Los días libres salen de los dos calendarios, Brinca y personal | aceptada, la lectura la cambia 0006 |
| [0006](0006-rutina-de-claude-por-persona.md) | Corre como rutina de Claude, una por persona | aceptada, la instalación la cambia 0008 |
| [0007](0007-como-corre-un-turno.md) | Cómo corre un turno: el script decide, Claude trae los datos | aceptada |
| [0008](0008-como-lo-obtiene-cualquiera.md) | Cómo lo obtiene cualquier persona de Brinca | aceptada, la configuración la cambia 0009 |
| [0009](0009-configuracion-en-la-rutina.md) | La configuración de cada persona va en sus rutinas, no en su entorno | aceptada |
