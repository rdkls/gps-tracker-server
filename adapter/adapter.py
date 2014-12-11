
class Adapter():
    @classmethod
    def decode(cls, datastring):
        # Given string data from a device, decode -> return standard 'Message'
        raise NotImplementedError()

    @classmethod
    def encode(cls, message):
        # Given a Message, encode -> string data to send to device
        raise NotImplementedError()

    @classmethod
    def response_to(cls, datastring):
        # For this adapter, get response (Message) to one datastring
        raise NotImplementedError()

    @classmethod
    def detect(cls, datastring):
        # Given a datastring, determine adapter type it's for
        # and return this adapter's class
        from .tk102 import tk102
        if tk102.decode(datastring):
            return tk102
