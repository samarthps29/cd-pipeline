#!/bin/bash

project_name="$1" # project name should be the first positional argument
python ./ec2.py "$project_name"

# Check if the project folder exists
if [[ ! -d "$project_name" ]]; then
    echo "Error: Project folder '$project_name' does not exist."
    exit 1
fi

# Change to the project directory
cd "$project_name" || exit

# Check for the contents of the project folder and decide which installer to run
if [[ -f "main.py" ]]; then
    echo "Python project detected. Running python_install.sh..."
    ../python_install.sh "$project_name"
elif [[ -f "package.json" ]]; then
    echo "Node.js project detected. Running node_install.sh..."
    ../node_install.sh
else
    echo "Error: The project does not contain recognized files."
    exit 1
fi
