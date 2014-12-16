#!/usr/bin/env python
import json
import config
import sys
from gevent.pywsgi import WSGIServer
from flask import Flask, request
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest
from models import *

app = Flask(__name__)
app.debug = True


def check_auth():
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        raise Unauthorized()
    u = User.check_api_key(api_key)
    if not u:
        raise Unauthorized()
    return u


@app.route('/login/', methods=['POST'])
def login():
    try:
        d = json.loads(request.data)
        email = d['email']
        password = d['password']
    except:
        raise BadRequest()
    try:
        u = User.objects.get(email=email)
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        raise Unauthorized()
    if u.check_password(password):
        return json.dumps({'api_key': u.api_key})
    raise Unauthorized()


@app.route('/user/<user_id>', methods=['GET'])
@app.route('/user/', methods=['GET'])
def user_list(user_id=None):
    user = check_auth()
    if user_id:
        try:
            u = User.objects.get(id=user_id)
        except:
            raise NotFound()
        resp = {
            '_id'       : str(u.id),
            'email'     : str(u.email),
            'devices'   : [str(d.id) for d in u.devices],
        }
    else:
        resp = []
        for u in User.objects.filter(id=user.id):
            resp.append({
                '_id'       : str(u.id),
                'email'     : str(u.email),
                'devices'   : [str(d.id) for d in u.devices],
            })
    return json.dumps(resp)


@app.route('/device/<device_id>', methods=['GET'])
@app.route('/device/', methods=['GET'])
def devices(device_id=None):
    user = check_auth()
    if device_id:
        try:
            d = filter(lambda d:str(d.id)==device_id, user.devices)[0]
            resp = {
                'id'            : str(d.id),
                'imei'          : d.imei,
                'ipaddr'        : d.ipaddr,
                'is_online'     : d.is_online,
                'latitude'      : d.latitude,
                'longitude'     : d.longitude,
            }
        except:
            raise NotFound()
    else:
        resp = []
        for d in user.devices:
            d = {
                'id'            : str(d.id),
                'imei'          : d.imei,
                'ipaddr'        : d.ipaddr,
                'is_online'     : d.is_online,
                'latitude'      : d.latitude,
                'longitude'     : d.longitude,
            }
            resp.append(d)
    return json.dumps(resp)


if __name__=='__main__':
    http = WSGIServer(('', 5000), app)
    http.serve_forever()
