FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project files
COPY pyproject.toml /app/
COPY mcp_fabric /app/mcp_fabric

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install

# Create non-root user
RUN useradd -m appuser
USER appuser

ENTRYPOINT ["mcp-fabric-rest", "--stdio"]
