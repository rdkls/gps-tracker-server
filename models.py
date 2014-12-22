import config
import bcrypt
import datetime
import mongoengine
import random
import hashlib

from adapter.adapter import Adapter

mongoengine.connect(config.MONGO_DBNAME, host=config.MONGO_HOST, port=config.MONGO_PORT)


class Message(mongoengine.Document):
    message_type = mongoengine.StringField()
    state = mongoengine.StringField(default=config.MESSAGE_STATE_INITIAL)
    imei = mongoengine.StringField()
    message_datastring = mongoengine.StringField()
    latitude = mongoengine.DecimalField()
    longitude = mongoengine.DecimalField()
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    
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


class GPSDevice(mongoengine.Document):
    imei = mongoengine.StringField(unique=True)
    ipaddr = mongoengine.StringField()
    name = mongoengine.StringField()
    licence_plate = mongoengine.StringField()

    # list of responses (data strings, encoded for device) to be sent to device
    responses = mongoengine.ListField(mongoengine.StringField())

    # the adapter for encode/decode messages to/from device
    adapter = None
    latitude = mongoengine.DecimalField()
    longitude = mongoengine.DecimalField()

    @property
    def is_online(self):
        if not self.imei:
            return False
        if Message.objects.filter(imei=self.imei, created__gte=datetime.datetime.utcnow() - datetime.timedelta(minutes=config.DEVICE_OFFLINE_TIMEOUT_MINUTES)):
            return True
        return False

    @property
    def user(self):
        try:
            return User.objects.get(devices=self)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_by_data(cls, datastring, ipaddr=None):
        adapter = Adapter.detect(datastring)
        if not adapter:
            raise Exception("Couldn't determine adapter from datastring: %s" % datastring)

        message = adapter.decode(datastring)

        if not message.imei:
            raise Exception("Couldn't get imei from datastring: %s" % datastring)

        """ Try retrieving device from db
            If none already, create a new one and return it
        """
        try:
            device = GPSDevice.objects.get(imei=message.imei)
        except mongoengine.DoesNotExist:
            device = GPSDevice(imei=message.imei, ipaddr=ipaddr)
            device.save()
        except mongoengine.MultipleObjectsReturned:
            raise mongoengine.MultipleObjectsReturned('Found more than one device with imei %s' % message.imei)
        if ipaddr and ipaddr != device.ipaddr:
            device.ipaddr = ipaddr
            device.save()
        return device
        

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
            if not message:
                break
            if not self.imei:
                self.imei = message.imei
            message.state = config.MESSAGE_STATE_RECEIVED
            message.save()

            # Determine any stock responses for this type of adapter (e.g. LOAD, ON)
            response = self.adapter.response_to(message)
            if response:
                self.responses.append(response)

            # If it's a location message, record this
            if config.MESSAGE_TYPE_LOCATION_FULL == message.message_type:
                self.latitude = message.latitude
                self.longitude = message.longitude
                self.save()
                maps_url = config.GOOGLE_MAPS_URI_FORMAT.format(latitude=message.latitude, longitude=message.longitude)
                print 'received location from %s: %s' % (self.imei, maps_url)

        # Get & send responses from queue
        self.retrieve_messages()

    def retrieve_messages(self):
        if not self.imei:
            return
        m = Message.dequeue_response(imei=self.imei)
        while m:
            self.responses.append(self.adapter.encode(m))
            m = Message.dequeue_response(imei=self.imei)

    def delete(self):
        User.objects.update(pull__devices=self.id)
        super(GPSDevice, self).delete()

    def __str__(self):
        return 'GPSDevice imei %s, ip %s' % (self.imei, self.ipaddr)


class User(mongoengine.Document):
    email = mongoengine.EmailField(required=True, unique=True)
    password = mongoengine.StringField(required=True)
    api_key = mongoengine.StringField()
    devices = mongoengine.ListField(mongoengine.ReferenceField(GPSDevice))

    @classmethod
    def check_api_key(self, api_key):
        try:
            return User.objects.get(api_key=api_key)
        except User.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        if not self.id and self.password:
            self.password = bcrypt.hashpw(self.password, salt=bcrypt.gensalt())
        if not self.api_key:
            self.api_key = hashlib.sha1(str(random.random())).hexdigest()
        super(User, self).save(*args, **kwargs)

    def check_password(self, password_to_check):
        return bcrypt.checkpw(hashed_password=self.password, password=password_to_check)

    def set_password(self, password):
        if not self.id:
            raise Exception('user.set_password() can only be called after user has been saved')
        self.password = bcrypt.hashpw(password, salt=bcrypt.gensalt())

    def __str__(self):
        return self.email
