# Mini-RAG

> **Under construction.** This project is a work in progress — APIs, structure, and features may change without notice.

A minimal Retrieval-Augmented Generation (RAG) backend built with FastAPI. It ingests documents (PDF/TXT), splits them into chunks, and persists them per-project in MongoDB — the groundwork for a RAG pipeline (embedding/retrieval/generation are not wired up yet).

## Features

- **File upload** — upload PDF or TXT files, scoped to a project (`project_id`), with content-type and size validation.
- **Document processing** — extract text via LangChain loaders (`TextLoader` for `.txt`, `PyMuPDF4LLMLoader` for `.pdf`) and split it into overlapping chunks with `RecursiveCharacterTextSplitter`.
- **Persistence** — projects and chunks are stored in MongoDB via [Beanie](https://beanie-odm.dev/) (an async ODM built on Pydantic + PyMongo).
- **Project-scoped storage** — uploaded files are saved under `src/assets/files/<project_id>/`, with a unique, collision-safe filename generated per upload.

## Tech stack

- **API**: FastAPI + Uvicorn
- **Database**: MongoDB, via Beanie / PyMongo (async)
- **Document loading & chunking**: LangChain (`langchain-community`, `langchain-pymupdf4llm`, `langchain-text-splitters`)
- **Config**: `pydantic-settings` (`.env`-based)
- **Packaging**: [`uv`](https://docs.astral.sh/uv/)
- **Containerization**: Docker / Docker Compose (with `compose watch` for live-reload dev)

## Project structure

```text
src/
  configs/         # pydantic-settings app configuration
  controllers/     # business logic (file validation, path generation, document loading/chunking)
  enums/           # response messages/signals, processing & file-type enums
  models/          # Beanie Document models (Project, Chunk)
  repositories/    # data-access layer wrapping Beanie models (CRUD, pagination, bulk insert)
  routes/          # FastAPI routers (base/health, data upload & processing)
  schemas/         # Pydantic request/response schemas
  main.py          # app entrypoint, lifespan (Mongo connection + Beanie init)
docker/
  docker-compose.yaml       # MongoDB service
  docker-compose-dev.yaml   # app service (build, watch/live-reload, port, env)
Dockerfile
```

## Getting started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- [uv](https://docs.astral.sh/uv/) (only needed if running without Docker)

### 1. Configure environment variables

Copy the example file and fill in the values:

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `APP_NAME` | Application name |
| `APP_VERSION` | Application version |
| `OPENAPI_API_KEY` | Reserved for LLM API access (not yet used) |
| `ALLOWED_MIM_TYPES` | Allowed upload MIME types, e.g. `["text/plain","application/pdf"]` |
| `FILE_MAX_SIZE` | Max upload size, in MB |
| `FILE_DEFAULT_CHUCK_SIZE` | Read buffer size (bytes) used while streaming uploads to disk |
| `MONGO_URI` | MongoDB connection string (use the container-internal port `27017` when connecting from another container, or the host-mapped port `27018` from your machine) |
| `DB_NAME` | MongoDB database name |

### 2. Run with Docker Compose (recommended)

```bash
docker compose -f ./docker/docker-compose.yaml -f ./docker/docker-compose-dev.yaml up --build --watch
```

This starts MongoDB and the API, and live-syncs local source changes into the running container. The API is available at `http://localhost:8000`, and interactive docs at `http://localhost:8000/docs`.

> `--watch` requires running in the foreground (don't combine with `-d`) — Compose needs an active process to monitor file changes.

### 3. Run locally without Docker

```bash
uv sync
cd src
uv run uvicorn main:app --reload
```

Requires a MongoDB instance reachable at whatever `MONGO_URI` points to.

## API

All routes are prefixed with `/api/v1`.

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | App name/version |
| `GET` | `/health` | Health check |
| `POST` | `/data/upload/{project_id}` | Upload a file (multipart `file` field) to a project |
| `POST` | `/data/process/{project_id}` | Load, chunk, and persist an uploaded file's content |

`POST /data/process/{project_id}` body:

```json
{
  "file_id": "abc123_document.pdf",
  "chunk_size": 100,
  "chunk_overlap": 20,
  "do_reset": 0
}
```

`do_reset: 1` deletes existing chunks for the project before inserting the new ones.

Full interactive API docs (Swagger UI) are available at `/docs` once the server is running.
