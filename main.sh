#!/bin/bash

# Set Python path to include all necessary directories
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src

# Run the scripts
python3 src/main.py

# Start the server
cd docs && python3 -m http.server 8888
