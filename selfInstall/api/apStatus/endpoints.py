
from http import HTTPStatus

from flask_restx import Namespace, Resource, abort

from selfInstall.api.apStatus.apParser import accessPointStatusReqParser
from selfInstall.api.apStatus.apFunctions import getAccessPointStatus

selfInstallNs = Namespace(name="self-install", validate=True)


@selfInstallNs.route("/accessPointStatus", endpoint="access_point_status")
class RegisterUser(Resource):
    """ Handles HTTP requests to URL: /api/v1/self-install/accessPointStatus """

    @selfInstallNs.doc(security="Bearer")
    @selfInstallNs.expect(accessPointStatusReqParser)
    @selfInstallNs.response(int(HTTPStatus.OK), """OK: Successful Attempt to Locate a Access Point

Examine Response: 'status_text' for addtional Info

Can be one of the following:

**FOUND_ON_CONTROLLER** - AP mac is found on one of the WNO controllers.  The response payload should be examined for further information regarding the AP’s readiness.


**NOT_IN_DIRECTOR** - Applies only to Ruckus APs. The AP has not yet reached the Ruckus Network Director for its controller assignment.


**NOT_ON_CONTROLLER** - AP is not found on a controller.
"""
                            )
    @selfInstallNs.response(int(HTTPStatus.BAD_REQUEST), """BAD_REQUEST: Incorrect formatting for a Access Point MAC Address

Examine Response: 'status_text' for addtional Info

Can be one of the following:

**BAD_MAC_FORMAT** - This error is returned when the AP Mac is not passed to the API in the proper regex format.
    """)
    @selfInstallNs.response(int(HTTPStatus.UNAUTHORIZED), """UNAUTHORIZED: Bad JWT or Controller Logon Failure

Examine Response: 'status_text' for addtional Info

Can be one of the following:

**CONTROLLER_UNAUTHORIZED** - Unable to authenticate directly to a WNO controller.


**DIRECTOR_UNAUTHORIZED** - Authorization failed to a Ruckus Network director.


**INVALID_TOKEN** - Unathorized JWT
    """)
    @selfInstallNs.response(int(HTTPStatus.SERVICE_UNAVAILABLE), """SERVICE_UNAVAILABLE: Critical Failure on a Controller System

Examine Response: 'status_text' for addtional Info

Can be one of the following:

**DIRECTOR_FAILURE** - System error querying the Ruckus Network Directors.


**NO_RND_SESSIONS** - No Ruckus Network Director sessions are available.


**CONTROLLER_FAILURE** - The AP mac is not found on a controller, and one of the controllers cannot be contacted.


**SYSTEM_EXCEPTION** - Other execption for Controller realated issues.
    """)
    def get(self):
        """ Find an Access Point and return its Status """
        requestData = accessPointStatusReqParser.parse_args()
        mac = requestData.get("mac")
        response = getAccessPointStatus(mac)
        status_code = response.pop('status_code')
        if status_code == HTTPStatus.OK:
            return response
        else:
            return abort(int(status_code), response['status_text'])
