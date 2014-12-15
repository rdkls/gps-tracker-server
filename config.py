MONGO_HOST                      = '127.0.0.1'
MONGO_PORT                      = 27017
MONGO_DBNAME                    = 'gpstrack'

DEVICE_GATEWAY_MAX_CONNECTIONS  = 100
DEVICE_GATEWAY_HOST_LISTEN      = '127.0.0.1'
DEVICE_GATEWAY_HOST_LISTEN      = ''
DEVICE_GATEWAY_PORT_LISTEN      = 9000
DEVICE_GATEWAY_RECV_SIZE        = 4096

DEVICE_OFFLINE_TIMEOUT_MINUTES  = 1 

MESSAGE_TYPE_INIT               = 'init'
MESSAGE_TYPE_HEARTBEAT          = 'heartbeat'
MESSAGE_TYPE_LOCATION_FULL      = 'location_full'
MESSAGE_TYPE_LOCATION_LOW       = 'location_low'
MESSAGE_TYPE_OBD                = 'obd'
MESSAGE_TYPE_REQ_LOCATION       = 'req_location'

MESSAGE_STATE_INITIAL           = 'initial'
#MESSAGE_STATE_PENDING          = 'pending'
MESSAGE_STATE_SENT              = 'sent'
MESSAGE_STATE_RECEIVED          = 'received'

GOOGLE_MAPS_URI_FORMAT          = 'https://maps.google.com.au/?q={latitude},{longitude}'

EVE_SETTINGS = {
    'MONGO_HOST'        : MONGO_HOST,
    'MONGO_PORT'        : MONGO_PORT,
    'MONGO_DBNAME'      : MONGO_DBNAME,
    'DOMAIN'            : {'eve-mongoengine': {}} # sadly this is needed for eve
}
