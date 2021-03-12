from selfInstall.api.auth.decorators import tokenRequired
import re
from selfInstall.api.apStatus import ruckusOui
from selfInstall import apiND

@tokenRequired
def work(mac):
    apVendor = 'Cisco'
    for oui in ruckusOui:
        if re.search(mac, oui, re.IGNORECASE):
            apVendor = 'Ruckus'
            break
    if apVendor == 'Ruckus':
        resp = apiND.getAPStatus(mac)
    
    return mac
