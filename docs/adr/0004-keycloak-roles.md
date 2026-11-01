# ADR-0004: Keycloak y modelo de roles

- **Estado:** Aceptado
- **Fecha:** 2026-10-31
- **Decisores:** Equipo AgroHelp

## Contexto

`docs/phases.md` recomienda implementar la autenticación temprano, aunque la gestión de usuarios y las funcionalidades de aplicación lleguen después. La arquitectura propone Keycloak como proveedor de identidad y el proyecto necesita distinguir entre quien administra la plataforma y quien solo consulta información.

## Decisión

Usar Keycloak como proveedor de identidad con esta configuración inicial:

- **Realm:** `agrohelp`.
- **Clientes:**
  - `web-app`: cliente público con PKCE para el frontend.
  - `api`: cliente bearer-only o confidencial para la validación de tokens entre servicios.
- **Roles de realm:**
  - `admin`: gestiona fuentes, catálogo, usuarios y configuración.
  - `analyst`: consulta precios, predicciones, analíticas e informes.
- **Usuario de prueba:** solo en el realm de desarrollo, nunca con credenciales reales.
- **Validación:** los servicios validan el JWT contra el JWKS de Keycloak y comprueban audiencia y roles.
- **Versionado:** el realm se exporta a `infrastructure/keycloak/realm-agrohelp.json` y se importa al arrancar.

Los secretos de clientes y usuarios no se versionan; se pasan por variables de entorno.

## Consecuencias

**Positivas:**

- Autenticación y autorización estándar basadas en OIDC.
- Los roles se gestionan de forma centralizada.
- El realm versionado permite reproducir el entorno local.

**Negativas:**

- Keycloak añade un contenedor y una base de datos adicional.
- El modelo de roles puede quedarse corto cuando aparezcan permisos más finos.
- Hay que mantener el realm exportado sincronizado con los cambios.

**Neutras:**

- El modelo de dos roles es suficiente para la Fase 1 y puede evolucionar.

## Alternativas consideradas

- **Autenticación propia:** descartada por el riesgo de seguridad y el coste de mantenimiento.
- **Auth0 u otro IdP SaaS:** descartado por dependencia externa y coste; se puede reevaluar si se necesita SSO.
- **Sin autenticación en la Fase 1:** descartada porque contradice “Security by Design” y la recomendación de implementar auth temprano.

## Disparador de revisión

La llegada de multi-tenant, SSO con un IdP externo o permisos de grano fino.

## Referencias

- `docs/phases.md`
- `docs/technicalArchitecture.md`
- [ADR-0001](0001-estructura-monorepo.md)
- [ADR-0002](0002-api-gateway.md)
