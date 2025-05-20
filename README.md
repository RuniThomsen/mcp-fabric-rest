# mcp-fabric-rest

MCP Server for Microsoft Fabric REST APIs to be used primarily in Visual Studio Code and Codex.

## Overview

The server exposes a REST interface that acts as a bridge between the Microsoft Cloud Partner (MCP) services and Fabric. It is intended to be a lightweight backend that Visual Studio Code extensions and other tools can interact with during development.

## Requirements

- Python 3.11
- [Poetry](https://python-poetry.org/) for dependency management

## Setup

1. Install dependencies:
   ```bash
   poetry install
   ```
   If internet access isn't available, run `install_offline.ps1` instead.
   Detailed steps are provided in [CODEX_SETUP.md](CODEX_SETUP.md).
2. Start the server over STDIO:
   ```bash
   poetry run python -m mcp_fabric.main --stdio
   poetry run python -m mcp_fabric.main --stdio --rest --host 0.0.0.0
   ```

With REST enabled the service listens on `http://localhost:3000` by default.
Use `--host` and `--port` to change the bind address.

## Authentication

The server supports two authentication modes:

- **Managed Identity** – used when running inside Azure with an identity assigned to the host.
- **Service Principal** – specify `AZURE_CLIENT_ID`, `AZURE_TENANT_ID` and `AZURE_CLIENT_SECRET` environment variables.

Configuration for these options is typically provided through environment variables or a configuration file.

## REST Endpoints

- `GET /health` – health check endpoint used by deployments or tools.
- `GET /v1/workspaces` – list Fabric workspaces accessible to the caller.
- `POST /v1/workspaces` – create a new workspace.
- `GET /v1/artifacts` – list artifacts (datasets, reports, notebooks, etc.).
- `POST /v1/artifacts` – create an artifact within a workspace.

These endpoints are a starting point and may be expanded as the server evolves.

## Testing

Run the unit tests with `pytest`:

```bash
poetry run pytest
```

The project includes a CI workflow that executes the same command for every pull request to ensure the server remains stable.

