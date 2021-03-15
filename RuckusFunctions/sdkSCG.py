#!/usr/bin/python
#Unnati Mhatre, 09/2017
#Stu Osborne 12/2017

#Last Updated:12/20/2017


import requests
import json
import csv
import sys

requests.adapters.DEFAULT_RETRIES = 5


import urllib3
try:
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
	print ('');

try:
	urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
except:
	print ('');


try:
	urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
except:
	print ('');



payload = {'listSize': 40000 }  

class clsSdkSCG:

	def __init__(self):
		self.myname = "clsSdkSCG"

	def apiQueryAPs(self, controllerip, port, apiVersion, cookies, session, dctFilters=dict()):
	
		if type(session) != type(requests.Session()):
			session = requests.Session()
			
		try:
			strURL = 'https://{controller_ip}:{port}/api/public/{apiVersion}/query/ap'
			r2 = session.post((strURL).format(controller_ip=controllerip, port=port, apiVersion=apiVersion), cookies=cookies, verify=False, timeout=(10,600), params=payload, json=dctFilters)
			if r2.status_code != 200:
				raise Exception('apiQueryAPs Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response['list']
			
		except Exception as err:
			return err

	def apiGetAccountingProfiles(self, controllerip, port, apiVersion, cookies, session):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			r2 = session.get(('https://{controller_ip}:{port}/api/public/{apiVersion}/profiles/acct').format(controller_ip=controllerip, port=port, apiVersion=apiVersion), cookies=cookies, verify=False, timeout=(10,600), params=payload)
			if r2.status_code != 200:
				raise Exception('apiGetAccountingProfiles Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response['list']
		except Exception as err:
			return err

	def apiGetAccountingProfile(self, controllerip, port, apiVersion, cookies, session, id):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			r2 = session.get(('https://{controller_ip}:{port}/api/public/{apiVersion}/profiles/acct/{id}').format(controller_ip=controllerip, port=port, apiVersion=apiVersion, id=id), cookies=cookies, verify=False, timeout=(10,600), params=payload)
			if r2.status_code != 200:
				raise Exception('apiGetAccountingProfile Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response
		except Exception as err:
			return err

	def apiGetAuthProfiles(self, controllerip, port, apiVersion, cookies, session):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			r2 = session.get(('https://{controller_ip}:{port}/api/public/{apiVersion}/profiles/auth').format(controller_ip=controllerip, port=port, apiVersion=apiVersion), cookies=cookies, verify=False, timeout=(10,600), params=payload)
			if r2.status_code != 200:
				raise Exception('apiGetAuthProfiles Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response['list']
		except Exception as err:
			return err

	def apiGetAuthProfile(self, controllerip, port, apiVersion, cookies, session, id):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			r2 = session.get(('https://{controller_ip}:{port}/api/public/{apiVersion}/profiles/auth/{id}').format(controller_ip=controllerip, port=port, apiVersion=apiVersion, id=id), cookies=cookies, verify=False, timeout=(10,600), params=payload)
			if r2.status_code != 200:
				raise Exception('apiGetAuthProfile Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response
		except Exception as err:
			return err

	def apiGetAuthRadiusProfiles(self, controllerip, port, apiVersion, cookies, session):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			r2 = session.get(('https://{controller_ip}:{port}/api/public/{apiVersion}/services/auth/radius').format(controller_ip=controllerip, port=port, apiVersion=apiVersion), cookies=cookies, verify=False, timeout=(10,600), params=payload)
			if r2.status_code != 200:
				raise Exception('apiGetAuthRadiusProfiles Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response['list']
		except Exception as err:
			return err

	def apiGetAuthRadiusProfile(self, controllerip, port, apiVersion, cookies, session, id):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			r2 = session.get(('https://{controller_ip}:{port}/api/public/{apiVersion}/services/auth/radius/{id}').format(controller_ip=controllerip, port=port, apiVersion=apiVersion, id=id), cookies=cookies, verify=False, timeout=(10,600), params=payload)
			if r2.status_code != 200:
				raise Exception('apiGetAuthRadiusProfile Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response
		except Exception as err:
			return err

	def apiGetSoftGreProfiles(self, controllerip, port, apiVersion, cookies, session):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			r2 = session.get(('https://{controller_ip}:{port}/api/public/{apiVersion}/profiles/tunnel/softgre').format(controller_ip=controllerip, port=port, apiVersion=apiVersion), cookies=cookies, verify=False, timeout=(10,600), params=payload)
			if r2.status_code != 200:
				raise Exception('apiGetSoftGreProfiles Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response['list']
		except Exception as err:
			return err

	def apiGetSoftGreProfile(self, controllerip, port, apiVersion, cookies, session, id):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			r2 = session.get(('https://{controller_ip}:{port}/api/public/{apiVersion}/profiles/tunnel/softgre/{id}').format(controller_ip=controllerip, port=port, apiVersion=apiVersion, id=id), cookies=cookies, verify=False, timeout=(10,600), params=payload)
			if r2.status_code != 200:
				raise Exception('apiGetSoftGreProfile Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response
		except Exception as err:
			return err

	def apiControllerLogin(self,controllerip,port,apiVersion,username,password,session):

		if type(session) != type(requests.Session()):
			session = requests.Session();

		try:

			r1 = session.post('https://{controller_ip}:{port}/api/public/{apiVersion}/session'.format(controller_ip=controllerip,port=port,apiVersion=apiVersion),json={"username":username,"password":password,"apiVersions" : [ "1", "2" ],"timeZoneUtcOffset" : "+08:00"},verify=False,timeout=60)

			if r1.status_code != 200:
				raise Exception("apiControllerLogin Exception: "+str(r1.status_code)+' / '+ r1.text);

			return r1;  

		except Exception as err:
			return err

	def apiControllerLogoff(self,controllerip,port,apiVersion,cookies,session):

		if type(session) != type(requests.Session()):
			session = requests.Session();


		# function to logoff the controller
		try:

			r1 = session.delete('https://{controller_ip}:{port}/api/public/{apiVersion}/session'.format(controller_ip=controllerip,port=str(port),apiVersion=apiVersion),cookies=cookies,verify=False,timeout=20);

			if r1.status_code != 200:
				raise Exception("apiControllerLogoff Exception: "+str(r1.status_code)+' / '+ r1.text);
	
			del session;
			return r1;  

		except Exception as err:
			return err

	def apGetSysInventory(self,controllerip,port,apiVersion,cookies,session):   

		#function to create a zone id map for the SCG and ascertain the zone of the AP

		if type(session) != type(requests.Session()):
			session = requests.Session();

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/system/inventory".format(controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(10,600), params=payload)   #get the apzone names and corresponding ids
			if r2.status_code != 200:
				raise Exception("apGetSysInventory Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode());

			return response['list'];

		except Exception as err:
			return err


	def apGetZoneInfo(self,controllerip,port,apiVersion,cookies,session):   

		#function to create a zone id map for the SCG and ascertain the zone of the AP

		if type(session) != type(requests.Session()):
			session = requests.Session();

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/rkszones".format(controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(10,600), params=payload)   #get the apzone names and corresponding ids
			if r2.status_code != 200:
				raise Exception("apGetZoneInfo Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode());

			return response['list'];

		except Exception as err:
			return err
	
	def apGetControllerSummary(self,controllerip,port,apiVersion,cookies,session):

		#gets information regarding the cluster, including the number of nodes and control plane IPs

		if type(session) != type(requests.Session()):
			session = requests.Session();

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/controller".format(controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(10,600), params=payload)   #get the apzone names and corresponding ids
			if r2.status_code != 200:
				raise Exception("apGetControllerSummary Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode());

			return response['list'];

		except Exception as err:
			return err


	def apGetAPGroups(self,controllerip,port,apiVersion,cookies,zoneId,session): 

		if type(session) != type(requests.Session()):
			session = requests.Session()

		#function to retrieve AP Groups associated with a zone

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/rkszones/{zoneId}/apgroups".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,zoneId=zoneId),cookies=cookies,verify=False,timeout=(10,600), params=payload)   #get the apgroup names and corresponding ids
			if r2.status_code != 200:
				raise Exception("apGetAPGroups Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode());

			return response['list'];

		except Exception as err:
			return err




	def apGetAPGroupDetail(self,controllerip,port,apiVersion,cookies,zoneId,groupID,sessionapGetAPGroupDetail): 

		if type(sessionapGetAPGroupDetail) != type(requests.Session()):
			sessionapGetAPGroupDetail = requests.Session()

		#function to retrieve AP Groups associated with a zone

		try:
			r2 = sessionapGetAPGroupDetail.get("https://{controller_ip}:{port}/api/public/{apiVersion}/rkszones/{zoneId}/apgroups/{groupID}".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,zoneId=zoneId,groupID=groupID),cookies=cookies,verify=False,timeout=(10,600), params=payload)  
			if r2.status_code != 200:
				raise Exception("apGetAPGroupDetail Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode());
	
			return response;

		except Exception as err:
			return err




	def apGetWLANs(self,controllerip,port,apiVersion,cookies,zoneId,session):

		if type(session) != type(requests.Session()):
			session = requests.Session();

		#function to wlan details given zoneid and wlanid

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/rkszones/{zoneId}/wlans".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,zoneId=zoneId),cookies=cookies,verify=False,timeout=(10,600), params=payload)   #get the apgroup names and corresponding ids
			
			if r2.status_code != 200:
				raise Exception("apGetWLANs Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode());
			
			return response['list'];

		except Exception as err:
			return err

		


	def apGetWLANDetail(self,controllerip,port,apiVersion,cookies,zoneId,wlanId,session):

		#function to wlan details given zoneid and wlanid

		if type(session) != type(requests.Session()):
			session = requests.Session();

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/rkszones/{zoneId}/wlans/{wlanId}".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,zoneId=zoneId,wlanId=wlanId),cookies=cookies,verify=False,timeout=(10,600), params=payload)   #get the apgroup names and corresponding ids
			if r2.status_code != 200:
				raise Exception("apGetWLANDetail Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode())

			return response;

		except Exception as err:
			return err

	def apGetZoneDetail(self,controllerip,port,apiVersion,cookies,session,zoneId): 


		if type(session) != type(requests.Session()):
			session = requests.Session();   

		#function to retrieve zone detail

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/rkszones/{zoneId}".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,zoneId=zoneId),cookies=cookies,verify=False,timeout=(10,600), params=payload)   #get the wlan grp names and corresponding ids

			if r2.status_code != 200:
				raise Exception("apGetZoneDetail Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode());

			return response;

		except Exception as err:
			return err
			
	def apZoneModifyAPReboot(self,controllerip,port,apiVersion,cookies,session,zoneId,body): 


		if type(session) != type(requests.Session()):
			session = requests.Session();   

		#function to update ap reboot timeout

		try:
			r2 = session.patch("https://{controller_ip}:{port}/api/public/{apiVersion}/rkszones/{zoneId}/apRebootTimeout".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,zoneId=zoneId),cookies=cookies,verify=False,timeout=(10,600), params=payload, json = body)   #get the wlan grp names and corresponding ids

			if r2.status_code not in [200,204]:
				raise Exception("apZoneModifyAPReboot Exception: "+str(r2.status_code)+' / '+ r2.text);

			return r2;

		except Exception as err:
			return err


	def apGetWLANGroups(self,controllerip,port,apiVersion,cookies,zoneId,session): 


		if type(session) != type(requests.Session()):
			session = requests.Session();   

		#function to retrieve wlan groups associated to a zone

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/rkszones/{zoneId}/wlangroups".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,zoneId=zoneId),cookies=cookies,verify=False,timeout=(10,600), params=payload)   #get the wlan grp names and corresponding ids
			if r2.status_code != 200:
				raise Exception("apGetWLANGroups Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode());

			return response['list'];

		except Exception as err:
			return err

	def apGetAPQuery(self, controllerip, port, apiVersion, cookies, session, payload2={}):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			strURL = 'https://{controller_ip}:{port}/api/public/{apiVersion}/query/ap'
			r2 = session.get((strURL).format(controller_ip=controllerip, port=port, apiVersion=apiVersion), cookies=cookies, verify=False, timeout=(10,1200), params=payload, json=payload2)
			if r2.status_code != 200:
				raise Exception('apGetAPQuery Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			response = json.loads(r2.content.decode())
			return response['list']
		except Exception as err:
			return err
			
	def apGetAPList(self,controllerip,port,apiVersion,cookies,session): 

		if type(session) != type(requests.Session()):
			session = requests.Session();  

		#function to retrieve list of APs from controller:

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/aps".format(controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(10,1200), params=payload)   #get the ap list from the controller
			if r2.status_code != 200:
				raise Exception("apGetAPList Exception: "+str(r2.status_code)+' / '+ r2.text);

			response = json.loads(r2.content.decode());

			return response['list'];

		except Exception as err:
			return err	
			
	def apCreateAP(self,controllerip,port,apiVersion,cookies,session,payload2): 

		if type(session) != type(requests.Session()):
			session = requests.Session()

		try:
			r2 = session.post("https://{controller_ip}:{port}/api/public/{apiVersion}/aps".format(controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(10,120),params=payload,json=payload2); 
			if r2.status_code != 201:
				raise Exception("apCreateAP Exception: "+str(r2.status_code)+' / '+r2.text);

			#response = json.loads(r2.content.decode());

			return True;

		except Exception as err:
			return err
			
	def apDisableLocationOverride(self, controllerip, port, apiVersion, cookies, session, apmac, additional=True):
		if type(session) != type(requests.Session()):
			session = requests.Session()
		try:
			r2 = session.delete(('https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/location').format(controller_ip=controllerip, port=port, apiVersion=apiVersion, apMac=apmac), cookies=cookies, verify=False, timeout=60, params=payload)
			if r2.status_code != 204:
				raise Exception('apUpdateAP Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			if additional:
				r2 = session.delete(('https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/locationAdditionalInfo').format(controller_ip=controllerip, port=port, apiVersion=apiVersion, apMac=apmac), cookies=cookies, verify=False, timeout=60, params=payload)
				if r2.status_code != 204:
					raise Exception('apUpdateAP Exception: ' + str(r2.status_code) + ' / ' + r2.text)
			return True
		except Exception as err:
			return err

			
	def apDisableAPMesh(self,controllerip,port,apiVersion,cookies,session,apmac): 

		if type(session) != type(requests.Session()):
			session = requests.Session()

		try:
		
			payload2 = dict();
			payload2.update({'meshMode':'DISABLE'});
			#payload2.update({"uplinkSelection" : "MANUAL"});
			#payload2.update({"meshUplinkEntryList" : [  ] });
			
			r2 = session.patch("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/meshOptions".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,apMac=apmac),cookies=cookies,verify=False,timeout=60,params=payload,json=payload2 );  
			
			if r2.status_code != 204:
				raise Exception("apUpdateAP Exception: "+str(r2.status_code)+' / '+r2.text);

			#response = json.loads(r2.content.decode());

			return True;

		except Exception as err:
			return err

	
	def apDeleteAPMesh(self,controllerip,port,apiVersion,cookies,session,apmac): 

		if type(session) != type(requests.Session()):
			session = requests.Session()

		try:

			r2 = session.delete("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/meshOptions".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,apMac=apmac),cookies=cookies,verify=False,timeout=160 );  
			
			if r2.status_code != 204:
				raise Exception("apUpdateAP Exception: "+str(r2.status_code)+' / '+r2.text);

			#response = json.loads(r2.content.decode());

			return True;

		except Exception as err:
			return err

	def apUpdateAP(self,controllerip,port,apiVersion,cookies,session,payload2,apmac): 

		if type(session) != type(requests.Session()):
			session = requests.Session()

		try:

			r2 = session.patch("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,apMac=apmac),cookies=cookies,verify=False,timeout=60,json=payload2,params=payload ); 
			
			if r2.status_code != 204:
				raise Exception("apUpdateAP Exception: "+str(r2.status_code)+' / '+r2.text);

			#response = json.loads(r2.content.decode());

			return True;

		except Exception as err:
			return err



	def apGetAPOnDemandInfo(self,controllerip,port,apiVersion,cookies,session,apmac): 

		if type(session) != type(requests.Session()):
			session = requests.Session()

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/operational/onDemandData".format(apMac = apmac,controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(10,1200), params=payload)   #get the ap list from the controller
			if r2.status_code != 200:
				raise Exception("apGetAPOnDemandInfo Exception: "+str(r2.status_code)+' / '+ r2.text);

		

			response = json.loads(r2.content.decode());

			return response #['list'];

		except Exception as err:
			return err
	
	def apGetAPOpSummary(self,controllerip,port,apiVersion,cookies,session,apmac): 

		if type(session) != type(requests.Session()):
			session = requests.Session()

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/operational/summary".format(apMac = apmac,controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(10,1200), params=payload)   #get the ap list from the controller
			if r2.status_code != 200:
				raise Exception('apGetAPOpSummary Exception: '+str(r2.status_code)+' / '+ r2.text);

		

			response = json.loads(r2.content.decode());

			return response

		except Exception as err:
			return err
			
	def apAPReboot(self,controllerip,port,apiVersion,cookies,session,apmac): 

		if type(session) != type(requests.Session()):
			session = requests.Session()

		try:
			r2 = session.put("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/reboot".format(apMac = apmac,controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(10,1200), params=payload, json = {} )   #get the ap list from the controller
			if r2.status_code != 204:
				raise Exception("apAPReboot Exception: "+str(r2.status_code)+' '+r2.text);

			return True;

		except Exception as err:
			return err
			
	def apDelete(self,controllerip,port,apiVersion,cookies,session,apmac): 

		if type(session) != type(requests.Session()):
			session = requests.Session()

		try:
			r2 = session.delete("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}".format(apMac = apmac,controller_ip=controllerip,port=port,apiVersion=apiVersion),cookies=cookies,verify=False,timeout=(10,120), params=payload)   #remove AP from controller
			if r2.status_code != 204:
				raise Exception("apDelete Exception: "+str(r2.status_code)+' '+r2.text);

			return True;

		except Exception as err:
			return err



	def apGetWLANGroup(self,controllerip,port,apiVersion,cookies,zoneId,wlanGroupID,session):

		#function to retrieve wlan group detail

		if type(session) != type(requests.Session()):
			session = requests.Session();  

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/rkszones/{zoneId}/wlangroups/{wlanGroupID}".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,zoneId=zoneId,wlanGroupID=wlanGroupID),cookies=cookies,verify=False,timeout=(10,1200), params=payload)   #get the wlan grp names and corresponding ids
			if r2.status_code != 200:
				raise Exception("apGetWLANGroup Exception: "+str(r2.status_code)+' '+r2.text);

			response = json.loads(r2.content.decode())
   
			return response;

		except Exception as err:
			return err

		

	def apiLegacyLogin(self,controllerip,username,password,sLeg):

		if type(sLeg) != type(requests.Session()):
			sLeg = requests.Session();

		sLeg.auth = (username, password)

		jsnAuth = json.dumps({'userName':username,'password':password});

		#@TODO: how are both legacy and 3_1 APIs set to have a unified timestamp of returned items?

		jsnHeader = {'TimezoneOffset':'-180','GMTOffset':'+0300','Accept':'application/json','Content-Type':'application/json'};

		try:
			r1=sLeg.put('https://{controller_ip}:8443/wsg/api/scg/session/login'.format(controller_ip=controllerip), headers = jsnHeader, data = jsnAuth, verify=False, timeout=30 );
			if r1.status_code != 200:
				raise Exception("apiLegacyLogin Exception: "+str(r1.status_code)+' '+r1.text);
			response= json.loads(r1.content.decode())
			print(response)
			if response['success'] == "false":
				raise Exception("apiLegacyLogin Exception: "+str(response["message"]))
			return r1;

		except Exception as err:
			return err

	def apiLegacyLogout(self,controllerip,sLeg):

		if type(sLeg) != type(requests.Session()):
			sLeg = requests.Session();

		#@TODO: how are both legacy and 3_1 APIs set to have a unified timestamp of returned items?

		try:
			r1=sLeg.delete('https://{controller_ip}:8443/wsg/api/scg/session/login'.format(controller_ip=controllerip), verify=False, timeout=30 );
			if r1.status_code != 200:
				raise Exception("apiLegacyLogout Exception: "+str(r1.status_code)+' '+r1.text);

			sLeg = requests.Session();
				
			return r1;

		except Exception as err:
			return err
   



	def apiGetLegacyAPReport(self,controllerip,session): 

		if type(session) != type(requests.Session()):
			session = requests.Session();

		try:
			lst = session.get('https://'+controllerip+':8443/wsg/api/rest/aps', verify=False, timeout=1600);
			if lst.status_code != 200:
				raise Exception("apiGetLegacyAPReport Exception: "+str(lst.status_code)+' '+lst.text);
				
			response = json.loads(lst.content.decode())
   
			return response['aps'];

		except Exception as err:
			return err
			


	def apiGetLegacyZoneReport(self,controllerip,sLeg): 

		if type(sLeg) != type(requests.Session()):
			sLeg = requests.Session();

		try:
			lstAPs = sLeg.get('https://'+controllerip+':8443/wsg/api/rest/mobilityzones');
			if lstAPs.status_code != 200:
				raise Exception("apiGetLegacyZoneReport Exception: "+str(lstAPs.status_code)+' '+lstAPs.text);

			response = json.loads(lstAPs.content.decode())
   
			return response['mobilityzones'];

		except Exception as err:
			return err
	



	def apiGetLegacySummaryReport(self,controllerip,sLeg): 

		if type(sLeg) != type(requests.Session()):
			sLeg = requests.Session();

		try:
			lstAPs = sLeg.get('https://'+controllerip+':8443/wsg/api/scg/planes/systemSummary');
			if lstAPs.status_code != 200:
				raise Exception("apiGetLegacySummaryReport Exception: "+str(lstAPs.status_code));

			response = json.loads(lstAPs.content.decode())
   
			return response;

		except Exception as err:
			return err
			
	
	def apGetAPAlarm(self,controllerip,port,apiVersion,cookies,session,apMac,parameters=dict() ): 
			
		#function to retrieve wlan group detail

		if type(session) != type(requests.Session()):
			session = requests.Session();  

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/operational/alarms".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,apMac=apMac),cookies=cookies,verify=False,timeout=(10,1200), params=payload, json = parameters)   #get the wlan grp names and corresponding ids
			if r2.status_code not in [200,204]:
				raise Exception("apGetWLANGroup Exception: "+str(r2.status_code)+' '+r2.text);

			response = json.loads(r2.content.decode())
   
			return response['list'];

		except Exception as err:
			return err
			
	def apGetAP(self,controllerip,port,apiVersion,cookies,session,apMac,parameters=dict() ): 
			
		#function to retrieve wlan group detail

		if type(session) != type(requests.Session()):
			session = requests.Session();  

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,apMac=apMac),cookies=cookies,verify=False,timeout=(10,1200), params=payload, json = parameters)   #get the wlan grp names and corresponding ids
			if r2.status_code not in [200,204]:
				raise Exception("apGetAP Exception: "+str(r2.status_code)+' '+r2.text);

			response = json.loads(r2.content.decode())
   
			return response;

		except Exception as err:
			return err
	
		
	def apGetAPEvents(self,controllerip,port,apiVersion,cookies,session,apMac,parameters=dict() ): 
			
		#function to retrieve wlan group detail

		if type(session) != type(requests.Session()):
			session = requests.Session();  

		try:
			r2 = session.get("https://{controller_ip}:{port}/api/public/{apiVersion}/aps/{apMac}/operational/events".format(controller_ip=controllerip,port=port,apiVersion=apiVersion,apMac=apMac),cookies=cookies,verify=False,timeout=(10,1200), params=payload, json = parameters)   #get the wlan grp names and corresponding ids
			if r2.status_code not in [200,204]:
				raise Exception("apGetWLANGroup Exception: "+str(r2.status_code)+' '+r2.text);

			response = json.loads(r2.content.decode())
   
			return response['list'];

		except Exception as err:
			return err







