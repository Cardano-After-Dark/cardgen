#!/bin/bash

# Color codes
GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m' # No Color

# Script name
SCRIPT_NAME=$(basename "$0")

# Commands to execute
commands=(
    "python3 -m venv venv"
    ". venv/bin/activate"
    "pip install -r requirements.txt"
)
delay=5

# Function to execute a command
execute_command() {
    echo "Executing: $1"
    if eval "$1"; then
        echo -e "${GREEN}Success executing:${NC} $1"
        return 0
    else
        echo -e "${RED}Error executing:${NC} $1"
        return 1
    fi
}

# Print header
echo -e "\nScript ${GREEN}$SCRIPT_NAME${NC} executing commands:"
printf '%s\n' "${commands[@]}" | sed 's/^/- /'
echo

# Execute commands
for cmd in "${commands[@]}"; do
    if execute_command "$cmd"; then
        sleep "$delay"
    else
        exit 1
    fi
done

echo -e "\n${GREEN}All commands executed successfully.${NC}"