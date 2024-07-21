#!/bin/bash

# Color codes
GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m' # No Color

# Script name
SCRIPT_NAME=$(basename "$0")

# Log file
LOG_FILE="logs/setup-cli.log"

# Ensure log directory exists
mkdir -p logs

# Commands to execute
commands=(
    "python3 -m venv venv"
    ". venv/bin/activate"
    "pip install -r requirements.txt"
)
delay=5

# Function to execute a command and log its output
execute_command() {
    local cmd="$1"
    local timestamp=$(date "+%Y.%m.%d %H:%M:%S")
    
    echo "Executing: $cmd"
    
    # Append timestamp and command to log file
    echo -e "\n# [$timestamp] $cmd" >> "$LOG_FILE"
    
    # Execute command and capture output
    if output=$(eval "$cmd" 2>&1); then
        echo -e "${GREEN}Success executing:${NC} $cmd"
        echo "$output" >> "$LOG_FILE"
        return 0
    else
        echo -e "${RED}Error executing:${NC} $cmd"
        echo "$output" >> "$LOG_FILE"
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
echo -e "Log file: $LOG_FILE"