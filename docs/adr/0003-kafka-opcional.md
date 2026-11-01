# ADR-0003: Kafka opcional en Fase 1

- **Estado:** Aceptado
- **Fecha:** 2026-10-31
- **Decisores:** Equipo AgroHelp

## Contexto

La arquitectura es event-driven y Kafka aparece como mecanismo de comunicación asíncrona. Sin embargo, la Fase 1 solo prepara la infraestructura y todavía no existe ningún flujo asíncrono real. Levantar Kafka desde el primer día añade un broker, almacenamiento, configuración de topics y observabilidad que nadie consume todavía.

`docs/phases.md` ya lo marca como “inicialmente opcional”.

## Decisión

Kafka no forma parte de la línea base de la Fase 1.

Se puede dejar definido como servicio opcional en Docker Compose (por ejemplo, con un perfil `kafka`) o añadirlo cuando aparezca el primer flujo asíncrono. Los topics propuestos para cuando se active son:

- `prices.raw`: precios extraídos por Data Acquisition.
- `prices.processed`: precios limpios y normalizados por Data Engineering.

La creación de topics y sus esquemas se definirán en `contracts/events/` antes de implementar los productores y consumidores.

## Consecuencias

**Positivas:**

- Entorno local más ligero y rápido de arrancar.
- Menos superficie de operación mientras no hay eventos.
- Los contratos de eventos se diseñan cuando se conoce el primer caso de uso real.

**Negativas:**

- Habrá que añadir Kafka y su configuración cuando llegue el primer flujo asíncrono.
- Si se usa una alternativa temporal (por ejemplo, `LISTEN/NOTIFY`), habrá que migrar después.

**Neutras:**

- La arquitectura sigue siendo event-driven; solo se pospone la infraestructura.

## Alternativas consideradas

- **Kafka ahora:** descartada por coste operativo sin uso real.
- **RabbitMQ:** descartada por añadir otra dependencia sin una ventaja clara para los casos previstos.
- **`LISTEN/NOTIFY` de PostgreSQL:** válida para el primer flujo simple, pero insuficiente para replay, desacoplamiento a escala o múltiples consumidores.

## Disparador de revisión

La aparición del primer flujo asíncrono real o la necesidad de replay y desacoplamiento entre servicios.

## Referencias

- `docs/phases.md`
- `docs/technicalArchitecture.md`
- [ADR-0001](0001-estructura-monorepo.md)
