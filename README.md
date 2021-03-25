![Charter Logo](images/images_Charter_R_Logo_RGB.png)

# Wireless Automation and Analytics (WAA) Self- Install API

#### Summary:

The WNO AP Status API was developted and is maintained by the Wireless Analytics and Automation (WAA) department at Charter and will return the status of a given Access Point (AP) mac on any Wireless Network Operations (WNO) public Wi-Fi controller by querying the various WNO Wi-Fi controller systems where the AP would connect.  

It queries various systems in real-time and will return a response detailing information regarding the AP’s operational status.  It will give in-depth details about a AP’s connection status, configuration status (readiness to transmit), and also return other various status codes in the event of a failure.  The API is vendor-agnostic, so it will return a normalized payload for both Ruckus and Cisco APs, and will also be updated as new AP vendors are deployed by WNO.

#### Sequence Flow:

![flow diagram](images/flow.png)


#### Target Audience:

The API is intended to support any Charter development requiring real-time status of Charter APs.

#### End-Point URLS:

##### Access Point Status API Endpoint
https://wno-waa-api-self-install.charter.com/api/v1/self-install/accessPointStatus
##### Swagger documentation:
https://wno-waa-api-self-install.charter.com/api/v1/ui


#### API Flow:

##### Ruckus:
![Ruckus api flow diagram](images/apiFlow.png)

##### Cisco:

![Cisco api flow diagram](images/ciscoApiFlow.png)

#### Access Point Controller Join Chronology:

1. Cable Modem (‘CM’) with ISIW tag joins CMTS
	
2. AP connects to CM and gets ISIW space IP from DHCP.  IP is registered to DLPQS API, available from APO

3. Depending on AP vendor, AP retrieves vendor-specific option 43 from DHCP

	- Ruckus:
    1. AP is directed to Ruckus Network Director (RND)
	2. RND examines subnet-based ruleset and directs AP to a regional controller
	3. AP Joins Controller and Zone specified by the Subnet Rule.  AP goes from ‘connectionState’ ‘Discovery’ to connectionState ‘Connect’
	4. Controller pushes firmware and configuration to the AP.  Several different configState values are returned during this process.
	5. AP configState changes to ‘completed’ and connectionState ‘connect’ to signal it is transmitting
	
	- Cisco:
	1. AP joins east or west provisioning controllers
	2. AP connection state changes to ‘Connect’
	3. AP configuration state changes to ‘DOWNLOADING’ while downloading firmware and configuration
	4. AP configState changes to ‘REGISTERED’ when transmitting if connectionState is ‘Connect’

#### Header Requirements

        {'Authorization':'bearer JWT token','mac':[APMAC]}

#### API Responses:

1. 'BAD_MAC_FORMAT'  -  HTTPStatus.BAD_REQUEST #400
This error is returned when the AP Mac is not passed to the API in the proper regex format.

2. 'NOT_IN_DIRECTOR' - HTTPStatus.OK #200
This status text currently applies only to Ruckus APs.  It means that the AP has not yet reached the Ruckus Network Director for its controller assignment

3.	'DIRECTOR_FAILURE' - HTTPStatus.SERVICE_UNAVAILABLE #503
This code is returned in the event that there is a system error querying the Ruckus Network Directors.
4.	'CONTROLLER_UNAUTHORIZED' - HTTPStatus.UNAUTHORIZED #401
Returned when the API is unable to authenticate directly to a WNO controller.  The authorizations are stored within a secured location in the API.  If this status is returned, please contact WAA.

5.	'DIRECTOR_UNAUTHORIZED' - HTTPStatus.UNAUTHORIZED #401
Returned when authorization fails to a Ruckus Network director.  Please contact WAA if this error is encountered.

6.	'CONTROLLER_FAILURE' - HTTPStatus.SERVICE_UNAVAILABLE #503
This error occurs when 1) the AP mac is not found on a controller, and 2) one of the controllers cannot be contacted.  This can happen because of system failure, system maintenance, etc.

7.	'NOT_ON_CONTROLLER' - HTTPStatus.OK #200
Returned if the AP is not found on a controller.

8.	'FOUND_ON_CONTROLLER' - HTTPStatus.OK #200
This status text is returned when the AP mac is found on one of the WNO controllers.  The response payload (detailed below) should be examined for further information regarding the AP’s readiness.

9.	'SYSTEM_EXCEPTION' - HTTPStatus.SERVICE_UNAVAILABLE #503
Returned when there is an exception in the API.  

10.	'NO_DIRECTOR_SESSIONS' - HTTPStatus.SERVICE_UNAVAILABLE #503
Returned when no Ruckus Network Director sessions are available.

#### API Return Payload:

        {
        "mac":"58:93:96:27:C8:30",
        "model":"ZF7762-AC",
        "name":"2140533_VENUEBASE_COAX",
        "ip":"67.49.162.181",
        "configState":"completed",
        "connectionState":"Connect",
        "vendor":"’Ruckus’"
        }

1.	'mac': same as the input passed
2.	‘vendor’: the AP’s manufacturer, currently ‘Ruckus’ or ‘Cisco’
3.	'model': the AP’s model as reported by the controller
4.	‘name’: the AP’s name on the controller
5.	‘ip’: the IP address of the AP as reported by the controller
6.	'connectionState': details whether the AP is in one of the following statuses:  ‘Discovery’, ‘Connect’, or ‘Disconnect’.  ‘Disconnect’ implies that the AP is not currently attached to a controller.  Note that Discovery connectionState applies to Ruckus controllers and is normally returned when the AP first joins to the controller.  
7.	‘configState’
    
    -	Ruckus:

            "configState" : {
            "description" : "State of the AP configuration.",
            "enum" : [ "newConfig", "fwApplied", "fwDownloaded", "fwFailed", "configApplied", "completed", "configFailed" ]

    -	Cisco:

            ‘DOWNLOADING’ or ‘REGISTERED’
-	configState of ‘completed’ or ‘REGISTERED’ indicates that the AP is fully operational if the connectionState is ‘Connect’


#### API Access

Access is granted by Wifi Analytics and Automation for a specific application.  A request should be sent to DL-NTO-Wireless-Analytics@charter.com.  Authorization tokens should be protected and not shared between individuals or other departments.
