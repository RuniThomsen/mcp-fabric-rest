FROM python:3.11-slim

WORKDIR /app

# Copy local wheel packages
COPY packages /app/packages

# Copy project files
COPY pyproject.toml requirements.txt /app/
COPY mcp_fabric /app/mcp_fabric

# Install dependencies using local wheels and install project
RUN pip install --no-index --find-links=/app/packages -r requirements.txt \
    && pip install -e .

# Create non-root user
RUN useradd -m appuser
USER appuser

ENTRYPOINT ["mcp-fabric-rest", "--stdio"]
