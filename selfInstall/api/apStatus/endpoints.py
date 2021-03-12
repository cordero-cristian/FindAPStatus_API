
from http import HTTPStatus

from flask_restx import Namespace, Resource

from selfInstall.api.apStatus.apParser import accessPointStatusReqParser, user_model
from selfInstall.api.apStatus.apFunctions import work

selfInstallNs = Namespace(name="self-install", validate=True)
selfInstallNs.models[user_model.name] = user_model


@selfInstallNs.route("/accessPointStatus", endpoint="access_point_status")
class RegisterUser(Resource):
    """ Handles HTTP requests to URL: /api/v1/self-install/accessPointStatus """

    @selfInstallNs.doc(security="Bearer")
    @selfInstallNs.expect(accessPointStatusReqParser)
    @selfInstallNs.response(int(HTTPStatus.OK), "Status of AP Goes Here", user_model)
    @selfInstallNs.response(int(HTTPStatus.NOT_FOUND), "Access Point Could Not Be Found")
    @selfInstallNs.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    @selfInstallNs.marshal_with(user_model)
    def get(self):
        """ Find an Access Point and return its Status """
        requestData = accessPointStatusReqParser.parse_args()
        mac = requestData.get("mac")
        return work(mac)