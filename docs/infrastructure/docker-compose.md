# Docker Compose del entorno local

Referencia del `compose.yaml` de la raíz. Ticket **INF-02**: solo PostgreSQL y RustFS. Keycloak, Kafka, CI/CD, backup y hardening tienen su propio ticket.

## Servicios

| Servicio | Imagen | Puertos host → contenedor | Uso |
|---|---|---|---|
| `postgres` | `postgres:16` | `5432:5432` | Base de datos principal (`agro_help_db`). |
| `rustfs` | `rustfs/rustfs:1.0.4` | `9000:9000` (API S3), `9001:9001` (consola) | Objetos S3: originales extraídos y documentos del RAG. |
| `volume-permission-helper` | `alpine:3.21` | — | Ajusta el dueño de `rustfs-data` a `10001:10001` y termina. |

RustFS corre como non-root (`10001:10001`). El helper es necesario porque los volúmenes de Docker nacen como `root`; sin él, RustFS no puede escribir en `/data`.

## Comandos

Desde la raíz del repositorio:

| Comando | Efecto |
|---|---|
| `docker compose config` | Valida la configuración. |
| `docker compose up -d` | Levanta los servicios. |
| `docker compose ps` | Muestra su estado. |
| `docker compose down` | Los detiene; los volúmenes persisten. |
| `docker compose down -v` | Además borra los volúmenes: **pierdes los datos**. |

## Estado

Red `agro-net`, volúmenes `pgdata`/`rustfs-data`, `env_file: .env`, `restart: unless-stopped` y variables `POSTGRES_*`/`RUSTFS_*`: definidos. Las credenciales de desarrollo están en `.env.example`; copia ese archivo a `.env` antes de arrancar.

## Tests

```bash
python3 -m unittest discover -s infrastructure/docker/tests -v
```

Validan la configuración resuelta sin levantar contenedores. `up -d` y `ps` son verificación manual al cerrar el ticket.
