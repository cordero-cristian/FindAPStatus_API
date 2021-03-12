from flask import Blueprint
from flask_restx import Api
from selfInstall.api.apStatus.endpoints import selfInstallNs

apiBp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    apiBp,
    version="1.0",
    title="WAA Self Install API",
    description="Please contact DL-NTO-Wireless-Analytics@charter.com for any issues",
    doc="/ui",
    authorizations=authorizations,
)

api.add_namespace(selfInstallNs, path="/self-install")
