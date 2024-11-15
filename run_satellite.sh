#!/bin/bash

# Check if satellite ID is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <satellite_id>"
    echo "Example: $0 A"
    exit 1
fi

SATELLITE_ID=$1

# Define the network map
NETWORK_MAP="A:5001,B:5002,C:5003,D:5004,E:5005"

# Get the port for this satellite
PORT=$(echo $NETWORK_MAP | tr ',' '\n' | grep "^$SATELLITE_ID:" | cut -d':' -f2)

if [ -z "$PORT" ]; then
    echo "Error: Invalid satellite ID"
    exit 1
fi

# Create required directories
mkdir -p logs config

# Start the satellite using Hypercorn
python main.py --id $SATELLITE_ID --port $PORT --network $NETWORK_MAP
