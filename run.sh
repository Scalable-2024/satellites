#!/bin/bash

python3 -m venv satellite_env

source ./satellite_env/bin/activate

pip install -r requirements.txt

#you make the random satellites
python3 ./src/satellites/make_random_satellites.py


#you run the websocket server 
python3 ./src/satellites/rotating_satellite_websocket.py


#to visualize the satellites
python3 ./src/satellites/real_time_satellite_visualization.py

#to run the server to get the latest position
python3 ./src/server/flask_server.py --websocket-uri ws://localhost:8765 --http-port 5000
