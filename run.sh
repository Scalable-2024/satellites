# use tmux to run the satellites in the background

./run-satellite.sh A
./run-satellite.sh B
./run-satellite.sh C
./run-satellite.sh D
./run-satellite.sh E



# or
pkill -f "python main.py"
rm -f config/routes.json

python3 run_network.py

