#!/bin/bash
# One-liner installation script for SudoThink
# Usage: curl -fsSL https://raw.githubusercontent.com/vusallyv/sudothink/main/install-oneline.sh | bash

set -e

echo "🚀 Installing SudoThink..."

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Download the installation script
curl -fsSL https://raw.githubusercontent.com/vusallyv/sudothink/refs/heads/master/install.sh -o install.sh
chmod +x install.sh

# Run the installation
./install.sh

# Clean up
cd /
rm -rf "$TEMP_DIR"

echo "✅ SudoThink installation completed!" 