from pathlib import Path
from CiscoFunctions.CiscoAuth import ciscoUserName, ciscopw
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import json
from http import HTTPStatus
from LoggingFunctions.apiLogger import apiLogger
apiLogger = apiLogger(__name__)

currentDir = Path().cwd() / 'CiscoFunctions'
jsonFile = currentDir / 'ControllersAndMarkets.json'
with open(jsonFile) as file:
    dictOfControllerFromFile = json.load(file)


def standardReturn(statusCode=None, statusText=None, response=None, *args):
    returnDict = {
        'status_code': statusCode,
        'status_text': statusText,
        'response': response
    }
    if args:
        returnDict.update({'additionalDetails': args})
        return returnDict
    return returnDict


class CiscoWlcFunctions():

    def __init__(self):
        self.dictOfControllers = dictOfControllerFromFile

    def controllerLogin(self, ip):
        apiLogger.logInfo(f"SSH attempt to vWLC {ip}")
        connectObj = ConnectHandler(ip=ip,
                                    port='22',
                                    username=ciscoUserName,
                                    password=ciscopw,
                                    device_type='cisco_wlc_ssh')
        return connectObj

    # used for multithread functions.
    # function to get all Access Points from one controller
    def getAllAccessPointsFromSingleController(self, wlcIp):
        # str[start:end:step]
        # defaultName=apMac.replace(':','')
        # first4=defaultName[0:4]
        # middle4=defaultName[4:8]
        # last4=defaultName[8:12]
        # defaultName=f"AP{first4}.{middle4}.{last4}"
        apInfoDict = dict()
        # pprint.pprint(f'atempting to connect to {wlcIp}')
        try:
            # login sends 'config paging disbaled' after logging in
            netmikoConnectObj = self.controllerLogin(wlcIp)
        except NetMikoTimeoutException:
            apiLogger.logError(f'TCP connection to device at ip: {wlcIp} failed')
            return standardReturn(statusCode=HTTPStatus.SERVICE_UNAVAILABLE,
                                  statusText=f'TCP connection to device at ip: {wlcIp} failed')

        except SSHException as err:
            apiLogger.logError(f'Failed SSH Attempt on device at ip: {wlcIp} failed')
            return standardReturn(statusCode=HTTPStatus.SERVICE_UNAVAILABLE, statusText=str(err))

        except AuthenticationException as err:
            apiLogger.logError(f'failed Authentication Attempt on device at ip: {wlcIp} failed')
            return standardReturn(statusCode=HTTPStatus.SERVICE_UNAVAILABLE, statusText=str(err))
        apiLogger.logInfo(f"logged onto vWLC {wlcIp}")
        # command to get the information about all Access Points currently connected to the WLC
        command = 'show ap summary'
        # get the hostname from the netmiko obj
        # (chrcnctraw-vwlc-m1-n1) >
        # pprint.pprint(f'getting hostname from {wlcIp}')
        hostname = netmikoConnectObj.find_prompt()
        # strip off the unnecessary characters
        hostname = hostname[1:-3]
        # send it
        allAccessPoints = netmikoConnectObj.send_command(command, use_textfsm=True)
        apiLogger.logInfo(f'ran {command} on {hostname}:{wlcIp} number of APs = {len(allAccessPoints)}')
        # disconnect sends 'config paging enable' before 'logout' command
        # pprint.pprint(netmikoConnectObj.is_alive())
        netmikoConnectObj.disconnect()
        apiLogger.logInfo(f"disconnected from {hostname}:{wlcIp}")
        for accessPoint in allAccessPoints:
            # if the accessPoint obj is a str, that means that there were no Access Points on the WLC
            if isinstance(accessPoint, str):
                continue
            # loop throught the Access Points and update our dict with the dat
            # make the key the AP MAC
            apInfoDict.update({accessPoint['mac']: {}})
            apInfoDict[accessPoint['mac']].update({'apName': accessPoint['ap_name']})
            apInfoDict[accessPoint['mac']].update({'apModel': accessPoint['ap_model']})
            apInfoDict[accessPoint['mac']].update({'ip': accessPoint['ip']})
            apInfoDict[accessPoint['mac']].update({'controller': hostname})
            apInfoDict[accessPoint['mac']].update({'controllerIp': wlcIp})

        '''
        adding the code below to the find function, This command has to be ran once per AP
        extremly long to run on every single ap, some controllers have 1800+ aps,
        testing on 1800  took about 25 min to gather all the info from show ap config general on all access points
        command='show ap config general'
        for apName,apinfo in apInfoDict.items():
            command=f'show ap config general {apName}'
            apConfig=netmikoConnectObj.send_command(command, use_textfsm=True)
            apInfoDict[apName].update({'operation_state':apConfig[0]['operation_state']})
            apInfoDict[apName].update({'gateway':apConfig[0]['gateway']})
            apInfoDict[apName].update({'netmask':apConfig[0]['netmask']})
            apInfoDict[apName].update({'uptime':apConfig[0]['uptime']})
        '''
        # return a DataFrame containing all the info about every single Access Point on a single controller
        # create a Dataframe from the dict
        dfToReturn = pd.DataFrame.from_dict(apInfoDict, orient='index')
        # add a title to the index
        dfToReturn.index.name = 'mac'
        # remove the index of AP's mac's and turn it into a column
        dfToReturn.reset_index(inplace=True)
        apiLogger.logInfo(f'got all Access Points from {hostname}: {wlcIp}')
        return dfToReturn

    # this function is used to get the general config of a accessPoint. requires a WLC IP and AP NAME
    def getApConfigGeneral(self, wlcIp, apName):
        try:
            # login sends 'config paging disbaled' after logging in
            netmikoConnectObj = self.controllerLogin(wlcIp)
        except NetMikoTimeoutException:
            apiLogger.logError(f'TCP connection to device at ip: {wlcIp} failed')
            return standardReturn(statusCode=HTTPStatus.SERVICE_UNAVAILABLE,
                                  statusText=f'TCP connection to device at ip: {wlcIp} failed')

        except SSHException as err:
            apiLogger.logError(f'Failed SSH Attempt on device at ip: {wlcIp} failed')
            return standardReturn(statusCode=HTTPStatus.SERVICE_UNAVAILABLE, statusText=str(err))

        except AuthenticationException as err:
            apiLogger.logError(f'failed Authentication Attempt on device at ip: {wlcIp} failed')
            return standardReturn(statusCode=HTTPStatus.SERVICE_UNAVAILABLE, statusText=str(err))
        apiLogger.logInfo(f"logged onto vWLC {wlcIp}")
        command = f'show ap config general {apName}'
        apConfigGeneral = netmikoConnectObj.send_command(command, use_textfsm=True)
        apiLogger.logInfo(f'ran {command} on {wlcIp}')
        netmikoConnectObj.disconnect()
        apiLogger.logInfo(f"disconnected from vWLC {wlcIp}")
        return apConfigGeneral
    '''
    example of show ap config general:
    administrative_state': 'ADMIN_ENABLED',
    'ap_group': 'default-group',
    'country': 'United States',
    'country_code': 'US',
    'flexconnect_vlan_mode': 'Disabled',
    'gateway': '22.188.229.129',
    'identifier': '1581',
    'image': 'C1550-K9W8-M',
    'ip': '22.188.229.201',
    'join_date_time': 'Wed Feb 17 22:10:32 2021',
    'join_taken_time': '0 days, 00 h 00 m 10 s',
    'lwapp_uptime': '11 days, 20 h 26 m 45 s',
    'mac': 'dc:a5:f4:b9:10:9c',
    'mode': 'FlexConnect',
    'model': 'AIR-CAP1552C-A-K9',
    'name': 'PUBL-5100035A58W-TAMP',
    'netmask': '255.255.255.128',
    'operation_state': 'REGISTERED',
    'primary_switch_ip': '71.46.57.247',
    'primary_switch_name': 'TAMP20-WLC8510-1',
    'secondary_switch_ip': 'Not Configured',
    'secondary_switch_name': '',
    'serial_number': 'FTX1749P0AB',
    'tertiary_switch_ip': 'Not Configured',
    'tertiary_switch_name': '',
    'uptime': '101 days, 11 h 32 m 06 s',
    'version': '15.3(3)JF10$'}]
    '''
    def getAllAccessPoints(self):
        # every we run this function ensure these are list empty and updated at the start of the function
        wlcIpList = list()
        for hostName, ip in self.dictOfControllers.items():
            wlcIpList.append(ip["ipAddress"])

        # multithread the function to get an AP from a single controller, on all controllers at once.
        with ThreadPoolExecutor(max_workers=len(self.dictOfControllers)) as executor:
            # make a list of DataFrames containing all the info about all the Access Points from every single controller
            returnedObjects = executor.map(self.getAllAccessPointsFromSingleController, wlcIpList)
        listOfDataFrames = list()
        for obj in returnedObjects:
            if isinstance(obj, dict):
                if obj['status_code']:
                    if obj['status_code'] == HTTPStatus.SERVICE_UNAVAILABLE:
                        apiLogger.logError('failed: could not get all Access Points from one or more vWLCs')
                        continue
            # need to handle other exections here
            if isinstance(obj, pd.DataFrame):
                # open everysingle DataFrame and dump the info into one single DataFrame and return it
                listOfDataFrames.append(obj)
        try:
            return pd.concat(listOfDataFrames, ignore_index=True)
        except ValueError:
            apiLogger.logCritical('failed: no access points retrieved')
            returnDict = {'mac': None,
                          'Model': None,
                          'Name': None,
                          'ip': None,
                          'configState': None,
                          'connectionState': 'Disconnect'
                          }
            return returnDict

    def findCiscoAccessPoint(self, apMac):
        # get all Aps from Funtion getAllAccessPoints
        allAccessPointDf = self.getAllAccessPoints()
        if isinstance(allAccessPointDf, dict):
            return standardReturn(statusCode=HTTPStatus.SERVICE_UNAVAILABLE,
                                  statusText='SYSTEM_EXCEPTION',
                                  response=allAccessPointDf)
        try:
            # find the Ap
            # this will return an empty Data Frame if no mac is found
            dfForReturn = allAccessPointDf.loc[allAccessPointDf['mac'] == apMac]
            apiLogger.logInfo(f"Found requested Access Point {apMac}")
        except IndexError as err:
            returnDict = {'mac': None,
                          'Model': None,
                          'Name': None,
                          'ip': None,
                          'configState': None,
                          'connectionState': 'Disconnect'
                          }
            apiLogger.logInfo(f"unable to find requested Access Point {apMac}. error: {err}")
            return standardReturn(statusCode=HTTPStatus.OK,
                                  statusText='NOT_ON_CONTROLLER',
                                  response=returnDict)
        try:
            # the loc function returns a key error if unable to find a controller ip
            controllerIp = dfForReturn.iloc[0]['controllerIp']
        except KeyError as err:
            apiLogger.logInfo(f"unable to find requested Access Point {apMac}. error: {err}")
            returnDict = {'mac': apMac,
                          'Model': None,
                          'Name': None,
                          'ip': None,
                          'configState': None,
                          'connectionState': 'Disconnect'
                          }
            return standardReturn(statusCode=HTTPStatus.SERVICE_UNAVAILABLE,
                                  statusText='CONTROLLER_FAILURE', response=returnDict)

        apName = dfForReturn.iloc[0]['apName']
        apConfigGeneral = self.getApConfigGeneral(controllerIp, apName)

        if apConfigGeneral['status_code']:
            returnDict = {'mac': dfForReturn.iloc[0]['mac'],
                          'Model': dfForReturn.iloc[0]['apModel'],
                          'Name': apName,
                          'ip': dfForReturn.iloc[0]['ip'],
                          'configState': None,
                          'connectionState': 'Disconnect'
                          }
            apiLogger.logInfo(f"unable to find requested Access Point {apMac} Status.")
            return standardReturn(statusCode=HTTPStatus.SERVICE_UNAVAILABLE,
                                  statusText='CONTROLLER_FAILURE', response=returnDict)

        # return dfForReturn.to_dict(orient='index')
        # return a usable dict object
        returnDict = {'mac': dfForReturn.iloc[0]['mac'],
                      'Model': dfForReturn.iloc[0]['apModel'],
                      'Name': apName,
                      'ip': dfForReturn.iloc[0]['ip'],
                      'configState': apConfigGeneral[0]['operation_state'],
                      'connectionState': 'Connect'
                      }
        apiLogger.logInfo(f"Found Requested Access Point {apMac}")
        return standardReturn(statusCode=HTTPStatus.OK, statusText='FOUND_ON_CONTROLLER', response=returnDict)
