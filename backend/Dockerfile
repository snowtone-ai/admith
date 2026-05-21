FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install uv
COPY backend/pyproject.toml ./
COPY backend/src ./src
RUN uv sync

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY backend/pyproject.toml backend/alembic.ini ./
COPY backend/alembic ./alembic
COPY backend/src ./src
COPY scripts ./scripts
ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH="/app/src"
CMD ["sh", "-c", "alembic upgrade head && uvicorn admith.api.main:app --host 0.0.0.0 --port 8000"]
