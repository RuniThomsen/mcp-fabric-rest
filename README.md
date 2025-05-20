# mcp-fabric-rest

MCP Server for Microsoft Fabric Rest API's to be used primarily in Visual Studio Code and Codex.

## Overview

The server exposes a REST interface that acts as a bridge between the Microsoft Cloud Partner (MCP) services and Fabric. It is intended to be a lightweight backend that Visual Studio Code extensions and other tools can interact with during development.

## Requirements

- [Node.js](https://nodejs.org/) 18 or later
- npm (comes with Node.js)

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the server:
   ```bash
   npm start
   ```

The service will listen on `http://localhost:3000` by default.

## Authentication

Depending on the environment, the server can be configured to use one of the following authentication methods:

- **API Key** via the `Authorization` header.
- **OAuth Token** obtained from Azure Active Directory.

Configuration for these options is typically provided through environment variables or a configuration file.

## REST Endpoints

- `GET /health` – health check endpoint used by deployments or tools.
- `POST /authenticate` – obtain a token or validate provided credentials.
- `GET /projects` – list projects within MCP.
- `POST /projects` – create a new project in MCP.

These endpoints are a starting point and may be expanded as the server evolves.


## Running Tests

This project uses [Poetry](https://python-poetry.org/) to manage Python dependencies.
Install them and run the test suite using:

```bash
poetry install
poetry run pytest -m compliance
poetry run bandit -r mcp_fabric_rest
poetry run mypy --strict mcp_fabric_rest
# Optional if installed
trivy fs .
```
