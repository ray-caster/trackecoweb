#!/bin/bash

# Setup script for daily statistics update
# This sets up a cron job to run daily at 8 PM WIB (13:00 UTC)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/daily_update.py"

# Make sure Python script is executable
chmod +x "$PYTHON_SCRIPT"

# Get Python path
PYTHON_PATH=$(which python3 || which python)

# Create cron job entry (8 PM WIB = 1 PM UTC)
CRON_JOB="0 13 * * * cd $SCRIPT_DIR && $PYTHON_PATH $PYTHON_SCRIPT >> $SCRIPT_DIR/daily_update.log 2>&1"

# Check if cron job already exists
(crontab -l 2>/dev/null | grep -v "$PYTHON_SCRIPT") | crontab -

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✓ Daily update cron job has been set up successfully!"
echo "  Schedule: Every day at 8 PM WIB (1 PM UTC)"
echo "  Script: $PYTHON_SCRIPT"
echo "  Log file: $SCRIPT_DIR/daily_update.log"
echo ""
echo "To verify the cron job, run: crontab -l"
echo "To remove the cron job, run: crontab -e"

