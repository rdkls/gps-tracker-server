#!/usr/bin/env python
from gevent.server import StreamServer
import config
import sys
from models import GPSDevice

def handle(sock, (clientip, clientport)):
    print
    print 'new connection from %s:%s' % (clientip, clientport)

    device = None
    while True:
        data = sock.recv(config.DEVICE_GATEWAY_RECV_SIZE)
        if not data:
            break
        print '%s > %s' % (clientip, data)
        if not device:
            device = GPSDevice.get_by_data(data, ipaddr=clientip)
        device.sent(data)

        resp = device.pop_response()
        while resp:
            sock.send(resp)
            print '%s < %s' % (clientip, resp)
            resp = device.pop_response()

if __name__ == '__main__':
    server = StreamServer((config.DEVICE_GATEWAY_HOST_LISTEN, config.DEVICE_GATEWAY_PORT_LISTEN), handle, spawn=config.DEVICE_GATEWAY_MAX_CONNECTIONS)
    print 'Device Gateway listening on %s:%s' % (config.DEVICE_GATEWAY_HOST_LISTEN, config.DEVICE_GATEWAY_PORT_LISTEN)
    server.serve_forever()
