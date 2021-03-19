
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

**FOUND_ON_CONTROLLER**
**NOT_IN_DIRECTOR**
**NOT_ON_CONTROLLER**
"""
                            )
    @selfInstallNs.response(int(HTTPStatus.BAD_REQUEST), """BAD_REQUEST: Incorrect formatting for a Access Point MAC Address

Examine Response: 'status_text' for addtional Info

Can be one of the following:

**BAD_MAC_FORMAT**
    """)
    @selfInstallNs.response(int(HTTPStatus.UNAUTHORIZED), """UNAUTHORIZED: Bad JWT or Controller Logon Failure

Examine Response: 'status_text' for addtional Info

Can be one of the following:

**CONTROLLER_UNAUTHORIZED**
**DIRECTOR_UNAUTHORIZED**
**INVALID_TOKEN**
    """)
    @selfInstallNs.response(int(HTTPStatus.SERVICE_UNAVAILABLE), """SERVICE_UNAVAILABLE: Critical Failure on a Controller System

Examine Response: 'status_text' for addtional Info

Can be one of the following:

**DIRECTOR_FAILURE**
**NO_RND_SESSIONS**
**CONTROLLER_FAILURE**
**SYSTEM_EXCEPTION**
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
