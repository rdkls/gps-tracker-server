MONGO_HOST                      = '127.0.0.1'
MONGO_PORT                      = 27017
MONGO_DBNAME                    = 'gpstrack'

DEVICE_GATEWAY_MAX_CONNECTIONS  = 100
DEVICE_GATEWAY_HOST_LISTEN      = '127.0.0.1'
DEVICE_GATEWAY_PORT_LISTEN      = 9000

MESSAGE_TYPE_INIT               = 'init'
MESSAGE_TYPE_HEARTBEAT          = 'heartbeat'
MESSAGE_TYPE_LOCATION_FULL      = 'location_full'
MESSAGE_TYPE_LOCATION_LOW       = 'location_low'
MESSAGE_TYPE_OBD                = 'obd'
MESSAGE_TYPE_REQ_LOCATION       = 'req_location'

MESSAGE_STATUS_INITIAL          = 'initial'
MESSAGE_STATUS_PENDING          = 'pending'
MESSAGE_STATUS_SENT             = 'sent'
