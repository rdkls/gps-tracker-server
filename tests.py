
from models import Message

def test_message_fifo():
    imei = 'test1'

    # Maybe we need to clean up some from previous run
    m = Message.dequeue_response(imei=imei)
    m = Message.dequeue_response(imei=imei)
    m = Message.dequeue_response(imei=imei)

    Message(imei=imei, message_datastring='111').save()
    Message(imei=imei, message_datastring='222').save()
    Message(imei=imei, message_datastring='333').save()

    m = Message.dequeue_response(imei=imei)
    print m
    assert('111' == m.message_datastring)

    m = Message.dequeue_response(imei=imei)
    print m
    assert('222' == m.message_datastring)

    m = Message.dequeue_response(imei=imei)
    print m
    assert('333' == m.message_datastring)

    m = Message.dequeue_response(imei=imei)
    assert(None == m)
    m = Message.dequeue_response(imei=imei)
    assert(None == m)
    m = Message.dequeue_response(imei=imei)
    assert(None == m)
