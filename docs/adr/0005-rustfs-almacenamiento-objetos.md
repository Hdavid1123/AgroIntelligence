# ADR-0005: RustFS como almacenamiento de objetos en lugar de MinIO

- **Estado:** Aceptado
- **Fecha:** 2026-10-31
- **Decisores:** Equipo AgroHelp

## Contexto

La Fase 1 necesita almacenamiento de objetos compatible con S3 para guardar los originales extraídos y, más adelante, los documentos que consumirá el RAG. La arquitectura proponía MinIO.

MinIO distribuye su edición comunitaria bajo AGPLv3 y ha reducido funcionalidad de su edición gratuita, lo que introduce incertidumbre sobre licencia y características de cara a un uso comercial. El proyecto necesita una alternativa con licencia permisiva y API S3 estable, porque los contratos de los servicios no deben depender del proveedor de almacenamiento.

RustFS es un almacenamiento de objetos compatible con S3, escrito en Rust y distribuido bajo Apache 2.0. Ofrece consola web, ejecución como usuario non-root y despliegue local con Docker Compose.

## Decisión

Usar **RustFS** como almacenamiento de objetos del proyecto, empezando por el entorno local de la Fase 1:

- Imagen fijada `rustfs/rustfs:1.0.4`.
- Puertos `9000` (API S3) y `9001` (consola), igual que antes.
- Credenciales por entorno: `RUSTFS_ACCESS_KEY` y `RUSTFS_SECRET_KEY`.
- Un único volumen persistente montado en `/data` (`RUSTFS_VOLUMES=/data`), suficiente para desarrollo local.
- Servicio auxiliar `volume-permission-helper` que ajusta el dueño del volumen a `10001:10001`, porque RustFS corre como non-root y los volúmenes de Docker nacen como `root`.
- Los buckets iniciales serán `raw` y `documents` (INF-05).
- Los backups de objetos de INF-08 usarán `rclone`, no herramientas específicas del proveedor.

La API S3 sigue siendo el contrato: ningún servicio dependerá de características exclusivas de RustFS.

## Consecuencias

**Positivas:**

- Licencia Apache 2.0, sin las obligaciones de copyleft de AGPL.
- Clientes S3 (`boto3`, `s3fs`, `rclone`) siguen funcionando sin cambios; solo cambian los nombres de las variables de credenciales.
- El contenedor corre como non-root desde el primer día.
- Endpoints y puertos no cambian respecto a MinIO.

**Negativas:**

- RustFS es más joven que MinIO: habrá que validar la cobertura de las operaciones S3 que usemos (multipart, URLs prefirmadas, versionado).
- El helper de permisos añade un servicio al compose.
- El formato en disco no es intercambiable con MinIO por defecto; una migración real se hace copiando objetos por S3, no moviendo el volumen.

**Neutras:**

- El almacenamiento sigue siendo local en Fase 1; Kubernetes y almacenamiento distribuido llegan más adelante.
- La consola cambia de interfaz, pero cumple la misma función.

## Alternativas consideradas

- **Mantener MinIO:** descartada por la licencia AGPL y la incertidumbre sobre la edición gratuita.
- **Ceph u otro almacenamiento distribuido:** descartada por complejidad operativa para un entorno local.
- **Sistema de archivos local:** descartada porque rompe la API S3 y obligaría a cambiar a los clientes más adelante.
- **S3 en la nube:** descartada en Fase 1 por coste y dependencia externa; la API S3 deja la puerta abierta.

## Referencias

- `docs/phases.md`
- `docs/technicalArchitecture.md`
- `docs/infrastructure/docker-compose.md`
- `docs/tickets/fase-1-trello.md` (INF-02, INF-05, INF-08)
- [RustFS en Docker Hub](https://hub.docker.com/r/rustfs/rustfs)
