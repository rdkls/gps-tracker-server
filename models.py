import config
import datetime
import mongoengine
from adapter.adapter import Adapter

mongoengine.connect(config.MONGO_DBNAME, host=config.MONGO_HOST, port=config.MONGO_PORT)


class Message(mongoengine.Document):
    message_type = mongoengine.StringField()
    state = mongoengine.StringField(default=config.MESSAGE_STATE_INITIAL)
    imei = mongoengine.StringField()
    message_datastring = mongoengine.StringField()
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    latitude = mongoengine.StringField()
    longitude = mongoengine.StringField()
    
    @classmethod
    def dequeue_response(self, imei):
        collection = mongoengine.connection.get_db()['message']
        resp = collection.find_and_modify(
            query = {'imei': imei, 'state': config.MESSAGE_STATE_INITIAL},
            sort = {'created': 1},
            update = {'$set': {'state': config.MESSAGE_STATE_SENT}},
        )
        if resp:
            return Message(**resp)

    def __str__(self):
        return u'Message type: %s, IMEI: %s, state: %s' % (self.message_type, self.imei, self.state)


class GPSDevice():
    """ Base class for single GPS device
        Later - Model for saving / retrieving to database
        Methods for encoding/decoding messages to/from device
    """
    def __init__(self, imei=None, ipaddr=None, protocol=None):
        self.imei = imei
        self.ipaddr = ipaddr
        self.adapter = None
        self.responses = []

    def pop_response(self):
        """ Get the current response, taking into account data read, and messages waiting
        """
        try:
            return self.responses.pop(0)
        except IndexError:
            return None

    def sent(self, datastring):
        if not self.adapter:
            self.adapter = Adapter.detect(datastring)
        if not self.adapter:
            raise Exception("Coudln't determine adapter from datastring: %s" % datastring)

        # Possibly multiple messages in datastring, separated by delimiter
        for messagestring in filter(lambda x:x, datastring.split(self.adapter.delimiter)):
            # Set IMEI, if needed
            message = self.adapter.decode(messagestring)
            #print message
            if not message:
                break
            if not self.imei:
                self.imei = message.imei

            # Determine any stock responses for this type of adapter (e.g. LOAD, ON)
            response = self.adapter.response_to(message)
            if response:
                self.responses.append(response)

            # If it's a location message, record this
            if config.MESSAGE_TYPE_LOCATION_FULL == message.message_type:
                maps_url = config.GOOGLE_MAPS_URI_FORMAT.format(latitude=message.latitude, longitude=message.longitude)
                print 'received location: '
                print maps_url

        # Get & send responses from queue
        self.retrieve_messages()

    def retrieve_messages(self):
        if not self.imei:
            return
        m = Message.dequeue_response(imei=self.imei)
        while m:
            self.responses.append(self.adapter.encode(m))
            m = Message.dequeue_response(imei=self.imei)
