import config
import mongoengine
from adapter.adapter import Adapter

mongoengine.connect(config.MONGO_DBNAME, host=config.MONGO_HOST, port=config.MONGO_PORT)

class Message(mongoengine.Document):
    message_type = mongoengine.StringField()
    imei = mongoengine.StringField()
    message_type = mongoengine.StringField()
    message_datastring = mongoengine.StringField()
    
    def __str__(self):
        return u'Message type %s, IMEI %s' % (self.message_type, self.imei)

class GPSDevice():
    """ Base class for single GPS device
        Model for saving / retrieving to database
        Methods for encoding/decoding messages to/from device
    """
    def __init__(self, imei=None, ipaddr=None, protocol=None):
        self.imei = imei
        self.ipaddr = ipaddr
        self.adapter = None
        self.last_data = None
        self.responses = []
        # TODO - check for imei / ip and retrieve if possible

    def pop_response(self):
        """ Get the current response, taking into account data read, and messages waiting
        """
        try:
            return self.responses.pop(0)
        except IndexError:
            return None

    def sent(self, data):
        if not self.adapter:
            self.adapter = Adapter.detect(data)

        # Set IMEI, if needed
        message = self.adapter.decode(data)
        if not self.imei:
            self.imei = message.imei

        # Determine any stock responses for this type of adapter (e.g. LOAD, ON)
        response = self.adapter.response_to(data)
        if response:
            self.responses.append(response)

        # TODO - hardcode
        message = Message(imei=self.imei, message_type=config.MESSAGE_TYPE_REQ_LOCATION)
        response = self.adapter.encode(message)
        self.responses.append(response)
