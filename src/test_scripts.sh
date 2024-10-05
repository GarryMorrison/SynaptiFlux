#!/bin/bash

# This script was created with assistance from ChatGPT, an AI language model by OpenAI.
# It runs Python scripts and logs the output, categorizing them by success or error.

# Testing script prefix
SCRIPT_PREFIX="testing_"

# Directory containing your Python scripts
SCRIPT_DIR="."

# Create a timestamped log directory
LOG_DIR="logs/$(date +'%Y-%m-%d_%H-%M-%S')"
mkdir -p "$LOG_DIR"

# Keep track of the number of success vs error cases
success_count=0
error_count=0

# Loop through all Python scripts in the directory
for script in "$SCRIPT_DIR/$SCRIPT_PREFIX"*.py; do
    echo "Running $script..."

    # Execute the script and redirect output to a temporary log file
    TEMP_LOG="$LOG_DIR/temp_$(basename "$script" .py).log"
    python3 "$script" > "$TEMP_LOG" 2>&1

    # Check the exit status of the Python script
    if [ $? -ne 0 ]; then
        # Rename the log file to indicate an error
        mv "$TEMP_LOG" "$LOG_DIR/error_$(basename "$script" .py).log"
        echo "Exception occurred in $script."
        echo "See log: $LOG_DIR/error_$(basename "$script" .py).log"
        error_count=$((error_count + 1))
    else
        # Rename the log file to indicate success
        mv "$TEMP_LOG" "$LOG_DIR/success_$(basename "$script" .py).log"
        echo "$script executed successfully."
        echo "See log: $LOG_DIR/success_$(basename "$script" .py).log"
        success_count=$((success_count + 1))
    fi

    echo # Create a blank line for readability
done

# Display brief stats:
echo
echo "Success: $success_count"
echo "Error: $error_count"
echo "Total: $((success_count + error_count))"

