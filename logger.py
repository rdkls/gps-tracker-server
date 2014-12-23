import logging
import logging.handlers
import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
handler = logging.handlers.RotatingFileHandler(filename=config.DEVICE_GATEWAY_LOGFILE, mode='a', maxBytes=5*1000*1000, backupCount=10)
handler.setFormatter(formatter)
logger.addHandler(handler)
