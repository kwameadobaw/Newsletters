#!/bin/bash

echo "========================================"
echo "Byte-Sized Brilliance Newsletter Website"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Starting the newsletter website..."
echo
echo "Website will be available at: http://localhost:5000"
echo "Admin panel: http://localhost:5000/admin"
echo "Admin credentials: admin / admin123"
echo
echo "Press Ctrl+C to stop the server"
echo

python3 start.py 