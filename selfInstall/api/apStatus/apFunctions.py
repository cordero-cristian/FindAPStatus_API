from selfInstall.api.auth.decorators import tokenRequired
from CiscoFunctions.CiscoWlcFunctions import CiscoWlcFunctions
from selfInstall.api.apStatus import ruckusOui
from selfInstall import apiND
import re

ciscoFunctions = CiscoWlcFunctions()


@tokenRequired
def getAccessPointStatus(mac):

    apVendor = 'Cisco'

    for oui in ruckusOui:
        if re.search(mac, oui, re.IGNORECASE):
            apVendor = 'Ruckus'
            break

    if apVendor == 'Ruckus':
        resp = apiND.getAPStatus(mac)
        return resp

    elif apVendor == 'Cisco':
        resp = ciscoFunctions.findCiscoAccessPoint(mac)
        return resp
