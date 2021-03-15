#!/usr/local/bin/python3.9

#Exclusive Property of Charter Communications
#Written by Stu Osborne


# to use this class
# assure CSV with RND info in same folder

# code example:
# import sdkRND_API
# objND = sdkRND.clsSdkRndAPI()
# resp = objND.rndInitSessions()

__version__ = 1.0

from http import HTTPStatus
import os,sys
import requests
import json
import csv
import urllib3
import time
import csv
import re
import sdkSCG
import datetime

requests.adapters.DEFAULT_RETRIES = 5

import multiprocessing

try:
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
	pass

try:
	urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
except:
	pass

try:
	urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
except:
	pass
	
import apiRuckusAuth_API


class clsSdkRndAPI:

	def __init__(self):
		
		self.myname = "clsSdkRndAPI"
		self.__version__ = '1.0'
		self.__author__ = 'Charter Communications, Inc.'
		
		print('{strS} / {strV} / {strC}'.format(strS=self.myname,strV=self.__version__,strC=self.__author__))
		
		self.origMultiProcessName = multiprocessing.current_process().name
		
	dctRNDSessions = dict()
	dctRNDTokens = dict()
	dctVSZTokens = dict()
	dctVSZSessions = dict()
	dctVSZLicenseTotals = dict()
	
	dir_path = os.path.dirname(os.path.realpath(__file__))
		
	regexIP = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
	regexSubnet = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}$'
	regexMAC = '([0-9A-Fa-f]{2}([:-])?){5}([0-9A-Fa-f]{2})'
	regexMACAPI = '([0-9A-Fa-f]{2}(:)){5}([0-9A-Fa-f]{2})'
	strInitDateStamp = datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
	regexValidSerial = '\d{12}'
	regexBadRNDResponse = "(authenticate)|(the page you are looking for)"
	vszCsvFiles = list()
	rndCsvFiles = list()
	
	#load the scg library
	clsSCG = sdkSCG.clsSdkSCG()
	
	def getProcessName(self):
		return multiprocessing.current_process().name
	
	#define the csv file finder function
	def find_csv_filenames(self,path_to_dir,suffix='.csv',contains=''):
		filenames = os.listdir(path_to_dir)
		return [ path_to_dir+'/'+filename for filename in filenames if filename.lower().endswith( suffix.lower() ) and contains.lower() in filename.lower() ]

	def	apiNetworkDirectorLogin(self, strRNDName, controllerip, apiVersion, username, password, session = None, iTimeOut = 60):
	
		#the raw call
	
		dctReturn = dict()
	
		if type(session) != type(requests.Session()):
			session=requests.Session()
			
		if not strRNDName or not isinstance(strRNDName,str):
			raise Exception ("strRNDName must be string")
		
		strRNDName = strRNDName.strip().upper()
				
		strBaseUrl = 'https://{controller_ip}/api/{apiVersion}'.format(controller_ip=controllerip,apiVersion=apiVersion)
		strURL = strBaseUrl + '/login'
		
		try:
			r1 = session.post(strURL,json={"username":username,"password":password},verify=False,timeout=iTimeOut)
		except Exception as err:
			strText = str(err)
			r1 = None
			
		dctLine = self.responseConvert(r1)
		dctLine.update({'strBaseUrl':strBaseUrl})
		dctLine.update({'iTimeOut':iTimeOut})
		dctLine.update({'rnd':strRNDName})
		dctLine.update({'session':session})
			
		dctReturn = {strRNDName:dctLine}
		
		return dctReturn
		
		
	def responseConvert(self,r1):
	
		dctReturn=dict()
		
		try:
			dctReturn.update({'rawResponse':r1})
		except:
			dctReturn.update({'rawResponse':None})
			
		try:
			dctReturn.update({'status_code':r1.status_code})
		except:
			dctReturn.update({'status_code':0})
			
		try:
			dctReturn.update({'status_text':r1.text})
		except:
			dctReturn.update({'status_text':None})
			
		try:
			dctReturn.update({'cookies':r1.cookies})
		except:
			dctReturn.update({'cookies':None})
			
		try:
			response = json.loads(r1.content.decode())
			dctReturn.update({'response':response})
		except:
			dctReturn.update({'response':None})
			
		try:
			token = response['token']
		except:
			token = None
				
		dctReturn.update({'token':token})
			
		return dctReturn
		
	
	def getURL(self,dctInfo):
		
			dctReturn = dict()
			iTimeOut = dctInfo.get('iTimeOut',300)
			strRND = dctInfo.get('strRND',None)
			strURL = dctInfo.get('strURL')
			strURL = strURL.replace('[[','{')
			strURL = strURL.replace(']]','}')

			hasMore = True
			
			dctRNDToken = self.getRNDToken(strRND)
			
			if not dctRNDToken:
				rndMainToken = self.getRNDToken(strRND,self.origMultiProcessName)
				
				if not rndMainToken:
					raise Exception('no rndMainToken Found!')
				
				rndMainToken.update({'session':requests.Session()})
				
				dctRNDToken = self.updateRNDToken(strRND,rndMainToken)
				#dctRNDToken = self.updateRNDToken(strRND)
				
				#print('dctToken updated')
			
			strPage = dctInfo.get('strPage','0')

			iPage = int(strPage)
			if not iPage:
				iPage = 1
				
			dctPayload = dctInfo.get('payload',dict())
			
			lstReturnList = list()
				
			while hasMore:
			
				#grab the RND session variable in case it was updated
				dctRNDSession = self.dctRNDSessions[strRND]
				
				strBaseURL = strURL.format(controller_ip=dctRNDSession['strRNDIP'],apiVersion=dctRNDSession['apiVersion'])
				
				dctRNDToken = self.getRNDToken(strRND)

				strCookies = dctRNDToken['cookies']
				
				strToken = dctRNDToken['token']
				
				dctPayload.update({'token':strToken})
				
				strMode = dctInfo.get('mode','get')
				if strMode not in ['get','put','post','delete']:
					raise Exception(strMode)
					
				#to do add page functionality when hasmore = true
				if re.search('\~\~startIndex\~\~',strBaseURL,re.IGNORECASE):
					strExecUrl = strBaseURL.replace('~~startIndex~~',str(iPage))
				else:
					strExecUrl = strBaseURL
					
				#print(strExecUrl)
				
				if __name__ != 'sdkRND_API':
					print (__name__)
					raise Exception(__name__)
					
				sessRND = dctRNDToken['session']
				
				if iPage > 1:
				
					strMsg = '{strR} page {strP}'.format(strP = iPage, strR = strRND)
					print(strMsg)
	
				try:
				
					if strMode == 'get':
						sessResponse = sessRND.get(strExecUrl,cookies=strCookies,json={'token':dctRNDToken['token']},verify=False,timeout=iTimeOut,params=dctPayload) 
						
					elif strMode == 'delete':
						sessResponse = sessRND.delete(strExecUrl,cookies=strCookies,json={'token':dctRNDToken['token']},verify=False,timeout=iTimeOut,params=dctPayload) 
						
					elif strMode == 'put':
						sessResponse = sessRND.put(strExecUrl,cookies=strCookies,verify=False,timeout=iTimeOut,json=dctPayload)
						
					elif strMode == 'post':
						sessResponse = sessRND.post(strExecUrl,cookies=strCookies,json=dctPayload,verify=False,timeout=iTimeOut) 
						
					else:
						raise Exception(strMode)
						
				except requests.exceptions.ReadTimeout as err:
					print ("Recovering from read timeout")
					continue
					
					raise Exception ('requests.exceptions.ReadTimeout')

				except requests.exceptions.ConnectionError as err:  #requests.exceptions.ConnectionError: None: Max retries exceeded with url
					raise Exception ('fix connectionerror handling')
					
				try:
					dctReturn.update({'status_code':sessResponse.status_code})
					
				except:
					dctReturn.update({'status_code':0})
					
				
				status_text = 'ERROR' #init
				
				try:
					status_text = sessResponse.text
					
				except:
				
					pass
									
				dctReturn.update({'status_text':status_text})
				
				if not re.search('AP Not Found',status_text,re.IGNORECASE) and not re.search('hasMore',status_text,re.IGNORECASE) and not re.search('true',status_text,re.IGNORECASE) and not re.search('ZONE',status_text,re.IGNORECASE) and not re.search('cluster',status_text,re.IGNORECASE) and not re.search("iprangetype",status_text) and not re.search("zoneId",status_text) and not re.search('clusterId',status_text)  and not re.search('numberofunprovisionaps',status_text):
					print (status_text)
					
				if not dctReturn['status_code']:
					continue
				
				if re.search(self.regexBadRNDResponse,sessResponse.text,re.IGNORECASE):
				
					if not re.search('(authenticate)',sessResponse.text,re.IGNORECASE):
						time.sleep(3)
						
					print('follow-up login attempt')
					
					#to do : check to see if vsz session objects are wiped out, we don't want that
					resp = self.rndInitSessions()
					continue
				

				response = json.loads(sessResponse.content.decode())
				
				#check multiprocessing mode first
				hasMore = response.get('hasMore',False)
				if hasMore:
					iPage += 1
						
				lstList = response.get('list',list())
				
				if lstList:
					lstReturnList.extend(lstList)
				
			if lstReturnList:
				response.update({'list':lstReturnList})

			dctReturn.update({'response':response})
			
			return dctReturn

	def apiRNDGetAPs(self, strRNDName = 'ALL', strSearch = None):
	
		# function to retrieve AP list !! PLEASE NOTE: The API call only allows to retrieve 100 APs at a time!!
		#try:
		
			dctReturn = dict()
		
			strRNDName = strRNDName.strip().upper()
		
			if not self.dctRNDSessions:
				resp = self.rndInitSessions()
				if isinstance(resp,Exception):
					raise Exception(str(resp))
			
			lstRNDs = list()
			
			for (strRnd,objRND) in self.dctRNDSessions.items():
				if strRNDName == 'ALL':
					lstRNDs.append(strRnd)
				elif strRNDName == 'PRIMARY':
					if objRND['bPrimaryRND']:
						lstRNDs.append(strRnd)
				elif strRNDName == strRnd:
					lstRNDs.append(strRnd)
					break
					
			if not lstRNDs:
				strMsg = "NO RNDs Matched Parameter {strR}".format(strR=strRNDName)
				raise Exception(strMsg)
			
			for strRND in lstRNDs:
			
				strMsg = 'Retrieving AP List from {strR}'.format(strR=strRND)
				#print(strMsg)
			
				baseURL = 'https://[[controller_ip]]/api/[[apiVersion]]/aps?startindex=~~startIndex~~&numberofrows=100&sortby=apserial&sortorder=1'
				if strSearch:
					baseURL += '&search={strSearch}'.format(strSearch=str(strSearch).strip())
					
				strExUrl = baseURL.format(controller_ip='{controller_ip}',apiVersion = '{apiVersion}')
				
				dctGetURL = dict()
				dctGetURL.update({'strURL':strExUrl})
				dctGetURL.update({'strRND':strRND})
				dctGetURL.update({'mode':'get'})
				
				dictGet = self.getURL(dctGetURL)
				dctReturn.update({strRND:dictGet})

			return dctReturn
			
		#except Exception as err:
		#	return err
			
			
	def apiVSZGetAPOpSumm(self,controllerip,port,apiVersion,cookies,session,apmac,iTimeOut=60):
	
		#FIX, MAKE COMMON VSZ QUERY FUNCTION WRAPPER
	
		dctReturn = dict()

		if type(session) != type(requests.Session()):
			session = requests.Session()

		try:

			strVSZURL = "https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/operational/summary"
			r2 = session.get(strVSZURL.format(apMac = apmac,controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(iTimeOut,iTimeOut)) #, params=payload 
			
			status_code = r2.status_code
			status_text = r2.text
			
			if re.search('AP cound not be found',r2.text,re.IGNORECASE):
				response = {}
			else:
				response = json.loads(r2.content.decode())
				
		except urllib3.exceptions.MaxRetryError as maxretryerr:
			status_code = 0
			status_text = 'apiVSZGetAPOpSumm '+str(err)
			response = dict()
				
		except requests.exceptions.ConnectionError as connerr:
			status_code = 0
			status_text = 'apiVSZGetAPOpSumm '+str(err)
			response = dict()
			
		except Exception as err:
			status_code = 0
			status_text = 'apiVSZGetAPOpSumm '+str(err)
			response = dict()
		
		
		dctReturn.update({'status_code':status_code})
		dctReturn.update({'status_text':status_text})
		dctReturn.update({'response':response})
		
		return dctReturn
			
	
	def apiRNDVSZGetAPOpSummary(self,strVSZName,strAPMac):
	
		dctReturn = dict()
	
		if not strVSZName or not isinstance(strVSZName,str):
			raise Exception('apiRNDVSZGetAPOpSummary: Pass vSZ name as as string')
		else:
			strVSZName = strVSZName.strip().lower()
			
		if not strAPMac or not isinstance(strAPMac,str) or not re.search(self.regexMAC,strAPMac):
			raise Exception('apiRNDVSZGetAPOpSummary: Pass AP Mac as string')
		else:
			strAPMac = strAPMac.strip()

		#assure the connection to the cluster is alive
		dctVsz = self.vszLogin(strVSZName)
		
		#get session information if multiprocessing
		dctVSZToken = self.getVSZToken(strVSZName)
		
		strMsg = 'Retrieving AP Operational Summary for {strA} on {strC}'.format(strC=strVSZName,strA=strAPMac)
		#print(strMsg)
		
		#fix, formalize message transport
		
		dctResp = self.apiVSZGetAPOpSumm(dctVSZToken['targetMgt'],dctVsz['api_port'],dctVsz['api_ver'],dctVSZToken['cookies'],dctVSZToken['session'],strAPMac)
		
		dctReturn.update({strVSZName:dctResp})
		
		return dctReturn
		

	def apiRNDGetVSZDetail(self,strVSZName,iTimeOut = 60):
	
		#fix, add ability to specify rnd , primary, etc.
	
		#basic parameter checking
		if not strVSZName or not isinstance(strVSZName,str):
			raise Exception('apiRNDGetVSZDetail: Pass vSZ name as string')
		else:
			strVSZName = strVSZName.strip().lower()
			
		if not iTimeOut or not isinstance(iTimeOut,int):
			raise Exception('apiRNDGetVSZDetail: Pass iTimeOut as int')
			
		#log into RND sessions if not already
		if not self.dctRNDTokens:
			resp = self.rndInitSessions()
			
		bVSZFound  = False #is the vsz managed by any RND in objects
		dctReturn = dict()

		#find this cluster
		for (strRnd,dctRNDSession) in self.dctRNDSessions.items():
		
			cluster = dctRNDSession.get('clusters',dict()).get(strVSZName,dict())
			
			#fix what to do if cluster is empty?
			
			if cluster:
				
				if not cluster.get('strAPIPort',None):
				
					bVSZFound = True
				
					#set up the payload to search for the vsz
					dctGetURL = dict()
					
					strURLGet = 'https://{controller_ip}/api/{apiVersion}/controllers/{strVSZIP}'.format(controller_ip='{controller_ip}',apiVersion='{apiVersion}',strVSZIP = cluster['ip']) 
					
					dctGetURL.update({'strURL':strURLGet})
					dctGetURL.update({'strRND':strRnd})
					dctGetURL.update({'iTimeOut':iTimeOut})
					
					#call the function
					dictGet = self.getURL(dctGetURL)
					
					response = dictGet.get('response',dict())
					
					for (k,v) in response['data'].items():
						cluster.update({k:v})
					
					strVersion = cluster['stats']['systemsummary']['version']
					
					if re.search('^3\.4',strVersion):
						strAPIPort = '7443'
						strAPIVer = 'v4_0'
					elif re.search('^3\.6',strVersion):
						strAPIPort = '7443'
						strAPIVer = 'v6_0'
					elif re.search('^3\.1',strVersion):
						strAPIPort = '7443'
						strAPIVer = 'v3_1'

					cluster.update({'api_port':strAPIPort})
					cluster.update({'api_ver':strAPIVer})				
					cluster.update({'version':strVersion})
					
					self.dctRNDSessions[strRnd]['clusters']['strVSZName'] = cluster
					
					dctReturn.update({strRnd:cluster})
					
				else:
					
					dctReturn.update({strRnd:cluster})
					
					bVSZFound = True
				
						
		if not bVSZFound:
			raise Exception("Invalid controller name")
			
		return dctReturn
		


	def apiNetworkDirectorGetControllers(self,controllerip,apiVersion,cookies,token,session):

		if type(session) != type(requests.Session()):
			session = requests.Session();

		# function to retrieve controllers managed by RND
		r2 = session.get('https://{controller_ip}/api/{apiVersion}/controllers'.format(controller_ip=controllerip,apiVersion=apiVersion),cookies=cookies,json={'token':token},verify=False,timeout=120);  
		if r2.status_code != 200:
			raise Exception("getControllers Exception: "+str(r2.status_code)+' / '+ r2.text);
		response = json.loads(r2.content.decode())
		
		return response['list']
			
			
	def getRNDList(self,strRNDName='-ALL-'):
	
		if not strRNDName or not isinstance(strRNDName,str):
			raise Exception('getRNDList: Pass RND Name, -ALL- or -PRIMARY- as first parameter')
	
		lstRND = list()
			
		for (strRnd,objRND) in self.dctRNDSessions.items():
		
			if strRNDName == '-ALL-':
				lstRND.append(strRnd)
				
			elif strRNDName == '-PRIMARY-' and objRND['bPrimaryRND']:
				lstRND.append(strRnd)
				
			elif strRNDName == strRnd:
				lstRND.append(strRnd)
				break
					
		if not lstRND:
			strMsg = "getRNDList: NO RNDs Matched Parameter {strR}.  Valid entries are -ALL-, -PRIMARY- or RND Name".format(strR=strRNDName)
			raise Exception(strMsg)
			
		return lstRND

	def getVSZToken(self, strVSZName, strProcName = None ):
	
		if not strProcName:
			strProcName = self.getProcessName()
			
		dctVSZTokens = self.dctVSZTokens.get(strVSZName,dict())
			
		dctToken = self.dctVSZTokens.get(strVSZName,dict()).get(strProcName,dict())
		
		if not dctToken and dctVSZTokens:
			for (processName,processToken) in dctVSZTokens.items():
				dctToken = dict()
				for (k,v) in processToken.items():
					if k == 'session':
						v = requests.Session()
					dctToken.update({k:v})
			
				return self.updateVSZToken(strVSZName, dctToken)

				
			
		return dctToken
		
	def updateVSZToken(self, strVSZName, dctLine, strProcName = None):
	
		
		if not strProcName:
			strProcName = self.getProcessName()
			
		dctReturn = dict()
		
		dctLine.update({'processName':strProcName})
		dctLine.update({'vsz':strVSZName})
			
		dctCurrentController = self.dctVSZTokens.get(strVSZName,dict())		
		
		dctCurrentController.update({strProcName:dctLine})
			
		self.dctVSZTokens.update({strVSZName:dctCurrentController})
	
		return dctLine

	def getRNDToken(self, strRNDName , strProcName = None ):
	
		if not strProcName:
			strProcName = self.getProcessName()
			
		dctToken = self.dctRNDTokens.get(strRNDName,dict()).get(strProcName,dict())
			
		return dctToken
		
	def updateRNDToken(self, strRNDName, dctLine, strProcName = None):
	
		if not strProcName:
			strProcName = self.getProcessName()
			
		strRNDName = strRNDName.strip().upper()
		
		#update the process id to the current ID when multiprocessing
		
		dctLine.update({'processName':strProcName})
		dctLine.update({'rnd':strRNDName})
		
		
		dctTempRNDTokens = self.dctRNDTokens.get(strRNDName,dict())
		dctTempRNDTokens.update({strProcName:dctLine})
		
		self.dctRNDTokens.update({strRNDName:dctTempRNDTokens})
			
		return dctLine
		
			
	def rndLogin(self,strRNDName,strRNDIP,apiVersion,username,password,bPrimaryRND=False,iTimeOut=60):
	
		if not strRNDName:
			raise Exception('Must pass RND Name as string')
		else:
			strRNDName = strRNDName.strip().upper()
			
		if not strRNDIP or not isinstance(strRNDIP,str) or not re.search(self.regexIP,strRNDIP):
			raise Exception('rndLogin: Must pass RND IP as ipv4 string')
			
		if not apiVersion or not isinstance(apiVersion,str):
			raise Exception('rndLogin: Must pass RND API Version as string')
			
		if not username or not isinstance(username,str):
			raise Exception('rndLogin: Must pass RND Username as string')
			
		if not password or not isinstance(password,str):
			raise Exception('rndLogin: Must pass RND Password as string')
			
		if not isinstance(bPrimaryRND,bool):
			raise Exception('rndLogin: Must pass bPrimaryRND as bool')
			
		if not iTimeOut or not isinstance(iTimeOut,int):
			raise Exception('rndLogin: Must pass iTimeOut as int')
			
		#get login for this session information
		dctToken = self.getRNDToken(strRNDName)
	
		#init loop variables
		tries = 0
		bSuccess = False
		
		while tries < 6 and not bSuccess:
		
			tries += 1
		
			#create a session object to keep the TCP connections alive between calls
			session = requests.session()
		
			#log onto the controller
			strMsg = 'Try {strTry} logging into RND {strRND} / {strIP}'.format(strTry=str(tries),strRND=strRNDName,strIP=strRNDIP)
			print (strMsg)
			
			#false = return token None = cookies
			dctResponse = self.apiNetworkDirectorLogin(strRNDName,strRNDIP,apiVersion,username,password,session,iTimeOut)

			dctToken = dctResponse[strRNDName]
			
			if dctToken['status_code'] == 401:
				strMsg = 'Login unsuccessful to RND {strRND} / {strIP} {strC} Error: {strErrorMsg} '.format(strRND=strRNDName,strIP=strRNDIP,strErrorMsg=dctToken['status_text'],strC=dctToken['status_code'])
				break
			
			elif dctToken['status_code'] != 200:
			
				print(dctToken)
			
				strMsg = 'Login unsuccessful to RND {strRND} / {strIP} {strC} Error: {strErrorMsg} '.format(strRND=strRNDName,strIP=strRNDIP,strErrorMsg=dctToken['status_text'],strC=dctToken['status_code'])
				
				print(strMsg)
				
				print('Pausing')
				
				time.sleep(2)
				
				continue
			
			else:
			
				self.updateRNDToken(strRNDName,dctToken)
				break
		
		if not dctToken['token']:
			strMsg = 'Login unsuccessful to RND {strRND} / {strIP} Error: {strErrorMsg} '.format(strRND=strRNDName,strIP=strRNDIP,strErrorMsg='Token not returned')
			print(strMsg)
			
		else:
		
			dctLine = self.dctRNDSessions.get(strRNDName,dict())

			
			if not dctLine:
			
				if bPrimaryRND:
					deleteAPvSZ = 'true'
				else:
					deleteAPvSZ = 'false'
			
				dctLine.update({'strRNDIP':strRNDIP})
				dctLine.update({'strRNDName':strRNDName})
				dctLine.update({'apiVersion':apiVersion})
				dctLine.update({'username':username})
				dctLine.update({'password':password})
				dctLine.update({'deleteAPvSZ':deleteAPvSZ})
				dctLine.update({'bPrimaryRND':bPrimaryRND})
				

			#add cluster information if requested 
			if not dctLine.get('clusters',None):
			
				response = self.apiNetworkDirectorGetControllers(strRNDIP,apiVersion,dctToken['cookies'],dctToken['token'],dctToken['session'])
				
				clusterDict = dict()
				clusterByIDRef = dict()
				
				for cluster in response:
					strClusterName = cluster['name'].strip().lower()
					strClusterID = cluster['_id'].strip()
					
					dctZoneNameIDXref = dict()
					dctZoneIDNameXref = dict()
					
					for zone in cluster['zones']:
					
						zoneName = zone['name'].strip()
						zoneID = zone['id'].strip()
						
						dctZoneNameIDXref.update({zoneName:zoneID})
						dctZoneIDNameXref.update({zoneID:zoneName})
						
					cluster.update({'dctZoneNameIDXref':dctZoneNameIDXref})
					cluster.update({'dctZoneIDNameXref':dctZoneIDNameXref})

					clusterDict.update({strClusterName:cluster})
					clusterByIDRef.update({strClusterID:strClusterName})

				dctLine.update({'clusters':clusterDict})
				dctLine.update({'clusterRefByID':clusterByIDRef})
			
			self.dctRNDSessions.update({strRNDName:dctLine})
			
			return dctLine			
			
	def rndInitSessions(self, strFilePattern = 'rnd', strCSVPath = dir_path ):

			if not self.rndCsvFiles:
			
				#find CSV files in the folder with 'networkdirector' in the filename
				csvFiles = self.find_csv_filenames(strCSVPath,'.csv',strFilePattern)
			
				if not csvFiles:
					strMsg = 'No csv files could be found matching file pattern {strFP} in directory {dirpath}'.format(strFP=strFilePattern,dirpath=strCSVPath)
					raise Exception(strMsg)
							
				#init the report
				lstFilteredResults = list()
				
				username = apiRuckusAuth_API.rndUserName
				password = apiRuckusAuth_API.rndPassword

				#loop through the network director csv files, and add rows to the candidate list
				for csvFile in csvFiles:

					#define candidate lists	
					lstReader = list()
					
					strMsg = '\nImporting Ruckus Network Directors from {strCSV}'.format(strCSV=csvFile)
					print (strMsg)
					
					with open(csvFile,'rU') as fh:
						reader = csv.reader(fh)
						lstReader.extend(list(reader))

					#remove non-candidate lines from the input lists.
					for list_row in lstReader:
						if len(list_row)>2 and re.search(self.regexIP,list_row[0]) and list_row[1] and list_row[2] and list_row[3]:
							lstFilteredResults.append(list_row)
						
				iRNDCount = 0 #init

				for lstRow in lstFilteredResults:

					controllerip = lstRow[0] #ip
					# if not re.search(self.regexRNDIPs,controllerip):
						# strNewRegex = '({oldReg})|(addReg)'.format(oldReg = self.regexRNDIPs, addReg = controllerip)
						# self.regexRNDIPs = strNewRegex
					
					controllername = lstRow[1]  #controller filename 
					apiVersion = lstRow[2]	#api version
					strPrimaryRND  = lstRow[3].strip().lower()
					
					controllername = controllername.strip().upper()
					
					# if controllername == 'NDCW':
						# password = 'xxx'
					# else:
						# password = apiRuckusAuth.rndPassword
					
					bPrimaryRND = False
					if re.search('true',strPrimaryRND,re.IGNORECASE):
						bPrimaryRND = True
						
					dctLine = {'controllerip':controllerip, 'username':username, 'password':password, 'controllername':controllername, 'apiVersion':apiVersion, 'bPrimaryRND':bPrimaryRND}
					
					self.rndCsvFiles.append(dctLine)
					
			else:
				iRNDCount = len(self.rndCsvFiles)
			
			for dctRnd in self.rndCsvFiles:
			
				#create a session object to keep the TCP connections alive between calls
				dctRNDSession  = self.rndLogin(dctRnd['controllername'],dctRnd['controllerip'],dctRnd['apiVersion'],dctRnd['username'],dctRnd['password'],dctRnd['bPrimaryRND'])	
				iRNDCount += 1

			if len(self.dctRNDSessions.keys()) == 0:
			
				#remove the stored login/passwords in the class
				self.rndCsvFiles = list()
				
				strMSG = 'NO_RND_SESSIONS'
				raise Exception(strMSG)
				
			if not self.vszCsvFiles:
			
				setClusters = set()
				
				for (strRndx,objRNDx) in self.dctRNDSessions.items():
				
					for strClustername in objRNDx['clusters'].keys():
					
						setClusters.add(strClustername)
						
				if not (setClusters):
					raise Exception('No clusters found in RND system')
						
				for strCluster in setClusters:
					
					vrow = dict()
					
					vrow.update({'controllername':strCluster})
					vrow.update({'username':apiRuckusAuth_API.vszUserName})
					vrow.update({'password':apiRuckusAuth_API.vszPassword})
					
					self.dctVSZSessions.update({strCluster:vrow})
					self.vszCsvFiles.append(vrow)
			
	def vszLogin(self,strVSZName,dctVsz=dict()):
	
		if not strVSZName or not isinstance(strVSZName,str):
			raise Exception('Pass vSZ name as first parameter as string')
		else:
			strVSZName = strVSZName.strip().lower()
			
		if not isinstance(dctVsz,dict):
			raise Exception('Pass dctVsz as dict')
			
		if not dctVsz:
			dctVsz = self.dctVSZSessions.get(strVSZName,dict())
			
		if not dctVsz:
			raise Exception('vSZ data not found in object or passed as parameter')
			
		if not dctVsz['username']:
			sys.exit('no user/password for vsz, pass to vszlogin')
		
			
		if not dctVsz['password']:
			sys.exit('no password for vsz')
			
		#log into RND sessions if not already
		if not self.dctRNDTokens:
			resp = self.rndInitSessions()

		bVSZFound  = False #is the vsz managed by any RND in objects
		dctVSZToken = self.getVSZToken(strVSZName)

		#does a login exist already?
		if not dctVSZToken:
			#print ('no dctVSZToken')
			
			dctVszMain = self.getVSZToken(strVSZName,self.origMultiProcessName)
			
			if dctVszMain:
				#print (dctVszMain)
				raise Exception('unknown error')
				
		#do a small call to see if the system is alive if found in session objects
		#fix: make sure this works
		
		if dctVSZToken.get('targetMgt',None):
		
			bVSZFound = True
			resp = None
			
			try:
			
				#print('getting controller summary for '+strVSZName)

				resp = self.clsSCG.apGetControllerSummary(dctVSZToken['targetMgt'],dctVsz['api_port'],dctVsz['api_ver'],dctVSZToken.get('cookies',None),dctVSZToken['session'])
				
				#print('got controller summary for '+strVSZName)
				
			except Exception as err:
			
				resp = err
			
			#login already established
			if not isinstance(resp,Exception) and resp:
				return dctVsz
		
		#vsz login required
		dctRNDVSZ = dict()
		
		#find this cluster
		for (strRND,rndObj) in self.dctRNDSessions.items():
			cluster = rndObj.get('clusters',dict()).get(strVSZName,dict())
			if cluster and isinstance(cluster,dict):
				bVSZFound = True
				dctRNDVSZ = cluster
				break
						
		if not bVSZFound:
			raise Exception("Invalid controller name")
				
		#get controller info
		dctRndVSZd = self.apiRNDGetVSZDetail(strVSZName)
		
		dctVSZd = dctRndVSZd.get(strRND,dict())
		if not dctVSZd:
			raise Exception('Version and API info not found')

		#init loop variables
		tries = 0
		r1 = None
		bSuccess = False
		
		while tries < 3 and not bSuccess:
		
			tries += 1

			for targetMgt in dctRNDVSZ['managementips']:
			
				dctVSZToken.update({'session':None}) #init
				dctVSZToken.update({'targetMgt':None})
				dctVSZToken.update({'cookies':None})

				#TO DO, STANDARDIZE MESSAGES

				#log in to the controller in question
				strPrintString = 'Attempting Login to vSZ {strV} / {strI}'.format(strV=strVSZName,strI=targetMgt)
				#print(strPrintString)

				logsess = requests.Session()
				
				r1 = self.clsSCG.apiControllerLogin(targetMgt,dctVSZd['api_port'],dctVSZd['api_ver'],dctVsz['username'],dctVsz['password'],logsess)
				
				if re.search("User name or password is invalid",str(r1)):
					raise Exception("User name or password is invalid")
				
				#check for login exceptions and log
				if isinstance(r1, Exception):
					strMsg = 'Login unsuccessful {strC} Error: {strE}'.format(strC=strVSZName,strE=str(r1))
					print(strMsg)
					continue
					
				dctVSZToken.update({'session':logsess})
				dctVSZToken.update({'targetMgt':targetMgt})
				dctVSZToken.update({'cookies':r1.cookies})
				dctVSZToken.update({'vsz':strVSZName})
				
				dctVsz.update({'api_port':dctVSZd['api_port']})
				dctVsz.update({'api_ver':dctVSZd['api_ver']})
				
				self.dctVSZSessions.update({strVSZName:dctVsz})
				
				dct = self.updateVSZToken(strVSZName,dctVSZToken)
								
				#print("logged into controller on ip "+targetMgt)
				bSuccess = True
				break
			
			if bSuccess:
				break

			print('Pausing')
			time.sleep(1)
				
		if not bSuccess:
			raise Exception("Login Error")
			
		#print ('logged in')
		
		return dctVsz
		
	def returnStatus(self,status_code=0,status_text='',response=dict()):
		retDict = dict()
		retDict.update({'status_code':status_code})
		retDict.update({'status_text':status_text})
		retDict.update({'response':response})
		return (retDict)
		
	def getAPStatus(self,strAPMac):
	
		strAPMac = strAPMac.strip().lower()
	
		try:
	
			dctResponse = dict()
			status_code = 0
			status_text = ''
		
			if not re.search(self.regexMACAPI,strAPMac):
				strMsg = 'BAD_MAC_FORMAT'.format(strM=strAPMac,strR=self.regexMACAPI)
				status_code = HTTPStatus.BAD_REQUEST #400
				status_text = strMsg
				return self.returnStatus(status_code,status_text,dict())


			#find the ap mac on ruckus network director
			rndSearchResp = self.apiRNDGetAPs(strRNDName = 'ALL', strSearch = strAPMac)

			bFound = False #init
			strRNDErrors = 0 #init
			strRNDController = None #init

			for (strRND,dctPayload) in rndSearchResp.items():

				if dctPayload['status_code'] != 200:
					strRNDErrors += 1
					
				apList = dctPayload.get('response',dict()).get('list',list())
				
				for dctListPayload in apList:
				
					if dctListPayload.get('mac','').strip().lower() == strAPMac:
						strRNDController = dctListPayload.get('clustername','').strip().lower()
						if strRNDController:
							bFound = True
							break

			#did all network directors respond to the request?
			if len(self.rndCsvFiles) != len(rndSearchResp):
				strRNDErrors = 1

			if not bFound:
				if not strRNDErrors:
					strMsg = 'NOT_IN_RND'
					status_code = HTTPStatus.UNPROCESSABLE_ENTITY #422
					status_text = strMsg
					return self.returnStatus(status_code,status_text,dict())
					
				else:
					strMsg = 'RND_FAILURE'
					status_code = HTTPStatus.SERVICE_UNAVAILABLE #503
					status_text = strMsg
					return self.returnStatus(status_code,status_text,dict())
					
					#ADD RND LOGIN FAILURE 401 - unauthorized

			try:		
				objVsz = self.vszLogin(strRNDController)
			except Exception as err:
				if str(err) == "User name or password is invalid":
					strMsg = 'VSZ_UNAUTHORIZED'
					status_code = 401
					status_text = strMsg
					return self.returnStatus(status_code,status_text,dict())
				else:
					strMsg = 'VSZ_FAILURE'
					status_code = HTTPStatus.SERVICE_UNAVAILABLE #503
					status_text = strMsg
					return self.returnStatus(status_code,status_text,dict())

			#uncomment to test for not found on vsz
			#strAPMac = '58:93:96:27:C8:33'
			
			try:
				objAPOpSumm = self.apiRNDVSZGetAPOpSummary(strRNDController,strAPMac)
			except:
				strMsg = 'VSZ_FAILURE'
				status_code = HTTPStatus.SERVICE_UNAVAILABLE #503
				status_text = strMsg
				return self.returnStatus(status_code,status_text,dict())
				
			for (vszDum,dctVSZPayload) in objAPOpSumm.items():
				intVSZStatusCode = dctVSZPayload.get('status_code',0)
				strVSZStatusText = dctVSZPayload.get('status_text',0)
				
				if intVSZStatusCode != 200:
					if intVSZStatusCode == 422:
						strMsg = 'NOT_FOUND_ON_VSZ'
						status_code = HTTPStatus.UNPROCESSABLE_ENTITY #422
						status_text = strMsg
					else:
						strMsg = 'VSZ_FAILURE'
						status_code = HTTPStatus.SERVICE_UNAVAILABLE #503
						status_text = strMsg
					return self.returnStatus(status_code,status_text,dict())
					
				dctVSZPayloadResp = dctVSZPayload.get('response',dict())
				
				#remove unneeded payload
				dctVSZPayloadResp.pop('provisionMethod',None)
				dctVSZPayloadResp.pop('externalPort',None)
				dctVSZPayloadResp.pop('dpId',None)
				dctVSZPayloadResp.pop('managementVlan',None)
				dctVSZPayloadResp.pop('latitude',None)
				dctVSZPayloadResp.pop('longitude',None)
				dctVSZPayloadResp.pop('location',None)
				dctVSZPayloadResp.pop('ipType',None)
				dctVSZPayloadResp.pop('provisionMethod',None)
				dctVSZPayloadResp.pop('provisionStage',None)
				dctVSZPayloadResp.pop('cpId',None)
				dctVSZPayloadResp.pop('dpId',None)
				dctVSZPayloadResp.pop('managementVlan',None)
				dctVSZPayloadResp.pop('managementVlan',None)
				dctVSZPayloadResp.pop('zoneId',None)
				dctVSZPayloadResp.pop('meshHop',None)
				dctVSZPayloadResp.pop('isCriticalAP',None)
				dctVSZPayloadResp.pop('description',None)
				dctVSZPayloadResp.pop('apGroupId',None)
				dctVSZPayloadResp.pop('meshRole',None)
				dctVSZPayloadResp.pop('countryCode',None)
				dctVSZPayloadResp.pop('administrativeState',None)
				dctVSZPayloadResp.pop('approvedTime',None)
				dctVSZPayloadResp.pop('externalIp',None)
				dctVSZPayloadResp.pop('serial',None)
				dctVSZPayloadResp.pop('clientCount',None)
				dctVSZPayloadResp.pop('uptime',None)
				dctVSZPayloadResp.pop('lastSeenTime',None)
				dctVSZPayloadResp.pop('clientCount',None)
				dctVSZPayloadResp.pop('wifi24Channel',None)
				dctVSZPayloadResp.pop('wifi50Channel',None)
				dctVSZPayloadResp.pop('version',None)
				dctVSZPayloadResp.pop('registrationState',None)
				
				
				return self.returnStatus(HTTPStatus.OK,'FOUND_ON_VSZ',dctVSZPayloadResp) #200
				
				
		except Exception as err:
			strMsg = str(err)
			status_code = HTTPStatus.SERVICE_UNAVAILABLE
			status_text = strMsg
			return self.returnStatus(status_code,status_text,dict())
						