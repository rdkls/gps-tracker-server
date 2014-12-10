#!/usr/bin/env python
import socket
import SocketServer
import re

RECV_SIZE       = 4096
MAX_CONNECTIONS = 1

HOST_LISTEN     = ''
PORT_LISTEN     = 9000

PORT_GPSTRACKERXY   = 9000
HOST_GPSTRACKERXY   = '202.104.150.75'
#PORT_SOURCE     = 56076

class GPSHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        self.data = self.request.recv(RECV_SIZE).strip()
        print '%s sent: %s' % (self.client_address[0], self.data)
        (client_ip, client_src_port) = self.request.getpeername()
        resp = self.get_resp(self.data)
        print 'responding: %s' % resp
        self.wfile.write(resp)
        self.request.close()
        print

    def get_resp(self, data):
        imei = None

        re_imei_start   = '^##,imei:(\d+),A;$'
        re_imei_only    = '^(\d+);$'

        if re.match(re_imei_start, data):
            resp = 'LOAD'
            imei = re.match(re_imei_start, data).groups()[0]
        elif re.match(re_imei_only, data):
            resp = 'ON'
            imei = re.match(re_imei_only, data).groups()[0]

            # hack to always ask for location, for now
            cmd = 'B'
            if cmd:
                resp = 'ON**,imei:{imei},{cmd}'.format(imei=imei, cmd=cmd)
        else:
            resp = None

        if imei:
            print 'IMEI %s' % imei

        #resp = self.pass_to_gpstrackerxy(data)
        return resp

    def pass_to_gpstrackerxy(self, data, client_src_port=56076):
        """ pass the device's request to gpstrackerxy server,
            returning that server's response (to go back to device)
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', client_src_port))
        s.connect((HOST_GPSTRACKERXY, PORT_GPSTRACKERXY))
        s.sendall(data)
        return s.recv(RECV_SIZE)

class GPSServer(SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    server = GPSServer((HOST_LISTEN, PORT_LISTEN), GPSHandler)
    server.serve_forever()
