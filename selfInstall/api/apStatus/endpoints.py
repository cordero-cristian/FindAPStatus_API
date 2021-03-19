
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
    @selfInstallNs.response(int(HTTPStatus.OK), """Please see Response 'status_text' for addtional Info

Can be one of the following:

FOUND_ON_CONTROLLER
NOT_IN_DIRECTOR
NOT_ON_CONTROLLER
"""
                            )
    @selfInstallNs.response(int(HTTPStatus.NOT_FOUND), "Access Point Could Not Be Found")
    @selfInstallNs.response(int(HTTPStatus.CONFLICT), "Busy WLC or Vsz/RND")
    @selfInstallNs.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), "Not found on vWLC or Vsz")
    @selfInstallNs.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    @selfInstallNs.response(int(HTTPStatus.BAD_REQUEST), "BAD MAC FORMAT")
    def get(self):
        """ Find an Access Point and return its Status """
        requestData = accessPointStatusReqParser.parse_args()
        mac = requestData.get("mac")
        response = getAccessPointStatus(mac)
        if response['status_code'] == HTTPStatus.OK:
            return response
        else:
            return abort(int(response['status_code']), response['status_text'])
