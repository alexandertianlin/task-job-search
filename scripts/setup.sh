#!/bin/bash
# task-job-search setup script (Mac/Linux compatible)

echo "=== task-job-search Setup ==="

# Check Python
if command -v python3 &> /dev/null; then
    PY=python3
elif command -v python &> /dev/null; then
    PY=python
else
    echo "Error: Python not found"
    exit 1
fi
echo "Using: $($PY --version)"

# Install dependencies
$PY -m pip install -r requirements.txt 2>/dev/null && echo "Dependencies installed" || echo "pip install skipped (try: pip install -r requirements.txt)"

# Make scripts executable
chmod +x scripts/*.sh
echo "Setup complete!"
