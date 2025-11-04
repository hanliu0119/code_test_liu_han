#!/usr/bin/env bash
# ============================================================
# Project setup script for code_test_liu_han
# Purpose: create a virtual environment and install dependencies
# ============================================================

set -e  # Exit immediately if any command fails
PROJECT_NAME="code_test_liu_han"

echo "Setting up project: ${PROJECT_NAME}"
echo "Current directory: $(pwd)"

# 1. Create a new virtual environment (if not existing)
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment (.venv)..."
  python3 -m venv .venv
else
  echo "Virtual environment already exists."
fi

# 2. Activate virtual environment (macOS/Linux only)
if [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu"* ]]; then
  source .venv/bin/activate
else
  echo "On Windows, please activate manually: .venv\\Scripts\\activate"
fi

# 3. Upgrade pip & setuptools
echo "Upgrading pip & setuptools..."
pip install --upgrade pip setuptools wheel

# 4. Install dependencies (including dev)
echo "Installing dependencies..."
pip install -e ".[dev]"

# 5. Verify installation by listing key packages
echo "Verifying installation..."
pip list | grep -E "fastapi|uvicorn|pydantic" || true

echo "Environment setup completed successfully."
