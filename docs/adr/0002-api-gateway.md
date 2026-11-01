# ADR-0002: Diferir el API Gateway

- **Estado:** Aceptado
- **Fecha:** 2026-10-31
- **Decisores:** Equipo AgroHelp

## Contexto

La Fase 1 prepara la infraestructura local, pero todavía no existen servicios de negocio desplegables. El frontend llega en la Fase 7. Incorporar un API Gateway ahora añadiría un componente que hay que configurar, observar y mantener sin que exista tráfico que enrutar.

La arquitectura reconoce que un gateway puede ser útil para centralizar autenticación, rate limiting, routing y CORS, pero también que introduce un punto único de fallo y una capa de configuración adicional.

## Decisión

No implementar un API Gateway en la Fase 1.

Cuando existan servicios, el frontend podrá consumirlos directamente o mediante un BFF ligero. La decisión se reevaluará cuando se cumpla al menos una de estas condiciones:

- Existan dos o más servicios que centralizar.
- Haga falta aplicar políticas transversales (autenticación, rate limiting, CORS, routing).
- El frontend necesite agregar respuestas de varios servicios.

Si se implementa más adelante, las opciones preferidas son Traefik o NGINX por su bajo coste operativo y su integración con Docker.

## Consecuencias

**Positivas:**

- Menos componentes en el entorno local.
- Menos configuración que mantener mientras no hay servicios.
- Los equipos pueden exponer APIs directamente y definir sus contratos con OpenAPI.

**Negativas:**

- Cuando llegue el gateway habrá que cambiar las URLs que consume el frontend.
- Las políticas transversales se aplicarán servicio a servicio hasta entonces.
- La autenticación se valida en cada servicio contra Keycloak.

**Neutras:**

- La decisión no impide añadir un gateway más adelante; solo lo pospone.

## Alternativas consideradas

- **Kong, NGINX o Traefik ahora:** descartada por ser prematura y añadir operación sin tráfico real.
- **Spring Cloud Gateway:** descartada porque introduce Java en un stack principalmente Python.
- **BFF en Next.js:** se puede considerar más adelante, cuando el frontend necesite agregar datos de varios servicios.

## Disparador de revisión

La aparición del segundo servicio desplegable o la primera necesidad transversal real (autenticación centralizada, rate limiting, routing o CORS).

## Referencias

- `docs/phases.md`
- `docs/technicalArchitecture.md`
- [ADR-0001](0001-estructura-monorepo.md)
