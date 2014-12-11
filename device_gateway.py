#!/usr/bin/env python
from gevent.server import StreamServer
import config
import sys
from models import GPSDevice

def handle(sock, (clientip, clientport)):
    print 'handle'
    fp = sock.makefile()

    # Create the device to use for this connection
    # Using him, we'll send, receive, persist all stuff
    device = GPSDevice(ipaddr=clientip)

    while True:
        data = fp.readline()
        if not data:
            break
        print 'read %s' % data
        device.sent(data)
        for response in device.responses:
            fp.write(response)
            fp.flush()
        fp.write(device.imei)
        fp.flush()

    fp.write('ooook then!')
    # receive data from a device
    # at this point we'll just have IP, and data
    # TODO - lookup by IP, some robustness / security on that
    # TODO - throttling by IP
    # parse message & do anything needed
    # send messages back to device
    pass

if __name__ == '__main__':
    server = StreamServer((config.DEVICE_GATEWAY_HOST_LISTEN, config.DEVICE_GATEWAY_PORT_LISTEN), handle, spawn=config.DEVICE_GATEWAY_MAX_CONNECTIONS)
    server.serve_forever()
