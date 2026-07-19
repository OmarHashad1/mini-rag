FROM python:3.13.9 as base

WORKDIR /mini-rag

COPY ./pyproject.toml ./uv.lock /mini-rag/

RUN pip install uv && uv sync --frozen --no-install-project

COPY . /mini-rag/

RUN uv sync --frozen

WORKDIR /mini-rag/src


CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
