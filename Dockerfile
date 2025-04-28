FROM python:3.13.2-slim

WORKDIR /

ADD config /config/

RUN mkdir -p /logs/

RUN pip install uv

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PROJECT_PATH=/app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-editable

CMD ["uv", "run", "-m", "src.main"]

