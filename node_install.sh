#!/bin/bash

# Check if package.json exists
if [[ ! -f "package.json" ]]; then
    echo "Error: package.json not found. Cannot install Node.js dependencies."
    exit 1
fi

# Install Node.js dependencies
echo "Installing dependencies from package.json..."
npm install

# Run the start command from package.json
echo "Running server.js..."
npm run start