import logging


class apiLogger():

    def __init__(self, LoggerName=__name__):
        self.logger = logging.getLogger(LoggerName)

    def logDebug(self, msg, controllerIp=None):
        extras = dict({'ip': controllerIp})
        self.logger.debug(msg, extra=extras)

    def logInfo(self, msg, controllerIp=None):
        extras = dict({'ip': controllerIp})
        self.logger.info(msg, extra=extras)

    def logWarning(self, msg, controllerIp=None):
        extras = dict({'ip': controllerIp})
        self.logger.warning(msg, extra=extras)

    def logError(self, msg, controllerIp=None):
        extras = dict({'ip': controllerIp})
        self.logger.error(msg, extra=extras)

    def logCritical(self, msg, controllerIp=None):
        extras = dict({'ip': controllerIp})
        self.logger.critical(msg, extra=extras)

    def logException(self, msg, controllerIp=None):
        extras = dict({'ip': controllerIp})
        self.logger.critical(msg, extra=extras)
