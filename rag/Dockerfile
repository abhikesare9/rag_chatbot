From ubuntu:22.04
WORKDIR /app
copy . /app
RUN apt update -y && apt upgrade -y
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python3", "main.py"]