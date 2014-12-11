
class Message():
    def __init__(self, message_type=None, imei=None):
        self.imei = imei
        self.message_type = message_type

    def __str__(self):
        return u'Message type %s, IMEI %s' % (self.message_type, self.imei)
