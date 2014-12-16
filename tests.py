import config
import sys
import mongoengine
import unittest
from models import Message
from models import GPSDevice
from models import User

tk102_heartbeat_string = u'865328021048409;'
tk102_location_low_string = 'imei:865328021048409,tracker,141210172556,0411959136,L,,,0BD4,,7A78,,,,,0,0,0.0%,,;'
tk102_location_full_string = 'imei:865328021048409,tracker,141210110820,,F,030823.000,A,3745.9502,S,14458.2049,E,1.83,119.35,,0,0,0.0%,,;'
tk102_init_string = '##,imei:865328021048409,A;'
tk102_datastrings = [
    tk102_heartbeat_string,
    tk102_location_low_string,
    tk102_location_full_string,
    tk102_init_string,
]

class TestModels(unittest.TestCase):
    def setUp(self):
        User.objects.delete({'email':'test@test.com'})
        self.user = User(email='test@test.com', password='test')
        self.user.save()

        GPSDevice.objects.delete({'imei':'test'})
        self.device = GPSDevice(imei='test')
        self.device.save()

        self.user.devices.append(self.device)
        self.user.save()

    def tearDown(self):
        self.user.delete()
        self.device.delete()

    # User
    def test_user(self):
        assert(self.user.check_password('test'))

    # GPSDevice
    def test_device_user(self):
        assert(self.user==self.device.user)

    def test_unique_imei(self):
        try:
            d = GPSDevice(imei='test')
            d.save()
        except mongoengine.NotUniqueError, e:
            pass
        assert(mongoengine.NotUniqueError == type(e))

    def test_device_get_by_data_bad(self):
        e = None
        try:
            device = GPSDevice.get_by_data('x')
        except Exception, e:
            pass
        assert(Exception==type(e))

    def test_device_get_by_data_good(self):
        for s in tk102_datastrings:
            device = GPSDevice.get_by_data(s)
            assert(GPSDevice==type(device))
            assert(unicode==type(device.imei))

    # Messages
    def test_location_req(self):
        m = Message()
        m.imei = '865328021048409'
        m.message_type = config.MESSAGE_TYPE_REQ_LOCATION
        m.save()

    def test_message_fifo(self):
        imei = 'test1'

        # Maybe we need to clean up some from previous run
        m = Message.dequeue_response(imei=imei)
        m = Message.dequeue_response(imei=imei)
        m = Message.dequeue_response(imei=imei)

        Message(imei=imei, message_datastring='111').save()
        Message(imei=imei, message_datastring='222').save()
        Message(imei=imei, message_datastring='333').save()

        m = Message.dequeue_response(imei=imei)
        assert('111' == m.message_datastring)

        m = Message.dequeue_response(imei=imei)
        assert('222' == m.message_datastring)

        m = Message.dequeue_response(imei=imei)
        assert('333' == m.message_datastring)

        m = Message.dequeue_response(imei=imei)
        assert(None == m)
        m = Message.dequeue_response(imei=imei)
        assert(None == m)
        m = Message.dequeue_response(imei=imei)
        assert(None == m)

    def test_gpsdevice_sent(self):
        d = GPSDevice.get_by_data(tk102_init_string)
        d.sent(tk102_init_string)
        d.sent(tk102_heartbeat_string)
        d.sent(tk102_location_full_string)
        assert(d.imei)
        assert(d.latitude)
        assert(d.longitude)

    def test_gpsdevice_tk102_response_init(self):
        self.device.sent(tk102_init_string)
        assert(self.device.imei)
        r = self.device.pop_response()
        assert('LOAD'==r)

    def test_gpsdevice_tk102_response_multi(self):
        self.device.sent(tk102_init_string + tk102_heartbeat_string)
        assert(self.device.imei)
        r = self.device.pop_response()
        assert('LOAD'==r)
        r = self.device.pop_response()
        assert('ON'==r)

    def test_gpsdevice_tk102_response_hb(self):
        self.device.sent(tk102_heartbeat_string)
        assert(self.device.imei)
        r = self.device.pop_response()
        assert('ON'==r)

    def test_gpsdevice_tk102_response_location(self):
        d = GPSDevice.get_by_data(tk102_location_full_string)
        d.sent(tk102_location_full_string)

    def test_device_online(self):
        d = GPSDevice()
        assert(False==d.is_online)

