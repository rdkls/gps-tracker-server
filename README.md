# GPS Tracker Server #
A basic system for managing GPS Tracker Devices.

Currently only looking at Coban TK102, since that's what I have.

There are 2 parts
- device_gateway, which GPS devices talk to
- rest api, for web & mobile access

Currently the device gateway handles initialization, heartbeat, and location request/response

The REST API is a quick throwup using EVE and its mongoengine extension

## System Requirements ##
* python
* virtualenv
* mongodb

## Setup ##
Nothing too strange here. Using virtualenv recommended = no system-wide packages
* `mkdir venv && virtualenv venv/gps`
* `. venv/gps/bin/activate`
* `pip install -r requirements.txt`

## Running the Device Gateway ##
Nothing fancy yet!
* `. venv/gps/bin/activate`
* `./device_gateway.py`

## Trying the Device Gateway ##
In another tab: `cat sample-reqs/tkip102-1.txt | nc localhost 9000`

## Running Tests ##
With virtualenv activated, just run 'nosetests'
