from selfInstall.api.auth.decorators import tokenRequired
import re
from selfInstall.CiscoFunctions.CiscoWlcFunctions import CiscoWlcFunctions
# from selfInstall.api.apStatus import ruckusOui
# from selfInstall import apiND

ciscoFunctions = CiscoWlcFunctions()


@tokenRequired
def work(mac):
    
    returnDict = ciscoFunctions.findCiscoAccessPoint('00:fc:ba:6a:b0:f0')
    return returnDict
