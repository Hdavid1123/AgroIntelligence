# Dominio 1. Data Acquisition
**Objetivo:** obtener información desde fuentes externas y llevarla a nuestra plataforma.

Este dominio no transforma profundamente los datos. Su responsabilidad es conectarse a las fuentes, extraer información y entregarla al siguiente dominio.

Microservicios:

01-data-acquisition/
│
├── data-source-service/
│
└── data-ingestion-service/

1. Data Source Service

Administra las fuentes de información:
- Registro de fuentes.
- Configuración de conexiones.
- Frecuencia de actualización.
- Credenciales.
- Estado de las fuentes.
2. Data Ingestion Service

Ejecuta las extracciones:
- Consulta APIs.
- Descarga archivos.
- Ejecuta scraping cuando corresponda.
- Almacena datos originales.
- Publica eventos de extracción completada.

Flujo:

FUENTES EXTERNAS
       |
       v
DATA SOURCE SERVICE
       |
       v
DATA INGESTION SERVICE
       |
       v
RAW DATA (RUSTFS)
       |
       v
KAFKA EVENT