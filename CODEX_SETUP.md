# Codex Environment Setup Guide

This guide explains how to set up and run the `mcp-fabric-rest` project in an offline (no internet) Codex Environment on Windows.

## Prerequisites
- Python 3.11 must be installed and available in your PATH.
- All required Python package wheels are present in the `packages/` directory (already included in this repo).

## Steps

1. **Run the offline installation script:**
   Open PowerShell in the project root and execute:
   ```powershell
   powershell -ExecutionPolicy Bypass -File install_offline.ps1
   ```
   This will:
   - Create a virtual environment (`venv`) if it doesn't exist
   - Activate the virtual environment
   - Install all dependencies from the local `packages/` directory
   - Install the project in development mode

2. **Activate the virtual environment (if not already active):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Run the server:**
   ```powershell
   python -m mcp_fabric.main --stdio
   ```

## Notes
- If you add new dependencies, download their `.whl` files in an internet-enabled environment and place them in the `packages/` directory before moving to Codex.
- The `run_server.ps1` script can also be used to activate the environment and start the server in one step.

---

**You are now ready to use `mcp-fabric-rest` in a fully offline Codex Environment!**
