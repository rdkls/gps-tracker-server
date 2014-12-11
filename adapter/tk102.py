import re
import config
from .adapter import Adapter
from models import Message

class tk102(Adapter):
    @classmethod
    def decode(cls, datastring):
        # e.g. ##,imei:865328021048409,A;
        re_init = '^##,imei:(?P<imei>\d+),A;$'

        # e.g. 865328021048409;
        re_heartbeat = '^(?P<imei>\d+);$'

        # e.g. imei:865328021048409,tracker,141210110820,,F,030823.000,A,3745.9502,S,14458.2049,E,1.83,119.35,,0,0,0.0%,,;
        re_location_full = '^imei:(?P<imei>\d+),' + \
            'tracker,' + \
            '(?P<local_date>\d*),' + \
            '(?P<local_time>\d*),' + \
            'F,' + \
            '(?P<time_utc>\d+\.\d+)?,' + \
            '(?P<validity>[AV]),' + \
            '(?P<latitude>\d+\.\d+),' + \
            '(?P<latitude_direction>)[NS],' + \
            '(?P<longitude>\d+\.\d+),' + \
            '(?P<longitude_direction>[EW]),' + \
            '(?P<speed>\d+\.\d+)?,' + \
            '(?P<course>\d+\.\d+)?,' + \
            '(?P<altitude>\d+\.\d+)?,' + \
            '.*;'

        # e.g. imei:865328021048409,tracker,141210172556,0411959136,L,,,0BD4,,7A78,,,,,0,0,0.0%,,;
        re_location_low = '^imei:(?P<imei>\d+),' + \
            'tracker,' + \
            '(?P<local_date>\d*),' + \
            '(?P<local_time>\d*),' + \
            'L,' + \
            '[^,]*,' + \
            '[^,]*,' + \
            '(?P<unknown_1>\w*),' + \
            '[^,]*,' + \
            '(?P<unknown_2>\w*),' + \
            ''

        message = None
        if re.match(re_init, datastring):
            imei = re.match(re_init, datastring).group('imei')
            message = Message(imei=imei, message_type=config.MESSAGE_TYPE_INIT)
        elif re.match(re_heartbeat, datastring):
            imei = re.match(re_heartbeat, datastring).group('imei')
            message = Message(imei=imei, message_type=config.MESSAGE_TYPE_HEARTBEAT)
        elif re.match(re_location_full, datastring):
            imei = re.match(re_location_full, datastring).group('imei')
            message = Message(imei=imei, message_type=config.MESSAGE_TYPE_LOCATION_FULL)
            # todo - set other message properties
        elif re.match(re_location_low, datastring):
            imei = re.match(re_location_low, datastring).group('imei')
            message = Message(imei=imei, message_type=config.MESSAGE_TYPE_LOCATION_LOW)
            # todo - set other message properties
        return message

    @classmethod
    def encode(cls, message):
        """
        message asking that device report location once
        #resp = '**,imei:{imei},{cmd}'.format(imei=imei, cmd='B')
        """
        if config.MESSAGE_TYPE_REQ_LOCATION == message.message_type:
            resp = '**,imei:{imei},{cmd}'.format(imei=message.imei, cmd='B')
            return resp

    @classmethod
    def response_to(cls, data):
        message = cls.decode(data)
        if not message:
            return
        if config.MESSAGE_TYPE_INIT == message.message_type:
            return 'LOAD'
        elif config.MESSAGE_TYPE_HEARTBEAT == message.message_type:
            return 'ON'

