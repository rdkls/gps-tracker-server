import config
import unittest
import sys
import mongoengine
from models import *
from rest_api import *

class TestApi(unittest.TestCase):

    def setUp(self):
        User.objects.filter(email='test@test.com').delete()
        self.user = User()
        self.user = User(email='test@test.com', password='test')
        self.user.save()

        GPSDevice.objects.filter(imei='test').delete()
        self.device = GPSDevice(imei='test')
        self.device.save()
        self.user.devices.append(self.device)
        self.user.save()

        self.client = app.test_client()
  
    def tearDown(self):
        self.device.delete()
        self.user.delete()

    def test_login(self):
        resp = self.client.post('/login/', data=json.dumps({
            'email'     : 'test@test.com',
            'password'  : 'test',
        }))
        api_key = json.loads(resp.data)['api_key']
        assert(api_key==self.user.api_key)

    def test_login_badpw(self):
        resp = self.client.post('/login/', data=json.dumps({
            'email'     : 'test@test.com',
            'password'  : 'bad',
        }))
        assert(401==resp.status_code)

    def test_login_baduser(self):
        resp = self.client.post('/login/', data=json.dumps({
            'email'     : 'bad@bad.com',
            'password'  : 'bad',
        }))
        assert(401==resp.status_code)

    def test_user_list(self):
        resp = self.client.get('/user/', headers={'X-API-KEY': self.user.api_key})
        assert(200==resp.status_code)
        assert(1==len(json.loads(resp.data)))

    def test_user_details(self):
        resp = self.client.get('/user/%s' % self.user.id, headers={'X-API-KEY': self.user.api_key})
        assert(200==resp.status_code)
        assert('test@test.com'==json.loads(resp.data)['email'])

    def test_device_list(self):
        resp = self.client.get('/device/', headers={'X-API-KEY': self.user.api_key})
        assert(200==resp.status_code)
        assert(1==len(json.loads(resp.data)))

    def test_device_details(self):
        resp = self.client.get('/device/%s' % self.device.id, headers={'X-API-KEY': self.user.api_key})
        assert(200==resp.status_code)
        assert('test'==json.loads(resp.data)['imei'])
