from selfInstall.api.auth.decorators import tokenRequired
from CiscoFunctions.CiscoWlcFunctions import CiscoWlcFunctions
from selfInstall.api.apStatus.ruckusOui import RuckusOui
from selfInstall import apiND
import re
from LoggingFunctions.apiLogger import apiLogger

ciscoFunctions = CiscoWlcFunctions()
apiLogger = apiLogger(__name__)


@tokenRequired
def getAccessPointStatus(mac):
    apiLogger.logInfo(f"attempting a get request on {mac}")
    apVendor = 'Cisco'

    for oui in RuckusOui:
        if re.search(oui, mac, re.IGNORECASE):
            apVendor = 'Ruckus'
            break

    if apVendor == 'Ruckus':
        resp = apiND.getAPStatus(mac)
        resp["response"].update({'vendor': apVendor})
        return resp

    elif apVendor == 'Cisco':
        resp = ciscoFunctions.findCiscoAccessPoint(mac)
        resp["response"].update({'vendor': apVendor})
        return resp
