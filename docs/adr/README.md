# Registro de decisiones de arquitectura (ADR)

Este directorio contiene las decisiones arquitectónicas del proyecto. Cada ADR registra el contexto, la decisión, las consecuencias y las alternativas consideradas.

## Índice

| ADR | Título | Estado | Fecha |
|---|---|---|---|
| [0001](0001-estructura-monorepo.md) | Estructura del monorepo y límites entre módulos y servicios | Aceptado | 2026-10-31 |
| [0002](0002-api-gateway.md) | Diferir el API Gateway | Aceptado | 2026-10-31 |
| [0003](0003-kafka-opcional.md) | Kafka opcional en Fase 1 | Aceptado | 2026-10-31 |
| [0004](0004-keycloak-roles.md) | Keycloak y modelo de roles | Aceptado | 2026-10-31 |
| [0005](0005-rustfs-almacenamiento-objetos.md) | RustFS como almacenamiento de objetos en lugar de MinIO | Aceptado | 2026-10-31 |

## Convenciones

- Un ADR aceptado no se reescribe para cambiar la decisión.
- Si una decisión cambia, se crea un nuevo ADR y el anterior se marca como `Superado por ADR-XXXX`.
- Estados posibles: `Propuesto`, `Aceptado`, `Rechazado` y `Superado por ADR-XXXX`.
- La numeración es secuencial, con cuatro dígitos.
- Los ADRs son documentación versionada; no se gestionan como tarjetas de Trello.
