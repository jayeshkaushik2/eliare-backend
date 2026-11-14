# syntax=docker/dockerfile:1

## -----------------------------------------------------
## Build stage (use tag with -dev suffix: e.g. 3.9.23-debian13-fips-dev)
FROM python:3.10.12 AS build-stage

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/env/bin:$PATH"

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN python -m venv env
COPY ./ ./
RUN pip install --no-cache-dir -r req.txt

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
