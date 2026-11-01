# Documento de arquitectura técnica
## Proyecto: Plataforma de inteligencia, análisis y predicción de precios agrícolas (AgroHelp)

Versión: 1.1
Fecha: Octubre de 2026
Estilo arquitectónico: Microservicios orientados a eventos (Event-Driven Architecture), con evolución progresiva desde módulos
Lenguaje principal: Python
Enfoque: Escalabilidad, modularidad, trazabilidad y extensibilidad.
___

## 1. Descripción general del sistema

### 1.1 Propósito
Desarrollar una plataforma tecnológica que permita recopilar, almacenar, procesar y analizar información relacionada con los mercados agrícolas, con el propósito de generar predicciones sobre el comportamiento futuro de los precios de productos agrícolas.

La plataforma permitirá:
1. Obtener información de diferentes fuentes de datos.
2. Procesar y estandarizar información mediante pipelines ETL/ELT.
3. Almacenar grandes cantidades de información histórica.
4. Analizar el comportamiento de los precios agrícolas.
5. Entrenar modelos de Machine Learning.
6. Generar predicciones sobre posibles incrementos o disminuciones de precios.
7. Consultar información mediante un sistema RAG.
8. Generar explicaciones sobre los factores que pueden influir en los precios.
9. Visualizar estadísticas, tendencias y predicciones.
10. Administrar fuentes, modelos, documentos y procesos de datos.

### 1.2 Principios arquitectónicos
La arquitectura se construirá siguiendo estos principios:

| Principio | Descripción |
|---|---|
| Microservicios | Los dominios con justificación técnica se despliegan como servicios independientes; el resto se mantiene como módulos con límites claros. |
| Database per Service | Cada servicio es propietario de sus datos. Los módulos comparten la base del servicio que los contiene hasta que se separen. |
| Event-Driven Architecture | Los servicios se comunicarán mediante eventos cuando corresponda. |
| API First | Los contratos de comunicación se definirán antes de implementar los servicios. |
| Stateless Services | Los servicios de consulta no dependerán de estado local persistente. |
| Observability | Todos los servicios tendrán logs, métricas y trazas. |
| Data Lineage | Se podrá rastrear el origen y transformación de los datos. |
| MLOps | Los modelos tendrán versiones, métricas y procesos de evaluación. |
| Reproducibility | Los experimentos y predicciones podrán reproducirse. |
| Security by Design | La seguridad estará contemplada desde el diseño. |

### 1.3 Distribución general del proyecto
El proyecto se organiza como un monorepo alineado con `docs/phases.md`. La estructura separa unidades desplegables (`services/`), lógica compartida (`modules/`), la aplicación web (`frontend/`), la infraestructura (`infrastructure/`), los contratos (`contracts/`) y la documentación (`docs/`).

```text
AgroIntelligence/
├── services/          # unidades desplegables
│   ├── data-acquisition/
│   ├── ml-training/
│   ├── prediction/
│   └── rag/
├── modules/           # lógica compartida, no desplegable por sí sola
│   ├── data-engineering/
│   ├── data-platform/
│   └── feature-engineering/
├── frontend/
│   └── web-app/
├── infrastructure/    # Docker, Keycloak, DBs, Kafka, monitoring, CI/CD, security
│   ├── docker/
│   ├── keycloak/
│   ├── databases/
│   ├── kafka/
│   ├── monitoring/
│   ├── ci-cd/
│   └── security/
├── contracts/         # OpenAPI / AsyncAPI
├── docs/              # arquitectura, fases, ADRs
│   └── adr/
└── README.md
```

| Carpeta | Contenido | ¿Se despliega? |
|---|---|---|
| `services/` | Servicios ejecutables con su propio Dockerfile, pruebas y configuración. | Sí |
| `modules/` | Lógica de dominio reutilizable, importada por uno o más servicios. | No por sí sola |
| `frontend/` | Aplicación web Next.js. | Sí |
| `infrastructure/` | Docker, Keycloak, bases de datos, Kafka, monitoreo, CI/CD y seguridad. No contiene lógica de negocio. | No |
| `contracts/` | Contratos OpenAPI y esquemas de eventos (AsyncAPI). | No |
| `docs/` | Arquitectura, fases, ADRs y documentación operativa. | No |

