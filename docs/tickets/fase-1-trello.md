# Tickets Fase 1 — Trello

Tickets para configurar la infraestructura descrita en `docs/phases.md` (Fase 1) y alineada con `docs/technicalArchitecture.md`.

## Cómo usar este archivo

1. Crea un tablero con estas listas:
   - `Decisiones`
   - `Backlog Fase 1`
   - `En curso`
   - `Hecho`
2. Copia cada sección `##` como una tarjeta de Trello.
3. Usa la línea `Etiquetas:` para crear las etiquetas del tablero.
4. Pega el checklist en la descripción de la tarjeta o conviértelo en checklist de Trello.
5. Respeta las dependencias indicadas antes de mover una tarjeta a `En curso`.

## Etiquetas sugeridas

`infraestructura`, `docker`, `base de datos`, `almacenamiento`, `autenticación`, `seguridad`, `ci/cd`, `documentación`, `dx`, `decisión`, `opcional`, `api-first`.

## Orden sugerido

```text
ADR-01 → INF-01 → INF-02 → INF-03 → INF-04 → INF-05 → INF-06
                                      └→ INF-07 (si aplica)
INF-03..07 → INF-08 → INF-09
INF-03 → INF-10 → INF-11 → INF-12
INF-01 → INF-13
INF-01 → INF-14 (opcional)
```

---

# Lista: Decisiones

## ADR-01 — Estructura del monorepo y límites módulo/servicio

**Etiquetas:** arquitectura, decisión

**Descripción:**
Documentar la estructura `services/`, `modules/`, `frontend/`, `infrastructure/`, `contracts/` y `docs/`, y el criterio para separar un módulo en un servicio independiente.

**Checklist:**
- [ ] Crear `docs/adr/0001-estructura-monorepo.md`
- [ ] Incluir contexto, decisión y consecuencias
- [ ] Definir el criterio para crear un nuevo servicio
- [ ] Verificar que `technicalArchitecture.md` refleja la decisión

**Criterio de aceptación:**
El ADR explica dónde vive cada dominio y cuándo se despliega de forma independiente.

**Dependencias:** ninguna.

---

## ADR-02 — API Gateway: diferir

**Etiquetas:** arquitectura, decisión

**Descripción:**
Decidir si se implementa un API Gateway en Fase 1. Recomendación: diferirlo hasta tener al menos dos servicios que centralizar.

**Checklist:**
- [ ] Crear `docs/adr/0002-api-gateway.md`
- [ ] Describir contexto y alternativas
- [ ] Registrar la decisión y sus consecuencias
- [ ] Definir el criterio para reevaluar

**Criterio de aceptación:**
Decisión documentada y aceptada.

**Dependencias:** ninguna.

---

## ADR-03 — Kafka opcional en Fase 1

**Etiquetas:** arquitectura, decisión, opcional

**Descripción:**
Documentar por qué Kafka es opcional al inicio y en qué momento activarlo.

**Checklist:**
- [ ] Crear `docs/adr/0003-kafka-opcional.md`
- [ ] Incluir contexto, decisión y consecuencias
- [ ] Proponer los topics iniciales
- [ ] Definir el disparador para activarlo

**Criterio de aceptación:**
Decisión documentada y aceptada.

**Dependencias:** ninguna.

---

## ADR-04 — Keycloak y modelo de roles

**Etiquetas:** seguridad, decisión

**Descripción:**
Definir el realm, los clientes y los roles iniciales (`admin`, `analyst`) de Keycloak.

**Checklist:**
- [ ] Crear `docs/adr/0004-keycloak-roles.md`
- [ ] Definir clientes `web-app` y `api`
- [ ] Definir roles y permisos
- [ ] Definir un usuario de prueba solo para desarrollo

**Criterio de aceptación:**
Modelo de roles documentado y reflejado en el realm.

**Dependencias:** ninguna.

---

# Lista: Backlog Fase 1

## INF-01 — Estructura de carpetas y rename

**Etiquetas:** infraestructura, documentación

**Descripción:**
Alinear el repositorio con la estructura de `docs/phases.md` y corregir `infraestructure` → `infrastructure`.

**Checklist:**
- [ ] Renombrar `infraestructure/` a `infrastructure/`
- [ ] Crear `infrastructure/{docker,keycloak,databases,kafka,monitoring,ci-cd,security}/`
- [ ] Verificar `services/`, `modules/`, `frontend/`, `contracts/` y `docs/`
- [ ] Actualizar las referencias en la documentación

**Criterio de aceptación:**
`tree -L 2` coincide con la estructura documentada y no quedan referencias al typo.

