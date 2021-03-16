from selfInstall.api.auth.decorators import tokenRequired
import re
from CiscoFunctions.CiscoWlcFunctions import CiscoWlcFunctions
# from selfInstall.api.apStatus import ruckusOui
# from selfInstall import apiND

ciscoFunctions = CiscoWlcFunctions()


@tokenRequired
def work(mac):
    
    returnDict = ciscoFunctions.findCiscoAccessPoint(mac)
    return returnDict
