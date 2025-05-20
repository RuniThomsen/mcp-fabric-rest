# Offline installation script for mcp-fabric-rest
# To be used in Codex Environment without internet access

# Create a virtual environment if it doesn't exist
if (-not (Test-Path -Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate the virtual environment
Write-Host "Activating virtual environment..."
. .\venv\Scripts\Activate.ps1

# Install packages from local directory
Write-Host "Installing packages from local directory..."
pip install --no-index --find-links=".\packages" pytest colorama iniconfig packaging pluggy

# Install the project in development mode
Write-Host "Installing the project in development mode..."
pip install -e .

Write-Host "Setup complete! You can now run the server using:"
Write-Host "python -m mcp_fabric.main --stdio"
