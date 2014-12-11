from .message import Message

class Adapter():
    @classmethod
    def decode(cls, datastring):
        # string data -> return standard 'Message'
        raise NotImplementedException()

    @classmethod
    def encode(cls, datastring):
        # Message -> string data
        # return standard 'Message'
        raise NotImplementedException()

    @classmethod
    def response_to(cls, datastring):
        # Message -> string data
        # return standard 'Message'
        raise NotImplementedException()

    @classmethod
    def detect(cls, data):
        from .tk102 import tk102
        if tk102.decode(data):
            return tk102
