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
(cd-pipeline-env) ubuntu@ip-172-31-38-159:~/cd-pipeline$ cat python_install.sh 
#!/bin/bash

project_name="$1"

# Create a virtual environment with the project name
python3 -m venv "$project_name"

# Activate the virtual environment
source "$project_name/bin/activate"

# Check if requirements.txt exists
if [[ -f "requirements.txt" ]]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Skipping installation of dependencies."
fi

# Run the main Python script
echo "Running main.py..."
python main.py

# Deactivate the virtual environment
deactivate
