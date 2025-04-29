FROM alpine:3.20 AS base

RUN apk update && apk add python3~=3.12 git
RUN apk add build-base libpq libpq-dev
RUN apk add --update py-pip 
RUN pip install uv --break-system-packages

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-editable

FROM base AS bot-image

WORKDIR /

ADD config /config/

RUN mkdir -p /logs/

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    PIP_NO_CACHE_DIR=off

CMD ["uv", "run", "-m", "src.main"]

FROM base AS alembic-image

ADD ./alembic.ini alembic.ini

CMD ["uv", "run", "alembic", "-c", "./alembic.ini" ,  "upgrade", "head"]