**Dependencias:** ninguna.

---

## INF-02 — README de arranque, puertos y credenciales

**Etiquetas:** documentación, dx

**Descripción:**
Documentar cómo clonar, configurar `.env`, levantar el stack, puertos, credenciales de desarrollo y troubleshooting.

**Checklist:**
- [ ] Requisitos: Docker, Docker Compose, Python y Node
- [ ] `cp .env.example .env`
- [ ] `docker compose up -d`
- [ ] Tabla de servicios, puertos y variables
- [ ] Cómo ver logs y estado
- [ ] Troubleshooting básico

**Criterio de aceptación:**
Un desarrollador nuevo levanta el entorno siguiendo solo el README.

**Dependencias:** INF-01, INF-03.

---

## INF-03 — Docker Compose base

**Etiquetas:** docker, infraestructura

**Descripción:**
Crear el compose base con red, volúmenes, healthchecks, políticas de reinicio y variables de entorno.

**Checklist:**
- [ ] `compose.yaml` con `name: agrointelligence`
- [ ] Red `agro-net`
- [ ] Volúmenes `pgdata`, `minio-data` y `kafka-data`
- [ ] `env_file: .env`
- [ ] `restart: unless-stopped`
- [ ] `docker compose config` válido

**Criterio de aceptación:**
`docker compose up -d` arranca sin errores y `docker compose ps` muestra los servicios.

**Dependencias:** INF-01.

---

## INF-04 — PostgreSQL

**Etiquetas:** base de datos, infraestructura

**Descripción:**
Servicio PostgreSQL con base `agro_help_db`, credenciales por entorno, scripts de inicialización, volumen y healthcheck.

**Checklist:**
- [ ] Imagen fijada (`postgres:16` o `17`)
- [ ] `POSTGRES_DB`, `POSTGRES_USER` y `POSTGRES_PASSWORD` desde `.env`
- [ ] Scripts de init en `infrastructure/databases/postgres/init/`
- [ ] Volumen `pgdata`
- [ ] Healthcheck `pg_isready`
- [ ] Probar conexión con `psql`

**Criterio de aceptación:**
La base de datos es accesible y los datos persisten tras `down/up`.

**Dependencias:** INF-03.

---

## INF-05 — MinIO y buckets iniciales

**Etiquetas:** almacenamiento, infraestructura

**Descripción:**
Servicio MinIO con consola, credenciales por entorno, volumen, healthcheck y creación de buckets iniciales.

**Checklist:**
- [ ] Imagen fijada
- [ ] Puertos 9000 (API) y 9001 (consola)
- [ ] `MINIO_ROOT_USER` y `MINIO_ROOT_PASSWORD` desde `.env`
- [ ] Volumen `minio-data`
- [ ] Healthcheck `/minio/health/live`
- [ ] Script de init para los buckets `raw` y `documents`
- [ ] Probar con la consola o con `mc`

**Criterio de aceptación:**
Consola accesible, buckets creados y datos persistentes.

**Dependencias:** INF-03.

---

## INF-06 — Keycloak y realm base

**Etiquetas:** autenticación, seguridad

**Descripción:**
Keycloak con PostgreSQL como backend, realm `agrohelp`, clientes `web-app` y `api`, roles `admin` y `analyst`.

**Checklist:**
- [ ] Servicio `keycloak`
- [ ] Base de datos `keycloak` en PostgreSQL
- [ ] Realm exportado en `infrastructure/keycloak/realm-agrohelp.json`
- [ ] Clientes `web-app` y `api`
- [ ] Roles `admin` y `analyst`
- [ ] Usuario de prueba solo para desarrollo
- [ ] Healthcheck
- [ ] Documentar cómo obtener un token

**Criterio de aceptación:**
Consola de administración accesible, token obtenible y realm versionado.

**Dependencias:** INF-04.

---

## INF-07 — Kafka en modo KRaft (opcional)

**Etiquetas:** kafka, opcional

**Descripción:**
Kafka de un nodo sin Zookeeper. Solo si ADR-03 confirma incluirlo en Fase 1.

**Checklist:**
- [ ] Servicio `kafka`
- [ ] Configuración KRaft
- [ ] Volumen `kafka-data`
- [ ] Healthcheck
- [ ] Script de creación del topic `prices.raw`
- [ ] Producir y consumir un mensaje de prueba

**Criterio de aceptación:**
Broker healthy y mensaje de prueba publicado y consumido.

**Dependencias:** INF-03, ADR-03.

---

## INF-08 — Makefile y smoke test

**Etiquetas:** dx, infraestructura

**Descripción:**
Comandos `up`, `down`, `logs`, `ps`, `health` y `reset`, más una verificación de salud del stack.

