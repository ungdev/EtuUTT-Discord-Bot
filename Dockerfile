FROM ghcr.io/astral-sh/uv:alpine

# Set uv environment to production
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_COMPILE_BYTECODE=1
# Set workdir
WORKDIR /usr/src/etuutt
# Install requirements
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.python-version,target=.python-version \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked --no-install-project
# Copy project files
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Set server port
ARG SERVER_PORT=3000
# Set server url
ENV SERVER_URL=http://0.0.0.0:${SERVER_PORT}
# Default port of the web server
EXPOSE ${SERVER_PORT}
# Default command
CMD ["uv", "run", "etuutt_bot"]
