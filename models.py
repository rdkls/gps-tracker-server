

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
        pass

    @property
    def get_response(self):
        """ Get the current response, taking into account data read, and messages waiting
        """
        try:
            return self.responses.pop(0)
        except IndexError:
            return None

    def sent(self, data):
        self.last_data = data
        if not self.adapter:
            from adapter.util import detect_adapter
            self.adapter = detect_adapter(data)

        # Set IMEI, if needed
        message = self.adapter.decode(data)
        if not self.imei:
            self.imei = message.imei

        # Determine any stock responses for this type of adapter (e.g. LOAD, ON)
        response = self.adapter.response_to(data)
        if response:
            self.responses.append(response)

        # TODO Get any response messages from the Queue