**Checklist:**
- [ ] `make up`
- [ ] `make down`
- [ ] `make logs`
- [ ] `make health` (PostgreSQL, MinIO, Keycloak y Kafka si aplica)
- [ ] `make reset` con confirmación
- [ ] Documentar en el README

**Criterio de aceptación:**
Un comando levanta el stack y reporta la salud de los servicios.

**Dependencias:** INF-03 a INF-07.

---

## INF-09 — Backup y restore local

**Etiquetas:** operación, infraestructura

**Descripción:**
Scripts para respaldar y restaurar PostgreSQL y MinIO.

**Checklist:**
- [ ] `pg_dump` / `pg_restore`
- [ ] `mc mirror` para MinIO
- [ ] Procedimiento en el README
- [ ] Prueba de restore

**Criterio de aceptación:**
Backup y restore probados localmente.

**Dependencias:** INF-04, INF-05.

---

## INF-10 — Hardening base de contenedores

**Etiquetas:** seguridad, observabilidad

**Descripción:**
Imágenes fijadas, usuarios non-root, redes separadas, secretos por entorno y logs con rotación.

**Checklist:**
- [ ] Versiones de imagen fijadas (sin `latest`)
- [ ] Usuarios non-root en imágenes propias
- [ ] Redes separadas app/data
- [ ] Secretos solo por entorno
- [ ] `.dockerignore`
- [ ] Healthchecks y rotación de logs

**Criterio de aceptación:**
Checklist completo y `docker compose config` válido.

**Dependencias:** INF-03.

---

## INF-11 — CI con GitHub Actions

**Etiquetas:** ci/cd

**Descripción:**
Workflow para validar el compose, el lint y los tests.

**Checklist:**
- [ ] `.github/workflows/ci.yml`
- [ ] `docker compose config`
- [ ] Ruff y pytest cuando haya código
- [ ] Build de imágenes cuando haya Dockerfiles
- [ ] Cache de dependencias

**Criterio de aceptación:**
CI verde en un PR y sin secretos en los logs.

**Dependencias:** INF-03.

---

## INF-12 — Protección de `main` y secretos en GitHub

**Etiquetas:** git, ci/cd

**Descripción:**
Configurar la rama protegida, PR obligatorio y CI requerido.

**Checklist:**
- [ ] Branch protection en `main`
- [ ] Require PR y status checks
- [ ] Secrets de GitHub si hacen falta
- [ ] Documentar en el README o en `CONTRIBUTING.md`

**Criterio de aceptación:**
Push directo a `main` bloqueado y CI requerido.

**Dependencias:** INF-11.

---

## INF-13 — Contratos base (OpenAPI / AsyncAPI)

**Etiquetas:** api-first, documentación

**Descripción:**
Dejar preparado `contracts/` con un OpenAPI mínimo y el esquema de eventos inicial.

**Checklist:**
- [ ] `contracts/openapi.yaml`
- [ ] `contracts/events/` con el esquema de precio
- [ ] Documentar la convención de versionado

**Criterio de aceptación:**
Contratos válidos y referenciados desde el README.

**Dependencias:** INF-01.

---

## INF-14 — Dockerfile base para servicios Python

**Etiquetas:** docker, backend

**Descripción:**
Plantilla multi-stage para futuros servicios Python, con usuario non-root y healthcheck.

**Checklist:**
- [ ] `infrastructure/docker/python/Dockerfile`
- [ ] `.dockerignore`
- [ ] Usuario non-root
- [ ] Build de prueba

**Criterio de aceptación:**
La imagen de ejemplo construye y corre como non-root.

**Dependencias:** INF-01.

---

# No crear todavía

Estos elementos aparecen en la arquitectura, pero no son de Fase 1 y solo generarían ruido en el tablero:

- API Gateway (implementación).
- Kubernetes, Helm y Terraform.
- Prometheus, Grafana, Loki y OpenTelemetry.
- pgvector y el servicio RAG.
- MLflow y los servicios de Machine Learning.
- Microservicios de Data Acquisition, Data Engineering y Data Platform.
- Frontend Next.js.

# Definition of Done de la Fase 1

- [ ] `docker compose up -d` levanta PostgreSQL, MinIO y Keycloak (y Kafka si se aprobó).
- [ ] Todos los servicios reportan `healthy`.
- [ ] `docker compose config` es válido.
- [ ] CI verde en `main`.
- [ ] El README permite a un desarrollador nuevo levantar el entorno.
- [ ] No hay secretos versionados.
- [ ] Los ADRs de la fase están escritos y aceptados.
