FROM python:3.13.1-slim
LABEL authors="KuyuGama"

ENV PIP_ROOT_USER_ACTION=ignore \
    VIRTUAL_ENV="/app/.venv/" \
    PATH="/app/.venv/bin:$PATH" \
    PORT=8000

RUN pip install uv -qqq

WORKDIR /app

COPY ./pyproject.toml /app/

RUN uv sync --no-cache

COPY . /app/

CMD fastapi run --port=$PORT
