FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"

# Use non-root user for security
RUN adduser -D appuser
USER appuser

# Copy only pyproject and lock first for caching
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Install production dependencies only
RUN --mount=type=cache,target=/home/appuser/.cache/uv \
    uv sync --locked --no-install-project --no-dev

# Copy full application
COPY --chown=appuser:appuser . .

# Install the project (editable install or not)
RUN --mount=type=cache,target=/home/appuser/.cache/uv \
    uv sync --locked --no-dev

# Entrypoint is defined in docker-compose
ENTRYPOINT []
