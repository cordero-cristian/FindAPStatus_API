from selfInstall.api.auth.decorators import tokenRequired
from CiscoFunctions.CiscoWlcFunctions import CiscoWlcFunctions
# from selfInstall.api.apStatus import ruckusOui
# from selfInstall import apiND

ciscoFunctions = CiscoWlcFunctions()


@tokenRequired
def work(mac):

    apVendor = 'Cisco'
#    for oui in RuckusOui:
#        if re.search(oui, mac, re.IGNORECASE):
#            apVendor = 'Ruckus'
#            break
#    if apVendor == 'Ruckus':
#        resp = apiND.getAPStatus(mac)
#        return resp
    resp = ciscoFunctions.findCiscoAccessPoint(mac)
    return resp
