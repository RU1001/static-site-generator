#!/bin/bash

# Set Python path to include all necessary directories
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src

# Run the scripts
python3 static_to_public.py

# Start the server
cd public && python3 -m http.server 8888
