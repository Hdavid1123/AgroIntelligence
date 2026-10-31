### Dominio 5. Generative AI
Objetivo: implementar el sistema RAG para consultar información documental y estructurada mediante lenguaje natural.

Microservicios:

05-generative-ai/
├── document-processing-service/
├── vector-search-service/
└── rag-service/

1. Document Processing Service
- Obtiene documentos.
- Extrae texto.
- Limpia contenido.
- Divide documentos en fragmentos.
- Genera embeddings.
- Indexa documentos.

2. Vector Search Service
- Almacena embeddings.
- Ejecuta búsquedas semánticas.
- Filtra por metadatos.
- Recupera fragmentos relevantes.

3. RAG Service

Coordina las consultas:
- Interpreta preguntas.
- Consulta documentos.
- Consulta datos estructurados mediante Analytics Service.
- Consulta predicciones mediante Prediction Service.
- Construye contexto.
- Envía información al LLM.
- Genera respuestas con fuentes.

Flujo:

DOCUMENTS
    |
    v
DOCUMENT PROCESSING
    |
    v
VECTOR SEARCH
    |
    v
RAG SERVICE
    |
    +------> ANALYTICS SERVICE
    |
    +------> PREDICTION SERVICE
    |
    v
LLM
    |
    v
ANSWER

Utilizaría LlamaIndex, pgvector y un proveedor de modelos LLM.