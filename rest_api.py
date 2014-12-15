#!/usr/bin/env python
import config
from eve import Eve
from eve_mongoengine import EveMongoengine

from models import *

if __name__=='__main__':
    app = Eve(settings=config.EVE_SETTINGS)
    ext = EveMongoengine(app)
    ext.add_model(User)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
