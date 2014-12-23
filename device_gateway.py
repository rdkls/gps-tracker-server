#!/usr/bin/env python
from gevent.server import StreamServer
import config
import sys
from models import GPSDevice
from logger import logger

def handle(sock, (clientip, clientport)):
    logger.info('New connection from %s:%s' % (clientip, clientport))
    device = None
    while True:
        data = sock.recv(config.DEVICE_GATEWAY_RECV_SIZE)
        if not data:
            break
        logger.info('%s > %s' % (clientip, data[:256]))
        if not device:
            try:
                device = GPSDevice.get_by_data(data, ipaddr=clientip)
            except Exception, e:
                logger.warning(e.message[:256])
                sock.close()
                return

        device.sent(data)

        resp = device.pop_response()
        while resp:
            sock.send(resp)
            logger.info('%s < %s' % (clientip, resp[:256]))
            resp = device.pop_response()

if __name__ == '__main__':
    server = StreamServer(
        (config.DEVICE_GATEWAY_HOST_LISTEN, config.DEVICE_GATEWAY_PORT_LISTEN),
        handle,
        spawn=config.DEVICE_GATEWAY_MAX_CONNECTIONS
    )
    msg = 'Device Gateway listening on %s:%s' % (config.DEVICE_GATEWAY_HOST_LISTEN, config.DEVICE_GATEWAY_PORT_LISTEN)
    print msg
    logger.info(msg)
    server.serve_forever()
