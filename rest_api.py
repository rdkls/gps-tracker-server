#!/usr/bin/env python
from flask import Flask
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest import methods
from flask.ext.mongorest import operators
from flask import request
from werkzeug.exceptions import NotFound, Unauthorized

from models import *

app = Flask(__name__)
api = MongoRest(app)

class DeviceResource(Resource):
    document = GPSDevice

class UserResource(Resource):
    uri_prefix = '/users/'
    document = User

class MessageResource(Resource):
    document = Message
    filters = {
        'imei'  : [operators.Exact],
    }


@api.register(name='messages', url='/messages/')
class MessageView(ResourceView):
    resource = MessageResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

@api.register(name='users', url='/users/')
class UserView(ResourceView):
    resource = UserResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

    def post(self, **kwargs):
        if 'pk' in kwargs:
            raise NotFound()
        self._resource.validate_request()
        obj = self._resource.create_object()
        obj.set_password(obj.password)
        ret = self._resource.serialize(obj, request.args)
        return ret

@api.register(name='devices', url='/devices/')
class DeviceView(ResourceView):
    resource = DeviceResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