> Nota: el repositorio conserva temporalmente la carpeta `infraestructure/`; el ticket INF-01 la renombra a `infrastructure/` para alinearla con `docs/phases.md`.

### 1.4 Estrategia de evolución
Se comienza con el menor número de unidades desplegables que permita entregar valor. Un dominio se convierte en servicio independiente cuando exista una justificación técnica (escala, ciclo de despliegue, aislamiento de fallos o equipo propietario). Hasta entonces, vive como módulo dentro del servicio que lo utiliza. Esto evita convertir los siete dominios en siete aplicaciones o en veinte microservicios desde el primer día.

## 2. Los siete dominios

### Dominio 1. Data Acquisition
**Objetivo:** obtener información desde fuentes externas y llevarla a nuestra plataforma.

Este dominio no transforma profundamente los datos. Su responsabilidad es conectarse a las fuentes, extraer información y entregarla al siguiente dominio.

**Ubicación:** `services/data-acquisition/`

```text
services/data-acquisition/
├── source-management/
├── connectors/
├── extraction/
└── scheduling/
```

**Despliegue:** servicio independiente. Es el primer servicio del sistema (Fase 2). Se comienza con una sola fuente de precios agrícolas.

### Dominio 2. Data Engineering
**Objetivo:** transformar los datos originales en información limpia, estandarizada y preparada para su utilización.

**Ubicación:** `modules/data-engineering/`

```text
modules/data-engineering/
├── ingestion/
├── cleaning/
├── normalization/
├── validation/
├── transformation/
└── pipelines/
```

**Despliegue:** módulo. Se ejecuta dentro del servicio que lo importe y puede separarse si el volumen de procesamiento lo justifica.

**Arquitectura Medallion:**
- **Bronze:** datos originales.
- **Silver:** datos limpios y normalizados.
- **Gold:** datos preparados para análisis y modelos.

Tecnologías previstas: Python, Polars, DuckDB y dbt.

### Dominio 3. Data Platform
**Objetivo:** centralizar el almacenamiento, la organización y la disponibilidad de los datos.

Este dominio no debe confundirse con Data Engineering. Uno transforma la información y el otro administra cómo se almacena y se pone a disposición.

**Ubicación:** `modules/data-platform/`

```text
modules/data-platform/
├── catalog/
├── product-management/
├── region-management/
├── market-management/
└── analytics/
```

**Despliegue:** módulo. Expone sus capacidades a través del servicio que lo contenga.

### Dominio 4. Machine Learning
**Objetivo:** desarrollar, entrenar, evaluar y ejecutar los modelos que predicen el comportamiento de los precios agrícolas.

**Ubicación:**
- `modules/feature-engineering/` para la ingeniería de variables.
- `services/ml-training/` para el entrenamiento.
- `services/prediction/` para la predicción.

```text
modules/feature-engineering/
services/
├── ml-training/
└── prediction/
```

**Despliegue:** `ml-training` y `prediction` como servicios independientes; `feature-engineering` como módulo compartido.

**MLOps:** registro y versionado de modelos con MLflow. Validación temporal obligatoria para evitar contaminación con información futura.

### Dominio 5. Generative AI
**Objetivo:** implementar el sistema RAG para consultar información documental y estructurada mediante lenguaje natural.

**Ubicación:** `services/rag/`

```text
services/rag/
├── document-processing/
├── embeddings/
├── retrieval/
└── generation/
```

**Despliegue:** servicio independiente. Usa `pgvector` como base vectorial.

**Regla:** el RAG no inventa predicciones ni realiza cálculos estadísticos por su cuenta. Consume los resultados de los servicios especializados y cita sus fuentes.

### Dominio 6. Application Services
**Objetivo:** proporcionar los servicios que necesita la aplicación para interactuar con los usuarios.

**Ubicación:**
- Identidad: Keycloak.
- Perfiles, preferencias y notificaciones: módulos o servicios según necesidad.
- API Gateway: diferido hasta que existan al menos dos servicios.

1. **Identity Service**

   Autenticación, autorización y gestión de roles con Keycloak. Realm `agrohelp`, clientes `web-app` y `api`, roles `admin` y `analyst`.

