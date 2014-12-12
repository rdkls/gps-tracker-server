#!/usr/bin/env python
import socket
import SocketServer
import re
from collections import namedtuple
import time

RECV_SIZE       = 4096
MAX_CONNECTIONS = 1

HOST_LISTEN     = '127.0.0.1'
HOST_LISTEN     = ''
PORT_LISTEN     = 9000

PORT_REMOTE     = 9000
HOST_REMOTE     = '202.104.150.75'
HOST_REMOTE     = '202.104.149.227'

HOST_REMOTE     = '173.248.151.183'
PORT_REMOTE     = 12300


class DataInit(namedtuple('DataInit', [
    'start_delimiter',
    'imei_unparsed',
    'end_delimiter',
])):
    @property
    def imei(self):
        try:
            return re.match('^imei:(\d+)$', self.imei_unparsed).groups()[0]
        except:
            return None

class DataHeartbeat(namedtuple('DataHeartbeat', [
    'imei_unparsed',
])):
    @property
    def imei(self):
        return re.match('^(\d+);$', self.imei_unparsed).groups()[0]

class DataTracker(namedtuple('DataTracker', [
    'imei_unparsed',
    'source',               # 'tracker'
    'local_date',
    'local_time',
    'type',                 # F - full / L - low
    'time',                 # UTC (HHMMSS.SSS)
    'validity',             # A / V
    'latitude',             # DDMM.MMMM
    'latitude_direction',   # N / S
    'longitude',            # DDDMM.MMMM
    'longitude_direction',  # E / W
    'speed',
    'course',
    'altitude',
    'unknown_1',
    'unknown_2',
    'unknown_3',
    'unknown_4',
    'end_delimiter',
])):
    @property
    def imei(self):
        try:
            return re.match('^imei:(\d+)', self.imei_unparsed).groups()[0]
        except:
            return None

class DataOBD(namedtuple('DataOBD', [
    'imei_unparsed',
    'source',
    'local_date',
    'local_time',
    'unknown_1',
    'unknown_2',
    'unknown_3',
    'unknown_4',
    'unknown_5',
    'unknown_6',
    'unknown_7',
    'unknown_8',
    'unknown_9',
    'unknown_10',
    'unknown_11',
    'unknown_12',
    'end_delimiter',
])):
    @property
    def imei(self):
        try:
            return re.match('^imei:(\d+)', self.imei_unparsed).groups()[0]
        except:
            return None
# DataLow = 
class UnrecognizedMessageException(Exception):
    pass

class GPSHandler(SocketServer.StreamRequestHandler):
    def parse_data(self, data):
        if not data:
            return None
        try:
            data = DataTracker(*(data.split(',')))
        except:
            pass
        try:
            data = DataOBD(*(data.split(',')))
        except:
            pass
        try:
            data = DataInit(*(data.split(',')))
        except:
            pass
        try:
            data = DataHeartbeat(*(data.split(',')))
        except:
            pass
        if str == type(data):
            raise UnrecognizedMessageException()
        return data

    def handle(self):
        while True:
            self.data = self.request.recv(RECV_SIZE).strip()
            try:
                self.data = self.parse_data(self.data)
            except UnrecognizedMessageException:
                print 'UNRECOGNIZED MESSAGE: %s' % self.data
                break
            print '%s sent: %s' % (self.client_address[0], self.data)

            if not self.data:
                print 'NO MORE DATA - EXIT'
                break

            # Get stock responses (init/heartbeat) for this IMEI
            resp = self.get_resp(self.data)
            if resp:
                print 'responding: %s' % resp
                self.wfile.write(resp)

            if 'tracker' == getattr(self.data, 'source', None) and 'F' == getattr(self.data, 'type'):
                print self.maps_uri(self.data)

            # Get any queued messages / commands for this IMEI
            if type(self.data) in [DataHeartbeat, DataInit]:
                resp = self.get_queued_message(self.data.imei)
                if resp:
                    print 'responding: %s' % resp
                    self.wfile.write(resp)

            if not self.data:
                time.sleep(1)
            print

    def get_queued_message(self, imei):
        # TODO
        #return None
        # hack to always ask for location, for now
        resp = '**,imei:{imei},{cmd}'.format(imei=imei, cmd='B')
        return resp

    def maps_uri(self, data):
        # TODO - don't know if this is even right, for now just for fun
        if 'S' == data.latitude_direction:
            latitude = -float(data.latitude)/100
        else:
            latitude = float(data.latitude)/100
        if 'W' == data.longitude_direction:
            longitude = -float(data.longitude)/100
        else:
            longitude = float(data.longitude)/100
        return 'http://maps.google.com/?q=%s,%s' % (latitude, longitude)

    def get_resp(self, data):
        if DataInit == type(data):
            resp = 'LOAD'
        elif DataHeartbeat == type(data):
            resp = 'ON'
        else:
            resp = None
        return resp

    def pass_to_remote(self, data, client_src_port=56076):
        """ pass the device's request to remote tracker server,
            returning that server's response (to go back to device)
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', client_src_port))
        s.connect((HOST_REMOTE, PORT_REMOTE))
        s.sendall(data)
        resp = s.recv(RECV_SIZE)
        print 'resp from remote server: %s' % resp
        return resp

class GPSServer(SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    server = GPSServer((HOST_LISTEN, PORT_LISTEN), GPSHandler)
    server.serve_forever()
