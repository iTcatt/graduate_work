FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update
RUN apt-get install -y --no-install-recommends graphviz unzip curl openjdk-17-jre-headless 
    
RUN curl -L -o structurizr-cli.zip \
      https://github.com/structurizr/cli/releases/download/v2025.03.28/structurizr-cli.zip && \
    unzip structurizr-cli.zip -d /opt/structurizr-cli && \
    rm structurizr-cli.zip && \
    ln -s /opt/structurizr-cli/structurizr.sh /usr/local/bin/structurizr-cli

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev


COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


ENV HF_HOME=/app/.cache/huggingface


RUN uv run start.py

ENV HF_HUB_OFFLINE=1
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uv", "run", "main.py"]
