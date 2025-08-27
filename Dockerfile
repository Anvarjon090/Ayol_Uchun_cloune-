# FROM ghcr.io/astral-sh/uv:python3.12-alpine

# # Set working directory
# WORKDIR /app

# # Enable bytecode compilation
# ENV UV_COMPILE_BYTECODE=1
# ENV UV_LINK_MODE=copy
# ENV PATH="/app/.venv/bin:$PATH"

# # Use non-root user for security
# RUN adduser -D appuser
# USER appuser

# # Copy only pyproject and lock first for caching
# COPY --chown=appuser:appuser pyproject.toml uv.lock ./


# USER appuser

# # Install production dependencies only
# # RUN --mount=type=cache,target=/home/appuser/.cache/uv \
# RUN uv sync --locked --no-install-project --no-dev 
#     # uv sync --locked --no-install-project --no-dev

# # Copy full application
# COPY --chown=appuser:appuser . .

# # Install the project (editable install or not)
# RUN --mount=type=cache,target=/home/appuser/.cache/uv \
#     uv sync --locked --no-dev

# # Entrypoint is defined in docker-compose

# USER appuser

# ENTRYPOINT []




FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"

# avval appuser yaratamiz
RUN adduser -D appuser

# faqat dependency fayllarni copy qilamiz
COPY pyproject.toml uv.lock ./

# root sifatida dependency o‘rnatamiz
RUN uv sync --locked --no-install-project --no-dev

# endi app fayllarni copy qilamiz
COPY . .

# qo‘shimcha o‘rnatish (agar kerak bo‘lsa)
RUN uv sync --locked --no-dev

# endi foydalanuvchini almashtiramiz
USER appuser

ENTRYPOINT []