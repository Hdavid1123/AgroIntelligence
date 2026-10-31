# Dominio 2. Data Engineering
**Objetivo:** transformar los datos originales en información limpia, estandarizada y preparada para su utilización.

Microservicios:

02-data-engineering/
│
├── data-processing-service/
│
└── data-quality-service/

1. Data Processing Service

Se encarga de:
- Limpiar información.
- Estandarizar unidades.
- Homologar productos y regiones.
- Eliminar duplicados.
- Transformar datos.
- Construir datasets Silver y Gold.
2. Data Quality Service

Se encarga de:
- Validar integridad.
- Detectar valores anómalos.
- Detectar registros incompletos.
- Verificar reglas de negocio.
- Registrar errores de calidad.

Flujo:

RAW DATA
   |
   v
DATA PROCESSING
   |
   v
DATA QUALITY
   |
   +------> QUARANTINE
   |
   v
CLEAN DATA
   |
   v
SILVER / GOLD

Utilizaría Python, Polars, DuckDB, dbt y Great Expectations.

Apache Airflow será el orquestador de los pipelines.