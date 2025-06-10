FROM python:3.12-slim AS base

# Instala LaTeX + herramientas necesarias

RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-extra \
    latexmk \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias
ENV UV_HTTP_TIMEOUT=120
RUN rm -f .venv/bin/replay || true
RUN uv sync --frozen --no-dev

# Copiar el resto del código
COPY ./src ./src
COPY ./knowledge ./knowledge

EXPOSE 8000

ENV PYTHONPATH=/app/src
CMD ["uv","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]