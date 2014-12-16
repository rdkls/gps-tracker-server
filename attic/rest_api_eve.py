#!/usr/bin/env python
import config
from flask import request
from eve import Eve
from eve_mongoengine import EveMongoengine
from eve.auth import TokenAuth

from models import *

class ApiTokenAuth(TokenAuth):
    def authorized(self, allowed_roles, resource, method):
        token = request.headers.get(config.EVE_AUTH_HEADER_NAME)
        if User.check_api_token(token):
            return True
        else:
            return False

if __name__=='__main__':
    app = Eve(auth=ApiTokenAuth, settings=config.EVE_SETTINGS)
    ext = EveMongoengine(app)
    ext.add_model(User)
    ext.add_model(Message)
    ext.add_model(GPSDevice)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
