### Dominio 3. Data Platform
**Objetivo:** centralizar el almacenamiento, la organización y la disponibilidad de los datos.

Este dominio no debe confundirse con Data Engineering. Uno transforma la información y el otro administra cómo se almacena y se pone a disposición.

Microservicios:

03-data-platform/
│
├── data-catalog-service/
│
└── analytics-service/

1. Data Catalog Service

Administra los metadatos:
- Catálogo de productos.
- Catálogo de regiones.
- Catálogo de mercados.
- Catálogo de datasets.
- Diccionario de datos.
- Procedencia de la información.

2. Analytics Service

Permite consultar y analizar la información:
- Precios históricos.
- Variaciones porcentuales.
- Promedios.
- Tendencias.
- Volatilidad.
- Comparaciones entre productos.
- Estadísticas regionales.
El almacenamiento será PostgreSQL para información estructurada y RustFS/S3 para los datos históricos y archivos.