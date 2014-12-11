# GPS Tracker Server #
A basic python server for managing GPS Tracker Devices.

Currently only looking at Coban TK102, since that's what I have.

## Setup ##
Nothing too strange here. Using virtualenv recommended = no system-wide packages
2. `mkdir venv && virtualenv venv/gps`
3. `. venv/gps/bin/activate`
4. `pip install -r requirements.txt`

## Running the Device Gateway ##
Nothing fancy yet!
1. `. venv/gps/bin/activate`
2. `./device_gateway.py`

## Trying the Device Gateway ##
In another tab: `cat sample-reqs/tkip102-1.txt | nc localhost 9000`
