import re
import config
from .adapter import Adapter
from models import Message

class tk102(Adapter):
    delimiter = ';'

    @classmethod
    def decode(cls, datastring):
        # e.g. ##,imei:865328021048409,A;
        re_init = '^##,imei:(?P<imei>\d{15}),A'

        # e.g. 865328021048409;
        re_heartbeat = '^(?P<imei>\d{15})'

        # e.g. imei:865328021048409,tracker,141210110820,,F,030823.000,A,3745.9502,S,14458.2049,E,1.83,119.35,,0,0,0.0%,,;
        re_location_full = '^imei:(?P<imei>\d{15}),' + \
            'tracker,' + \
            '(?P<local_date>\d*),' + \
            '(?P<local_time>\d*),' + \
            'F,' + \
            '(?P<time_utc>\d+\.\d+)?,' + \
            '(?P<validity>[AV]),' + \
            '(?P<latitude>\d+\.\d+),' + \
            '(?P<latitude_hemisphere>[NS]),' + \
            '(?P<longitude>\d+\.\d+),' + \
            '(?P<longitude_hemisphere>[EW]),' + \
            ''
        """
            '(?P<speed>\d+\.\d+)?,' + \
            '(?P<course>\d+\.\d+)?,' + \
            '(?P<altitude>\d+\.\d+)?,' + \
            '.*;'
        """

        # e.g. imei:865328021048409,tracker,141210172556,0411959136,L,,,0BD4,,7A78,,,,,0,0,0.0%,,;
        re_location_low = '^imei:(?P<imei>\d{15}),' + \
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

        if re.match(re_init, datastring):
            imei = re.match(re_init, datastring).group('imei')
            message = Message(imei=imei, message_type=config.MESSAGE_TYPE_INIT, message_datastring=datastring)
        elif re.match(re_heartbeat, datastring):
            imei = re.match(re_heartbeat, datastring).group('imei')
            message = Message(imei=imei, message_type=config.MESSAGE_TYPE_HEARTBEAT, message_datastring=datastring)
        elif re.match(re_location_full, datastring):
            match = re.match(re_location_full, datastring)
            imei = match.group('imei')
            message = Message(imei=imei, message_type=config.MESSAGE_TYPE_LOCATION_FULL, message_datastring=datastring)

            latitude = match.group('latitude')
            latitude_hemisphere = match.group('latitude_hemisphere')
            longitude = match.group('longitude')
            longitude_hemisphere = match.group('longitude_hemisphere')

            # Latitude and Longitude need to be converted from this proto's spec to standard decimal
            # Locations come as HHHHMM.MMMM
            # hours are any number of digits, followed by
            # seconds which are 2-digit integer part, period, fractional part
            re_location = '^(\d+)(\d{2}\.\d+)$'

            (h, m) = re.match(re_location, latitude).groups()
            h = float(h)
            m = float(m)
            latitude = h + m/60
            if 'S' == latitude_hemisphere:
                latitude = -latitude

            (h, m) = re.match(re_location, longitude).groups()
            h = float(h)
            m = float(m)
            longitude = h + m/60
            if 'W' == longitude_hemisphere:
                longitude = -longitude

            message.latitude = latitude
            message.longitude = longitude
            # TODO - set other message properties
        elif re.match(re_location_low, datastring):
            imei = re.match(re_location_low, datastring).group('imei')
            message = Message(imei=imei, message_type=config.MESSAGE_TYPE_LOCATION_LOW, message_datastring=datastring)
            # TODO - set other message properties
        else:
            return None
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
    def response_to(cls, message):
        if type(message) in [str, unicode]:
            message = cls.decode(data)
        if not message:
            return
        if config.MESSAGE_TYPE_INIT == message.message_type:
            return 'LOAD'
        elif config.MESSAGE_TYPE_HEARTBEAT == message.message_type:
            return 'ON'

