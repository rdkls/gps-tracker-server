from .tk102 import tk102

tk102_heartbeat_string = '865328021048409;'
tk102_location_low_string = 'imei:865328021048409,tracker,141210172556,0411959136,L,,,0BD4,,7A78,,,,,0,0,0.0%,,;'
tk102_location_full_string = 'imei:865328021048409,tracker,141210110820,,F,030823.000,A,3745.9502,S,14458.2049,E,1.83,119.35,,0,0,0.0%,,;'
tk102_init_string = '##,imei:865328021048409,A;'

def test_tk102_location_low():
    message = tk102.decode(tk102_location_low_string)
    print message
    assert(message)
    assert(str==type(message.imei))

def test_tk102_location_full():
    message = tk102.decode(tk102_location_full_string)
    print message
    assert(message)
    assert(str==type(message.imei))

def test_tk102_init():
    message = tk102.decode(tk102_init_string)
    assert(message)
    assert(str==type(message.imei))

def test_tk102_hb():
    message = tk102.decode(tk102_heartbeat_string)
    assert(message)
    assert(str==type(message.imei))

def test_tk102_bad():
    message = tk102.decode('A BAD DATASTRING')
    assert(None==message)


def test_detect():
    #from .util import detect_adapter
    from .adapter import Adapter
    assert(tk102 == Adapter.detect(tk102_init_string))
    assert(tk102 == Adapter.detect(tk102_heartbeat_string))
    assert(tk102 == Adapter.detect(tk102_location_full_string))
    assert(tk102 == Adapter.detect(tk102_location_low_string))
