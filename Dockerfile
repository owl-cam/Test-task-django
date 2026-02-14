FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=/.venv
WORKDIR /app
COPY ./src /app
RUN uv venv /.venv && uv sync
ENV PYTHONPATH="/app"
