# Skills de agentes

Este proyecto usa tres skills de agente provenientes del repositorio público
[`nschurmann/hola-ai`](https://github.com/nschurmann/hola-ai). Están instaladas
a nivel de proyecto, por lo que quedan versionadas junto al código y disponibles
para cualquiera que clone el repositorio.

## Skills instaladas

| Skill | Qué hace | Qué no hace |
|---|---|---|
| `backlog` | Convierte una idea o funcionalidad en un backlog de historias de usuario verticales y cortas. | No inventa requisitos, no crea historias técnicas, no estima. |
| `story` | Toma **una** historia y le añade 2–3 criterios de aceptación (Given/When/Then) y un mini plan de máximo 5 viñetas. | No escribe código. Si necesita más de 3 criterios, propone dividir la historia. |
| `pair` | Pair programming con TDD: un test → rojo → código mínimo → verde, y se detiene a esperar aprobación. | No hace commits, no modifica tests para que pasen, no añade cosas no pedidas. |

Las tres skills están pensadas para invocarse **manualmente**. Su frontmatter
incluye `disable-model-invocation: true`, así que el agente no las activa por su
cuenta.

## Flujo de trabajo

```text
/backlog  →  /story  →  /pair
  qué        qué exacto   cómo
```

La salida de cada skill es la entrada de la siguiente. Los bloques generados
están pensados para copiarse al gestor de tareas o al issue correspondiente.

## Cómo se instalaron

Se usó el CLI del ecosistema de skills (`npx skills`), apuntando a OpenCode y al
ámbito de proyecto:

```bash
DISABLE_TELEMETRY=1 npx -y skills add https://github.com/nschurmann/hola-ai \
  -a opencode \
  --skill backlog --skill story --skill pair \
  -y
```

Requisitos: Node.js 22.20 o superior y `npx` disponible.

El CLI descarga el repositorio, detecta las skills y copia los archivos a
`.agents/skills/`, que es una ruta que OpenCode descubre automáticamente
(compatibilidad). No requiere configuración adicional en `opencode.json`.

## Estructura en el proyecto

```text
.
├── .agents/
│   └── skills/
│       ├── backlog/
│       │   └── SKILL.md
│       ├── pair/
│       │   └── SKILL.md
│       └── story/
│           └── SKILL.md
└── skills-lock.json
```

- `.agents/skills/<id>/SKILL.md`: contenido de cada skill.
- `skills-lock.json`: registra la fuente, la ruta y el hash de cada skill para
  poder actualizarlas o restaurarlas.

## Cómo usarlas en OpenCode

En OpenCode V2 las skills no son comandos de barra (`/backlog`). Se invocan
mencionándolas en el prompt con su ID:

```text
@backlog quiero una app para registrar parcelas y tratamientos
```

```text
@story <pegar la historia del backlog>
```

```text
@pair <pegar el bloque generado por story>
```

También se puede pedir explícitamente al agente que cargue una skill por nombre
(por ejemplo, «usa la skill `backlog`»).

> Nota: si se prefiere conservar el flujo con `/backlog`, `/story` y `/pair`, se
> pueden crear comandos en `.opencode/commands/` cuyo prompt cargue la skill
> correspondiente. No es necesario para usar las skills.

## Actualizar

```bash
# Comprobar si hay cambios en la fuente
npx skills check

# Actualizar las skills del proyecto
npx skills update -p
```

## Desinstalar

```bash
npx skills remove backlog story pair -y
```

## Consideraciones

- **Revisar antes de confiar**: las skills son instrucciones que el agente
  ejecuta con sus permisos. Este repositorio solo contiene archivos `SKILL.md`
  (sin scripts), pero conviene revisar cualquier actualización.
- **Telemetría**: el CLI recopila telemetría anónima por defecto. Se desactiva
  con `DISABLE_TELEMETRY=1` o `DO_NOT_TRACK=1`.
- **Rutas de descubrimiento de OpenCode**: `.agents/skills` y `.claude/skills`
  (compatibilidad), además de `.opencode/skills` (nativa).
