# ADR-0001: Estructura del monorepo y límites entre módulos y servicios

- **Estado:** Aceptado
- **Fecha:** 2026-10-31
- **Decisores:** Equipo AgroHelp

## Contexto

El proyecto nace como un monorepo con siete dominios funcionales. La propuesta inicial de `docs/technicalArchitecture.md` organizaba el código en carpetas por dominio (`01-data-acquisition/`, `02-data-engineering/`, …, `07-infrastructure/`) y empujaba a que cada dominio tuviera sus propios microservicios. Esa estructura duplica responsabilidades, complica el arranque local y favorece la creación prematura de servicios.

`docs/phases.md` propone una estructura más simple (`services/`, `modules/`, `frontend/`, `infrastructure/`, `contracts/`, `docs/`) y recomienda explícitamente no convertir los siete dominios en siete aplicaciones ni en veinte microservicios.

## Decisión

Adoptar la estructura de `docs/phases.md`:

```text
AgroIntelligence/
├── services/          # unidades desplegables
├── modules/           # lógica compartida, no desplegable por sí sola
├── frontend/          # aplicación web
├── infrastructure/    # Docker, Keycloak, DBs, Kafka, monitoring, CI/CD, security
├── contracts/         # OpenAPI / AsyncAPI
├── docs/              # arquitectura, fases, ADRs
└── README.md
```

Reglas:

1. `services/` contiene unidades desplegables con su propio Dockerfile, pruebas y configuración.
2. `modules/` contiene lógica de dominio reutilizable, importada por uno o más servicios. No se despliega por sí sola.
3. `infrastructure/` no contiene lógica de negocio.
4. `contracts/` contiene los contratos OpenAPI y los esquemas de eventos.
5. `frontend/` contiene la aplicación Next.js.

Mapeo inicial de los dominios:

| Dominio | Ubicación inicial |
|---|---|
| Data Acquisition | `services/data-acquisition/` |
| Data Engineering | `modules/data-engineering/` |
| Data Platform | `modules/data-platform/` |
| Machine Learning | `modules/feature-engineering/`, `services/ml-training/`, `services/prediction/` |
| Generative AI | `services/rag/` |
| Application Services | Keycloak + módulos o servicios según necesidad |
| Infrastructure | `infrastructure/` |

Un módulo se separa en un servicio independiente solo si cumple al menos uno de estos criterios:

- Necesita escalar de forma independiente.
- Tiene un ciclo de despliegue distinto.
- Requiere aislamiento de fallos.
- Tiene un equipo propietario distinto.
- Usa un runtime o dependencias incompatibles.

También se renombra la carpeta `infraestructure/` a `infrastructure/`.

## Consecuencias

**Positivas:**

- Menos unidades desplegables al inicio y un entorno local más simple.
- Límites de dominio claros sin pagar el coste operativo de los microservicios.
- La separación posterior es un refactor controlado, no una reescritura.

**Negativas:**

- Separar un módulo más adelante exige mover código y definir contratos.
- Varios módulos comparten la base de datos del servicio que los contiene hasta que se separan.
- La estructura de carpetas no coincide todavía con el repositorio actual (`infraestructure/`); hay que renombrarla.

**Neutras:**

- Los siete dominios se mantienen como modelo conceptual, aunque no todos sean servicios.

## Alternativas consideradas

- **Carpetas por dominio (`01-data-acquisition/`…):** descartada porque duplica la organización y empuja a crear un servicio por dominio desde el inicio.
- **Monolito único:** descartada porque difumina los límites entre dominios y dificulta una separación futura.
- **Microservicios desde el día 1:** descartada por el coste operativo y porque todavía no hay flujos que justifiquen la separación.

## Referencias

- `docs/phases.md`
- `docs/technicalArchitecture.md`
- [ADR-0002](0002-api-gateway.md)
- [ADR-0003](0003-kafka-opcional.md)