2. **User Service**

   Gestiona perfiles, preferencias, productos favoritos e historial de consultas. Inicialmente puede vivir como módulo.

3. **Notification Service**

   Gestiona alertas sobre precios, predicciones y actualizaciones. Inicialmente puede vivir como módulo.

4. **API Gateway**

   Centraliza las solicitudes del frontend y las distribuye a los microservicios correspondientes. **No se implementa en Fase 1**; ver ADR-02.

**Frontend:**

```text
frontend/web-app/
├── app/                 # rutas Next.js (App Router)
├── components/          # componentes reutilizables
├── features/            # dashboard, products, markets, analytics, predictions, assistant, users
├── services/            # clientes de API
├── hooks/
└── types/
```

Tecnologías: Next.js, React y TypeScript.

### Dominio 7. Infrastructure
**Objetivo:** proporcionar toda la infraestructura necesaria para ejecutar, comunicar, desplegar y monitorear los microservicios.

Aquí no desarrollaremos lógica de negocio.

**Ubicación:** `infrastructure/`

```text
infrastructure/
├── docker/
├── kubernetes/     # futuro
├── helm/           # futuro
├── terraform/      # futuro
├── kafka/
├── databases/
├── monitoring/
├── ci-cd/
└── security/
```

**Despliegue:** no contiene lógica de negocio. En Fase 1 solo se implementa lo necesario para el entorno local con Docker Compose; Kubernetes, Helm y Terraform se incorporan más adelante.

## 3. Infraestructura y despliegue

### 3.1 Fase 1: infraestructura local
La Fase 1 prepara el entorno para desarrollar y desplegar los componentes. El criterio de salida es que `docker compose up -d` levante el entorno y todos los servicios reporten salud.

| Componente | Implementación en Fase 1 |
|---|---|
| Contenedores | Docker + Docker Compose |
| Base de datos | PostgreSQL |
| Almacenamiento de objetos | MinIO |
| Autenticación | Keycloak |
| Comunicación asíncrona | Kafka en modo KRaft (opcional) |
| CI/CD | GitHub Actions |
| API Gateway | Diferido (ADR-02) |
| Orquestación productiva | Kubernetes / Helm / Terraform: futuro |

### 3.2 Componentes y fase de introducción
| Componente | Tecnología | Fase |
|---|---|---|
| Contenedores | Docker | 1 |
| Orquestación local | Docker Compose | 1 |
| Base de datos | PostgreSQL | 1 |
| Almacenamiento | MinIO | 1 |
| Autenticación | Keycloak | 1 |
| Comunicación asíncrona | Kafka | 1 (opcional) |
| CI/CD | GitHub Actions | 1 |
| API Gateway | — | Diferido |
| Orquestación productiva | Kubernetes + Helm + Terraform | Futura |
| Vector DB | pgvector | 6 |
| Monitoreo | Prometheus + Grafana | Futura |
| Logs | Loki | Futura |
| Trazas | OpenTelemetry | Futura |

### 3.3 Decisiones diferidas
- **API Gateway:** no se implementa hasta que existan al menos dos servicios que centralizar.
- **Kafka:** opcional en Fase 1; se activa cuando haya comunicación asíncrona real.
- **Kubernetes, Helm y Terraform:** se incorporan cuando el despliegue local ya no sea suficiente.
- **Observabilidad completa:** Prometheus, Grafana, Loki y OpenTelemetry se añaden después de estabilizar el entorno local.

### 3.4 ADRs
Las decisiones arquitectónicas se documentan en `docs/adr/`:

- `0001-estructura-monorepo.md`
- `0002-api-gateway.md`
- `0003-kafka-opcional.md`
- `0004-keycloak-roles.md`

## 4. Comunicación de los dominios

- **Síncrona:** APIs REST documentadas con OpenAPI. Los contratos viven en `contracts/`.
- **Asíncrona:** eventos con Kafka y esquemas versionados. Los contratos de eventos viven en `contracts/events/`.
- **API First:** ningún servicio se implementa sin su contrato acordado.
- **Database per Service:** cada servicio es dueño de sus datos; los módulos acceden a los datos a través del servicio propietario.
